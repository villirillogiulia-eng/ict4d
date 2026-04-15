import requests
import json

def fetch_health_data():
    # Overpass API query for health facilities in The Gambia bounding box
    # [minLat, minLon, maxLat, maxLon]
    overpass_url = "https://overpass-api.de/api/interpreter"
    overpass_query = """
    [out:json][timeout:90];
    (
      node["amenity"~"hospital|clinic|doctors|pharmacy|health_post"](13.0,-17.0,14.0,-13.5);
      way["amenity"~"hospital|clinic|doctors|pharmacy|health_post"](13.0,-17.0,14.0,-13.5);
    );
    out center;
    """
    
    print("Fetching data from Overpass API (this may take a minute)...")
    try:
        response = requests.post(overpass_url, data={'data': overpass_query}, timeout=100)
        response.raise_for_status()
        data = response.json()
        
        # Convert OSM JSON to a simple GeoJSON FeatureCollection
        geojson = {
            "type": "FeatureCollection",
            "features": []
        }
        
        for element in data.get('elements', []):
            # Use 'center' for ways, or 'lat'/'lon' for nodes
            lat = element.get('lat') or element.get('center', {}).get('lat')
            lon = element.get('lon') or element.get('center', {}).get('lon')
            
            if lat and lon:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": element.get('tags', {})
                }
                # Add the OSM ID for reference
                feature["properties"]["osm_id"] = element.get('id')
                geojson["features"].append(feature)
        
        with open('health_facilities.geojson', 'w') as f:
            json.dump(geojson, f, indent=2)
            
        print(f"Successfully saved {len(geojson['features'])} health facilities to health_facilities.geojson")
        
    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    fetch_health_data()
