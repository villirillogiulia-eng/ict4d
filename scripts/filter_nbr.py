import json

# Define the bounding box for North Bank Region (approximate)
# North of the Gambia River, south of the Senegal border
NBR_MIN_LAT = 13.45 
NBR_MAX_LAT = 13.75
NBR_MIN_LON = -16.50
NBR_MAX_LON = -14.60

def filter_nbr_facilities(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    nbr_features = []
    for feature in data['features']:
        lon, lat = feature['geometry']['coordinates']
        if NBR_MIN_LAT <= lat <= NBR_MAX_LAT and NBR_MIN_LON <= lon <= NBR_MAX_LON:
            feature['properties']['region'] = 'North Bank'
            nbr_features.append(feature)
            
    nbr_geojson = {
        "type": "FeatureCollection",
        "features": nbr_features
    }
    
    with open(output_file, 'w') as f:
        json.dump(nbr_geojson, f, indent=2)
        
    print(f"Found {len(nbr_features)} health facilities in the North Bank Region.")
    high_risk = sum(1 for f in nbr_features if f['properties']['flood_risk'] == 'high')
    print(f"Of these, {high_risk} are at high risk of flooding.")

if __name__ == "__main__":
    filter_nbr_facilities('health_facilities_with_risk.geojson', 'nbr_health_facilities.geojson')
