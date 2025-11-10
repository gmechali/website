

import json

# Read the existing JSONL file (which already has the alternative names and type)
with open('/Users/gmechali/Desktop/datacommons/website/places.jsonl', 'r') as f:
    lines = f.readlines()

updated_lines = []
for line in lines:
    original_data = json.loads(line)

    # The original_data already has the desired top-level fields
    # We just need to ensure the 'id' field is correctly formatted if it's used by the import process
    # For now, we'll assume the import process will map 'dcid' to its internal ID.
    # If the import requires an 'id' field at the top level, it should be 'dcid' itself.
    # Let's output the original_data as is, as per the request to remove 'struct_data' and 'document ID'.
    updated_lines.append(json.dumps(original_data) + '\n')

# Write the updated content to a new file
with open('/Users/gmechali/Desktop/datacommons/website/places_for_import.jsonl', 'w') as f:
    f.writelines(updated_lines)

print("Successfully created places_for_import.jsonl with top-level fields (dcid, name, type, alternativeNames).")

