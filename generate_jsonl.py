import datacommons as dc
import json

dcids = []
with open('/Users/gmechali/Desktop/datacommons/website/static/sitemap/Country.0.txt') as f:
    for line in f:
        line = line.strip()
        if not line.startswith("https://datacommons.org/place/"):
            continue
        dcids.append(line.split('https://datacommons.org/place/')[-1])

# Get names and types for all dcids in a single API call
names = dc.get_property_values(dcids, 'name')
types = dc.get_property_values(dcids, 'typeOf')

alternative_names_map = {
    "country/USA": ["USA", "United States of America", "America"],
    "country/GBR": ["Great Britain", "UK", "Britain"],
    "country/ARE": ["UAE"],
    "country/CHN": ["People's Republic of China"],
    "country/RUS": ["Russian Federation"],
    "country/KOR": ["Republic of Korea"],
    "country/PRK": ["Democratic People's Republic of Korea"],
    "country/VNM": ["Vietnam"],
}

with open('places.jsonl', 'w') as f:
    for dcid in dcids:
        # There may be multiple names for a dcid, we take the first one.
        name = names[dcid][0] if dcid in names and names[dcid] else dcid.split('/')[-1]
        # There may be multiple types for a dcid, we take the first one.
        place_type = types[dcid][0] if dcid in types and types[dcid] else "Unknown"

        alternative_names = alternative_names_map.get(dcid, [])

        json_object = {
            "dcid": dcid,
            "name": name,
            "type": place_type,
            "alternativeNames": alternative_names
        }

        f.write(json.dumps(json_object) + '\n')

print("Successfully created places.jsonl")