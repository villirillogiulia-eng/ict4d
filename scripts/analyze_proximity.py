import json
import math

def haversine(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + \
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * \
        math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def separate_nearby_sites(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    features = data['features']
    n = len(features)
    
    # Track which sites have a neighbor within 1km
    has_neighbor = [False] * n
    
    for i in range(n):
        lon1, lat1 = features[i]['geometry']['coordinates']
        for j in range(i + 1, n):
            lon2, lat2 = features[j]['geometry']['coordinates']
            
            distance = haversine(lat1, lon1, lat2, lon2)
            
            if distance <= 1.0: # 1 kilometer
                has_neighbor[i] = True
                has_neighbor[j] = True
    
    # Add property to GeoJSON
    for i in range(n):
        features[i]['properties']['proximity_group'] = 'clustered' if has_neighbor[i] else 'isolated'
        features[i]['properties']['has_neighbor_within_1km'] = has_neighbor[i]

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    clustered_count = sum(has_neighbor)
    print(f"Analysis Complete:")
    print(f"- Total sites: {n}")
    print(f"- Clustered (within 1km of another site): {clustered_count}")
    print(f"- Isolated (no other site within 1km): {n - clustered_count}")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    separate_nearby_sites('health_facilities.geojson', 'health_facilities_proximity.geojson')
