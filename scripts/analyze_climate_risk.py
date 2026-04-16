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

def calculate_risk_score(distance, severity, dead, displaced):
    # Normalize inputs
    try:
        sev = float(severity) if severity and severity != 'N/A' else 1.0
    except ValueError:
        sev = 1.0
        
    try:
        deaths = float(dead) if dead else 0.0
    except ValueError:
        deaths = 0.0
        
    try:
        disp = float(displaced) if displaced else 0.0
    except ValueError:
        disp = 0.0

    # Distance factor: closer means higher risk
    # We use a decay function: 1 / (1 + distance)
    dist_factor = 1.0 / (1.0 + distance)
    
    # Impact factor: based on severity, deaths and displacements
    # Severity is usually 1, 1.5, or 2
    # Deaths and displacements can be large, so we log them
    impact_factor = sev + math.log1p(deaths) + math.log1p(disp / 100.0)
    
    return dist_factor * impact_factor

def identify_climate_risk(health_file, hazard_file, output_file):
    with open(health_file, 'r') as f:
        health_data = json.load(f)
    with open(hazard_file, 'r') as f:
        hazard_data = json.load(f)
    
    health_sites = health_data['features']
    hazard_events = hazard_data['features']
    
    print(f"Analyzing {len(health_sites)} health sites against {len(hazard_events)} climate hazards...")

    for h_feat in health_sites:
        h_lon, h_lat = h_feat['geometry']['coordinates']
        
        max_risk_score = 0
        nearest_hazard_dist = float('inf')
        nearest_hazard_type = 'None'
        
        for f_feat in hazard_events:
            f_lon, f_lat = f_feat['geometry']['coordinates']
            dist = haversine(h_lat, h_lon, f_lat, f_lon)
            
            if dist < nearest_hazard_dist:
                nearest_hazard_dist = dist
                nearest_hazard_type = f_feat['properties']['hazard_type']
            
            # Calculate risk score for this hazard
            score = calculate_risk_score(
                dist, 
                f_feat['properties'].get('severity'),
                f_feat['properties'].get('dead'),
                f_feat['properties'].get('displaced')
            )
            
            if score > max_risk_score:
                max_risk_score = score
        
        # Categorize risk
        h_feat['properties']['climate_risk_score'] = round(max_risk_score, 3)
        h_feat['properties']['nearest_hazard_distance_km'] = round(nearest_hazard_dist, 3)
        h_feat['properties']['nearest_hazard_type'] = nearest_hazard_type
        
        # Determine risk level
        if max_risk_score > 1.5:
            h_feat['properties']['flood_risk'] = 'high' # Keeping key for backward compatibility
            h_feat['properties']['climate_risk_level'] = 'High'
        elif max_risk_score > 0.8:
            h_feat['properties']['flood_risk'] = 'medium'
            h_feat['properties']['climate_risk_level'] = 'Medium'
        else:
            h_feat['properties']['flood_risk'] = 'low'
            h_feat['properties']['climate_risk_level'] = 'Low'

    with open(output_file, 'w') as f:
        json.dump(health_data, f, indent=2)
    
    high_count = sum(1 for f in health_sites if f['properties']['climate_risk_level'] == 'High')
    med_count = sum(1 for f in health_sites if f['properties']['climate_risk_level'] == 'Medium')
    
    print(f"Analysis Complete:")
    print(f"- Total health sites: {len(health_sites)}")
    print(f"- High Risk: {high_count}")
    print(f"- Medium Risk: {med_count}")
    print(f"- Low Risk: {len(health_sites) - high_count - med_count}")
    print(f"Results saved to: {output_file}")

if __name__ == "__main__":
    identify_climate_risk('data/health_facilities.geojson', 'data/floods.geojson', 'data/health_facilities_with_risk.geojson')
