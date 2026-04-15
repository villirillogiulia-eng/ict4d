import json
import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Earth radius in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def identify_flood_risk(health_file, flood_file, output_file):
    with open(health_file, 'r') as f:
        health_data = json.load(f)
    with open(flood_file, 'r') as f:
        flood_data = json.load(f)
    
    all_features = []
    
    health_sites = health_data['features']
    flood_events = flood_data['features']
    
    print(f"Comparing {len(health_sites)} health sites against {len(flood_events)} flood events...")

    for h_feat in health_sites:
        h_lon, h_lat = h_feat['geometry']['coordinates']
        is_at_risk = False
        nearest_flood_dist = float('inf')
        
        for f_feat in flood_events:
            f_lon, f_lat = f_feat['geometry']['coordinates']
            dist = haversine(h_lat, h_lon, f_lat, f_lon)
            if dist < nearest_flood_dist:
                nearest_flood_dist = dist
        
        # Determine risk
        if nearest_flood_dist <= 1.0:
            h_feat['properties']['flood_risk'] = 'high'
        else:
            h_feat['properties']['flood_risk'] = 'low'
            
        h_feat['properties']['nearest_flood_distance_km'] = round(nearest_flood_dist, 3)
        all_features.append(h_feat)

    health_data['features'] = all_features

    with open(output_file, 'w') as f:
        json.dump(health_data, f, indent=2)
    
    at_risk_count = sum(1 for f in all_features if f['properties']['flood_risk'] == 'high')
    print(f"Analysis Complete:")
    print(f"- Total health sites: {len(all_features)}")
    print(f"- High Risk (within 1km): {at_risk_count}")
    print(f"- Low Risk: {len(all_features) - at_risk_count}")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    identify_flood_risk('health_facilities.geojson', 'floods.geojson', 'health_facilities_with_risk.geojson')
