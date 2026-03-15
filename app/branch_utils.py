import requests
import json
from pathlib import Path

overpass_url = "https://overpass-api.de/api/interpreter"
cache_dir = Path("data/branch_cache")
cache_dir.mkdir(parents=True, exist_ok=True)

def fetch_hm_branches_osm(city):
    """
    Fetch H&M branch locations from OSM using Overpass API.
    Caches results to avoid repeated requests.
    """
    cache_path = cache_dir / f"{city.lower().replace(' ', '_')}_hm_branches.json"
    if cache_path.exists():
        with open(cache_path, 'r', encoding='utf-8') as f:
            print(f"[INFO] Using cached data for {city}")
            return json.load(f)

    print(f"[INFO] Querying Overpass API for H&M branches in {city}...")
    query = f"""
    [out:json];
    area["name"="{city}"]->.searchArea;
    (
    node["shop"="clothes"]["brand"="H&M"](area.searchArea);
    way["shop"="clothes"]["brand"="H&M"](area.searchArea);
    relation["shop"="clothes"]["brand"="H&M"](area.searchArea);
    );
    out center;
    """
    
    response = requests.post(overpass_url, data={'data': query}, headers={"User-Agent": "waste-mvp-bot/0.1"})
    response.raise_for_status()

    data = response.json()
    branches = []
    for element in data.get('elements', []):
        if 'lat' in element and 'lon' in element:
            name = element['tags'].get('name', 'H&M Store')
            branches.append({
                'name': name,
                'lat': element['lat'],
                'lon': element['lon']
            })

    with open(cache_path, 'w', encoding='utf-8') as f:
        json.dump(branches, f, indent=2)
        print(f"[INFO] Cached branch data for {city} at {cache_path}")

    return branches
