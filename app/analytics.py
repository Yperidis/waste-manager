import dash
from branch_utils import fetch_hm_branches_osm
from dash import html, dcc, Input, Output
import dash_leaflet as dl
import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import parse_qs


def scrape_branch_data(city):
    # Example: scrape "H&M Berlin textile recycling" search pages
    query = f"H&M {city} textile recycling intake"
    url = "https://www.google.com/search"
    resp = requests.get(url, params={'q': query}, headers={'User-Agent': '*'})
    soup = BeautifulSoup(resp.text, 'html.parser')
    snippets = [p.get_text() for p in soup.select('div.BNeawe')[:5]]
    return snippets


# H&M locations sample
# branches = {
#     'Berlin': [
#         {'name': 'H&M Friedrichstraße', 'lat': 52.5208, 'lon': 13.3877},
#         {'name': 'H&M Kurfürstendamm', 'lat': 52.5026, 'lon': 13.3302},
#     ],
#     'Athens': [
#         {'name': 'H&M Ermou', 'lat': 37.9755, 'lon': 23.7341},
#         {'name': 'H&M The Mall', 'lat': 38.0248, 'lon': 23.7462},
#     ]
# }

def init_dashboard(server):
    dash_app = dash.Dash(__name__, server=server, routes_pathname_prefix="/analytics/")

    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.H1("Textile Inflows to H&M Branches"),
        dl.Map(id='branch-map', style={'width': '100%', 'height': '400px'}, center=[52.52, 13.405], zoom=12, children=[dl.TileLayer()]),
        html.Div(id='kpi-output'),
        html.H3("Scraped Public Data Snippets"),
        html.Ul(id='snippets')
    ])

    @dash_app.callback(
        [Output('branch-map', 'children'),
         Output('branch-map', 'center'),
         Output('kpi-output', 'children'),
         Output('snippets', 'children')],
        Input('url', 'search')
    )
    def update_map(query_string):
        parsed = parse_qs(query_string.lstrip('?'))
        city = parsed.get('location', ['Berlin'])[0]  # fallback to Berlin
        branches = fetch_hm_branches_osm(city)
        if not branches:
            return [dl.TileLayer()], (0,0), html.Div("No H&M branches found."), []

        brs = branches
        markers = [dl.Marker(position=(b['lat'], b['lon']), children=dl.Popup(f"{b['name']}")) for b in brs]
        center = (brs[0]['lat'], brs[0]['lon']) if brs else (0, 0)

        # Simple KPI estimates
        df = pd.DataFrame(brs)
        total_inflow = len(brs) * 2000
        kpis = html.Div([
            html.P(f"Estimated total inflow: {total_inflow} kg/month"),
            html.P(f"Branches: {len(brs)}")
        ])

        snippets = [html.Li(text) for text in scrape_branch_data(city)]
        children = [dl.TileLayer()] + markers

        return children, center, kpis, snippets

    return dash_app
