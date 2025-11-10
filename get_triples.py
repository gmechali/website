
import datacommons as dc
import json

# Fetch all triples for country/GBR
triples = dc.get_triples(["country/GBR"])

# Print the triples in a readable format
print(json.dumps(triples, indent=2))
