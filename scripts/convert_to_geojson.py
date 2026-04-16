import csv
import json

def csv_to_geojson(csv_file, geojson_file):
    features = []
    count = 0
    with open(csv_file, 'r', encoding='utf-8-sig') as f: # Added 'utf-8-sig' to handle BOM
        reader = csv.DictReader(f)
        for row in reader:
            try:
                # Clean keys just in case there are hidden spaces
                clean_row = {k.strip(): v for k, v in row.items()}
                
                # Only include Gambia records
                country = clean_row.get('Country', 'Unknown')
                other_country = clean_row.get('OtherCountry', '')
                
                if 'gambia' not in country.lower() and 'gambia' not in other_country.lower():
                    continue

                lon_str = clean_row.get('long')
                lat_str = clean_row.get('lat')
                
                if not lon_str or not lat_str:
                    continue
                    
                lon = float(lon_str)
                lat = float(lat_str)
                
                # Determine hazard type based on MainCause
                cause = clean_row.get('MainCause', 'Unknown')
                hazard_type = 'Flood' # Default
                if any(x in cause.lower() for x in ['drought', 'dry spell', 'rainfall deficit']):
                    hazard_type = 'Drought'
                elif any(x in cause.lower() for x in ['fire', 'bushfire']):
                    hazard_type = 'Fire'
                elif any(x in cause.lower() for x in ['erosion', 'salinity']):
                    hazard_type = 'Coastal'
                elif 'heat' in cause.lower():
                    hazard_type = 'Heat'

                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "id": clean_row.get('ID', 'N/A'),
                        "country": country,
                        "hazard_type": hazard_type,
                        "cause": cause,
                        "date": clean_row.get('Began', 'N/A'),
                        "severity": clean_row.get('Severity', 'N/A'),
                        "dead": clean_row.get('Dead', '0'),
                        "displaced": clean_row.get('Displaced', '0'),
                        "area": clean_row.get('Area', '0')
                    }
                }
                features.append(feature)
                count += 1
            except (ValueError, KeyError) as e:
                # print(f"Skipping row due to error: {e}")
                continue

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Successfully processed {count} climate hazard events into {geojson_file}")

if __name__ == "__main__":
    csv_to_geojson('data/FloodArchive.csv', 'data/floods.geojson')
