"""Analytics helpers for the waste management MVP."""

import dash
import dash_leaflet as dl
import requests

from app.branch_utils import fetch_hm_branches_osm
from bs4 import BeautifulSoup
from dash import html, dcc, Input, Output, State
from flask import Flask
from urllib.parse import parse_qs

# Configuration for waste categories
WASTE_CATEGORIES = {
    "Textiles": ["H&M", "Zara", "Local Charity"],
    "Plastics": ["PET", "PE", "PS", "PVC", "PP", "Plastic Films"],
    "Plastic Films": ["LDP", "HDP"],
}


def scrape_branch_data(city: str, subcategory: str) -> list[str]:
    """Scrape snippets for specific waste categories and locations.

    Parameters
    ----------
    city : str
        The city for recycling search.
    subcategory : str
        The waste subcategory or brand.

    Returns
    -------
    list[str]
        List of scraped text snippets.
    """
    query = f"{subcategory} {city} recycling intake"
    url = "https://www.google.com/search"
    try:
        resp = requests.get(
            url, params={"q": query}, headers={"User-Agent": "*"}, timeout=5
        )
        soup = BeautifulSoup(resp.text, "html.parser")
        snippets = [p.get_text() for p in soup.select("div.BNeawe")[:5]]
        return snippets
    except Exception:
        return ["Data currently unavailable from external sources."]


def init_dashboard(server: Flask) -> dash.Dash:
    """Create and register a Dash analytics dashboard with dynamic user inputs.

    Parameters
    ----------
    server : Flask
        The Flask server instance to register the Dash app with.

    Returns
    -------
    dash.Dash
        The initialized Dash application.
    """
    dash_app = dash.Dash(__name__, server=server, routes_pathname_prefix="/analytics/")

    dash_app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            html.Div(
                [
                    html.H1("Waste Flow Analytics Dashboard"),
                    # Category Selectors
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Main Category:"),
                                    dcc.Dropdown(
                                        id="category-dropdown",
                                        options=[
                                            {"label": k, "value": k}
                                            for k in WASTE_CATEGORIES.keys()
                                        ],
                                        value="Textiles",
                                        clearable=False,
                                    ),
                                ],
                                style={"width": "48%", "display": "inline-block"},
                            ),
                            html.Div(
                                [
                                    html.Label("Subcategory/Brand:"),
                                    dcc.Dropdown(
                                        id="subcategory-dropdown", clearable=False
                                    ),
                                ],
                                style={
                                    "width": "48%",
                                    "display": "inline-block",
                                    "float": "right",
                                },
                            ),
                        ],
                        style={
                            "padding": "20px",
                            "background": "#f9f9f9",
                            "borderRadius": "10px",
                            "marginBottom": "20px",
                        },
                    ),
                ]
            ),
            dl.Map(
                id="branch-map",
                style={"width": "100%", "height": "400px"},
                center=[52.52, 13.405],
                zoom=12,
                children=[dl.TileLayer()],
            ),
            html.Div(id="kpi-output", style={"marginTop": "20px"}),
            html.H3("Market Intelligence & Public Data"),
            html.Ul(id="snippets"),
        ],
        style={"padding": "20px"},
    )

    # Callback 1: Update subcategory dropdown based on category
    @dash_app.callback(
        [
            Output("subcategory-dropdown", "options"),
            Output("subcategory-dropdown", "value"),
        ],
        Input("category-dropdown", "value"),
    )
    def update_subcategory_list(selected_category: str):
        """Update the subcategory dropdown options based on selected category.

        Parameters
        ----------
        selected_category : str
            The selected main waste category.

        Returns
        -------
        tuple
            A tuple containing the options list and the default value.
        """
        subs = WASTE_CATEGORIES.get(selected_category, [])
        options = [{"label": s, "value": s} for s in subs]
        default_value = subs if subs else None
        return options, default_value

    # Callback 2: Update Map, KPIs, and Scraped Data
    @dash_app.callback(
        [
            Output("branch-map", "children"),
            Output("branch-map", "center"),
            Output("kpi-output", "children"),
            Output("snippets", "children"),
        ],
        [Input("url", "search"), Input("subcategory-dropdown", "value")],
        [State("category-dropdown", "value")],
    )
    def update_dashboard_content(query_string: str, subcategory: str, category: str):
        """Update the dashboard map, KPIs, and scraped data based on inputs.

        Parameters
        ----------
        query_string : str
            The URL query string containing location.
        subcategory : str
            The selected subcategory.
        category : str
            The selected main category.

        Returns
        -------
        tuple
            A tuple containing map children, center coordinates, KPI div, and snippets list.
        """
        # 1. Handle Location Parsing
        parsed = parse_qs(query_string.lstrip("?"))
        city = parsed.get("location", ["Berlin"])

        if not subcategory:
            return [dl.TileLayer()], (0, 0), html.Div("Select a category to begin."), []

        # 2. Fetch Geographic Data (Simulated logic for OSM/Branches)
        # In a real scenario, fetch_hm_branches_osm would be parameterized by subcategory
        branches = fetch_hm_branches_osm(city) if subcategory == "H&M" else []

        # 3. Build Map Markers
        markers = [
            dl.Marker(
                position=(b["lat"], b["lon"]),
                children=dl.Popup(f"{b['name']} - {subcategory}"),
            )
            for b in branches
        ]
        center = (branches["lat"], branches["lon"]) if branches else (52.52, 13.405)

        # 4. Generate Dynamic KPIs
        # Logic varies based on category (Textiles vs Plastics)
        multiplier = 2000 if category == "Textiles" else 500
        total_volume = len(branches) * multiplier

        kpis = html.Div(
            [
                html.Div(
                    [
                        html.Strong(
                            f"Current View: {city} | {category} ({subcategory})"
                        ),
                        html.P(f"Estimated Monthly Processing: {total_volume} kg"),
                        html.P(f"Active Intake Facilities: {len(branches)}"),
                    ],
                    style={
                        "padding": "15px",
                        "borderLeft": "5px solid #2e7d32",
                        "background": "#e8f5e9",
                    },
                )
            ]
        )

        # 5. Fetch Scraped Data
        snippets_list = [
            html.Li(text) for text in scrape_branch_data(city, subcategory)
        ]
        map_children = [dl.TileLayer()] + markers

        return map_children, center, kpis, snippets_list

    return dash_app
