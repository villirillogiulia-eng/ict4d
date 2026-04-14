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
                
                lon = float(clean_row['long'])
                lat = float(clean_row['lat'])
                
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat]
                    },
                    "properties": {
                        "id": clean_row.get('ID', 'N/A'),
                        "country": clean_row.get('Country', 'Unknown'),
                        "cause": clean_row.get('MainCause', 'Unknown'),
                        "date": clean_row.get('Began', 'N/A'),
                        "severity": clean_row.get('Severity', 'N/A')
                    }
                }
                features.append(feature)
                count += 1
            except (ValueError, KeyError) as e:
                continue

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(geojson_file, 'w', encoding='utf-8') as f:
        json.dump(geojson, f, indent=2)
    
    print(f"Successfully processed {count} flood events into {geojson_file}")

if __name__ == "__main__":
    csv_to_geojson('FloodArchive.csv', 'floods.geojson')
