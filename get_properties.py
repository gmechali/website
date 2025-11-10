
import datacommons as dc
import json

# Fetch all properties for country/GBR
properties = dc.get_property_values(["country/GBR"], "*")

# Print the properties in a readable format
print(json.dumps(properties, indent=2))
