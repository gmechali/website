import datacommons as dc
import json
import os
import time
import glob

# Define the base directory for sitemap files
SITEMAP_BASE_DIR = '/Users/gmechali/Desktop/datacommons/website/static/sitemap'

# Mapping for additional alternative names
alternative_names_map = {
    "country/USA": ["United States", "America", "US", "U.S."],
    "country/GBR": ["Great Britain", "UK", "Britain", "United Kingdom of Great Britain and Northern Ireland"],
    "country/CHN": ["People's Republic of China", "PRC"],
    "country/IND": ["Bharat"],
    "country/BRA": ["Federative Republic of Brazil"],
    "country/RUS": ["Russian Federation"],
    "country/KOR": ["Republic of Korea"],
    "country/PRK": ["Democratic People's Republic of Korea", "DPRK"],
    "country/EGY": ["Arab Republic of Egypt"],
    "country/ZAF": ["Republic of South Africa"],
    "country/NLD": ["Holland"],
    "country/ITA": ["Italian Republic"],
    "country/ESP": ["Kingdom of Spain"],
    "country/SWE": ["Kingdom of Sweden"],
    "country/NOR": ["Kingdom of Norway"],
    "country/DNK": ["Kingdom of Denmark"],
    "country/FIN": ["Republic of Finland"],
    "country/IRL": ["Republic of Ireland", "Éire"],
    "country/NZL": ["Aotearoa"],
    "country/AUT": ["Republic of Austria"],
    "country/BEL": ["Kingdom of Belgium"],
    "country/GRC": ["Hellenic Republic"],
    "country/PRT": ["Portuguese Republic"],
    "country/CHE": ["Swiss Confederation"],
    "country/TUR": ["Republic of Turkey"],
    "country/UKR": ["Ukraine"],
    "country/POL": ["Republic of Poland"],
    "country/ARG": ["Argentine Republic"],
    "country/CHL": ["Republic of Chile"],
    "country/COL": ["Republic of Colombia"],
    "country/PER": ["Republic of Peru"],
    "country/VEN": ["Bolivarian Republic of Venezuela"],
    "country/SAU": ["Kingdom of Saudi Arabia"],
    "country/ISR": ["State of Israel"],
    "country/IRN": ["Islamic Republic of Iran", "Persia"],
    "country/IRQ": ["Republic of Iraq"],
    "country/SYR": ["Syrian Arab Republic"],
    "country/LBN": ["Lebanese Republic"],
    "country/JOR": ["Hashemite Kingdom of Jordan"],
    "country/KWT": ["State of Kuwait"],
    "country/QAT": ["State of Qatar"],
    "country/BHR": ["Kingdom of Bahrain"],
    "country/OMN": ["Sultanate of Oman"],
    "country/YEM": ["Republic of Yemen"],
    "country/PAK": ["Islamic Republic of Pakistan"],
    "country/BGD": ["People's Republic of Bangladesh"],
    "country/THA": ["Kingdom of Thailand", "Siam"],
    "country/VNM": ["Socialist Republic of Vietnam"],
    "country/IDN": ["Republic of Indonesia"],
    "country/PHL": ["Republic of the Philippines"],
    "country/MYS": ["Malaysia"],
    "country/SGP": ["Republic of Singapore"],
    "country/CAF": ["CAR"],
    "country/COD": ["Congo (DRC)"],
    "country/COG": ["Congo (Republic)"],
    "country/ETH": ["Federal Democratic Republic of Ethiopia"],
    "country/KEN": ["Republic of Kenya"],
    "country/NGA": ["Federal Republic of Nigeria"],
    "country/UGA": ["Republic of Uganda"],
    "country/TZA": ["United Republic of Tanzania"],
    "country/ZMB": ["Republic of Zambia"],
    "country/ZWE": ["Republic of Zimbabwe"],
    "country/GHA": ["Republic of Ghana"],
    "country/CIV": ["Ivory Coast"],
    "country/SEN": ["Republic of Senegal"],
    "country/MLI": ["Republic of Mali"],
    "country/NER": ["Republic of Niger"],
    "country/TCD": ["Republic of Chad"],
    "country/SDN": ["Republic of the Sudan"],
    "country/SSD": ["Republic of South Sudan"],
    "country/SOM": ["Federal Republic of Somalia"],
    "country/ERI": ["State of Eritrea"],
    "country/DJI": ["Republic of Djibouti"],
    "country/MDG": ["Republic of Madagascar"],
    "country/MOZ": ["Republic of Mozambique"],
    "country/AGO": ["Republic of Angola"],
    "country/BWA": ["Republic of Botswana"],
    "country/NAM": ["Republic of Namibia"],
    "country/LSO": ["Kingdom of Lesotho"],
    "country/SWZ": ["Kingdom of Eswatini", "Swaziland"],
    "country/MWI": ["Republic of Malawi"],
    "country/COM": ["Union of the Comoros"],
    "country/MUS": ["Republic of Mauritius"],
    "country/SYC": ["Republic of Seychelles"],
    "country/CPV": ["Republic of Cabo Verde"],
    "country/STP": ["Democratic Republic of São Tomé and Príncipe"],
    "country/GNB": ["Republic of Guinea-Bissau"],
    "country/GIN": ["Republic of Guinea"],
    "country/SLE": ["Republic of Sierra Leone"],
    "country/LBR": ["Republic of Liberia"],
    "country/MRT": ["Islamic Republic of Mauritania"],
    "country/MAR": ["Kingdom of Morocco"],
    "country/DZA": ["People's Democratic Republic of Algeria"],
    "country/TUN": ["Republic of Tunisia"],
    "country/LBY": ["State of Libya"],
    "country/MLT": ["Republic of Malta"],
    "country/CYP": ["Republic of Cyprus"],
    "country/ALB": ["Republic of Albania"],
    "country/BIH": ["Bosnia and Herzegovina"],
    "country/HRV": ["Republic of Croatia"],
    "country/MNE": ["Montenegro"],
    "country/SRB": ["Republic of Serbia"],
    "country/MKD": ["Republic of North Macedonia"],
    "country/BGR": ["Republic of Bulgaria"],
    "country/ROU": ["Romania"],
    "country/MDA": ["Republic of Moldova"],
    "country/BLR": ["Republic of Belarus"],
    "country/LTU": ["Republic of Lithuania"],
    "country/LVA": ["Republic of Latvia"],
    "country/EST": ["Republic of Estonia"],
    "country/ISL": ["Republic of Iceland"],
    "country/FRO": ["Faroe Islands"],
    "country/GRL": ["Greenland"],
    "country/SJM": ["Svalbard and Jan Mayen"],
    "country/KAZ": ["Kazakhstan", "Republic of Kazakhstan"],
    "country/KGZ": ["Kyrgyzstan", "Kyrgyz Republic"],
    "country/TJK": ["Tajikistan", "Republic of Tajikistan"],
    "country/TKM": ["Turkmenistan"],
    "country/UZB": ["Uzbekistan", "Republic of Uzbekistan"],
    "country/AFG": ["Afghanistan", "Islamic Republic of Afghanistan"],
    "country/PAK": ["Islamic Republic of Pakistan"],
    "country/NPL": ["Nepal", "Federal Democratic Republic of Nepal"],
    "country/BTN": ["Bhutan", "Kingdom of Bhutan"],
    "country/MMR": ["Myanmar", "Burma", "Republic of the Union of Myanmar"],
    "country/LAO": ["Laos", "Lao People's Democratic Republic"],
    "country/KHM": ["Cambodia", "Kingdom of Cambodia"],
    "country/MNG": ["Mongolia"],
    "country/TWN": ["Taiwan", "Republic of China"],
    "country/HKG": ["Hong Kong", "Hong Kong Special Administrative Region"],
    "country/MAC": ["Macau", "Macao Special Administrative Region"],
    "country/PLW": ["Palau", "Republic of Palau"],
    "country/PNG": ["Independent State of Papua New Guinea"],
    "country/SLB": ["Solomon Islands"],
    "country/VUT": ["Republic of Vanuatu"],
    "country/FJI": ["Republic of Fiji"],
    "country/TON": ["Kingdom of Tonga"],
    "country/WSM": ["Independent State of Samoa"],
    "country/TUV": ["Tuvalu"],
    "country/KIR": ["Republic of Kiribati"],
    "country/NRU": ["Republic of Nauru"],
    "country/NIU": ["Niue"],
    "country/COK": ["Cook Islands"],
    "country/TKL": ["Tokelau"],
    "country/WLF": ["Wallis and Futuna"],
    "country/NCL": ["New Caledonia"],
    "country/PYF": ["French Polynesia"],
    "country/PCN": ["Pitcairn Islands"],
    "country/FLK": ["Falkland Islands"],
    "country/SGS": ["South Georgia and the South Sandwich Islands"],
    "country/HMD": ["Heard Island and McDonald Islands"],
    "country/IOT": ["British Indian Ocean Territory"],
    "country/ATF": ["French Southern Territories"],
    "country/BVT": ["Bouvet Island"],
    "country/ATA": ["Antarctica"],
    "country/ATB": ["British Antarctic Territory"],
    "country/UMI": ["U.S. Minor Outlying Islands"],
    "country/CXR": ["Christmas Island"],
    "country/CCK": ["Cocos (Keeling) Islands"],
    "country/NFK": ["Norfolk Island"],
    "country/AIA": ["Anguilla"],
    "country/BMU": ["Bermuda"],
    "country/VGB": ["British Virgin Islands"],
    "country/CYM": ["Cayman Islands"],
    "country/FLK": ["Falkland Islands"],
    "country/GIB": ["Gibraltar"],
    "country/GRL": ["Greenland"],
    "country/GLP": ["Guadeloupe"],
    "country/GUF": ["French Guiana"],
    "country/MTQ": ["Martinique"],
    "country/MYT": ["Mayotte"],
    "country/MSR": ["Montserrat"],
    "country/REU": ["Réunion"],
    "country/SHN": ["Saint Helena"],
    "country/MAF": ["Saint Martin"],
    "country/SPM": ["Saint Pierre and Miquelon"],
    "country/SXM": ["Sint Maarten"],
    "country/TCA": ["Turks and Caicos Islands"],
    "country/VIR": ["U.S. Virgin Islands"],
    "country/ALA": ["Åland Islands"],
    "country/BES": ["Bonaire, Sint Eustatius and Saba"],
    "country/BLM": ["Saint Barthélemy"],
    "country/CUW": ["Curaçao"],
    "country/GGY": ["Guernsey"],
    "country/IMN": ["Isle of Man"],
    "country/JEY": ["Jersey"],
    "country/MCO": ["Monaco"],
    "country/SMR": ["San Marino"],
    "country/VAT": ["Vatican City", "Holy See"],
    "wikidataId/Q130340667": ["Arab League"],
    "wikidataId/Q23681": ["Central America"],
    "wikidataId/Q244165": ["Benelux"],
    "wikidataId/Q29999": ["Kingdom of the Netherlands"],
    "wikidataId/Q31354462": ["African Union"],
    "wikidataId/Q40362": ["Melanesia"],
    "wikidataId/Q756617": ["Polynesia"],
}

all_dcids = set()

# Collect DCIDs from all sitemap files
sitemap_files = glob.glob(os.path.join(SITEMAP_BASE_DIR, '*.0.txt'))
for sitemap_file in sitemap_files:
    with open(sitemap_file, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith("https://datacommons.org/place/"):
                all_dcids.add(line.split('https://datacommons.org/place/')[-1])

# Convert set to list for API call
all_dcids_list = list(all_dcids)

# Initialize maps for names, types, and containedInPlace
names_map = {}
types_map = {}
contained_in_place_map = {}

# Chunk size for API calls and delay
CHUNK_SIZE = 500
DELAY_SECONDS = 1

# Fetch names and types for all collected DCIDs with chunking and error handling
for i in range(0, len(all_dcids_list), CHUNK_SIZE):
    chunk = all_dcids_list[i:i + CHUNK_SIZE]
    try:
        chunk_names = dc.get_property_values(chunk, 'name')
        chunk_types = dc.get_property_values(chunk, 'typeOf')
        chunk_contained_in = dc.get_property_values(chunk, 'containedInPlace')

        names_map.update(chunk_names)
        types_map.update(chunk_types)
        contained_in_place_map.update(chunk_contained_in)

    except Exception as e:
        print(f"Warning: Data Commons API call failed for chunk {i}-{i+len(chunk)-1}: {e}. Using fallback names and types for this chunk.")
    time.sleep(DELAY_SECONDS) # Add a delay to prevent rate limiting

# Collect all unique containedInPlace DCIDs to fetch their names
all_contained_in_dcids = set()
for dcid_list in contained_in_place_map.values():
    for dcid_item in dcid_list:
        all_contained_in_dcids.add(dcid_item)

all_contained_in_dcids_list = list(all_contained_in_dcids)
contained_in_names_map = {}

# Fetch names for all unique containedInPlace DCIDs
for i in range(0, len(all_contained_in_dcids_list), CHUNK_SIZE):
    chunk = all_contained_in_dcids_list[i:i + CHUNK_SIZE]
    try:
        chunk_names = dc.get_property_values(chunk, 'name')
        contained_in_names_map.update(chunk_names)
    except Exception as e:
        print(f"Warning: Data Commons API call failed for containedInPlace names chunk {i}-{i+len(chunk)-1}: {e}. Using fallback names for this chunk.")
    time.sleep(DELAY_SECONDS)

updated_lines = []
for dcid in all_dcids_list:
    # Robust fallback for name
    name_list = names_map.get(dcid)
    if name_list and name_list[0]:
        name = name_list[0]
    else:
        name = dcid.split('/')[-1]

    # Robust fallback for place_type
    type_list = types_map.get(dcid)
    if type_list and type_list[0]:
        place_type = type_list[0]
    else:
        place_type = "Unknown"

    # Get alternative names from the map (no automatic DCID addition)
    current_alternative_names = list(alternative_names_map.get(dcid, []))

    # Get containedInPlace names
    contained_in_places_dcids = contained_in_place_map.get(dcid, [])
    contained_in_place_names = []
    for contained_dcid in contained_in_places_dcids:
        contained_name_list = contained_in_names_map.get(contained_dcid)
        if contained_name_list and contained_name_list[0]:
            contained_in_place_names.append(contained_name_list[0])
        else:
            contained_in_place_names.append(contained_dcid.split('/')[-1])


    json_object = {
        "dcid": dcid,
        "name": name,
        "type": place_type,
        "alternativeNames": current_alternative_names,
        "containedInPlace": contained_in_place_names
    }

    # Output the JSON object directly as requested
    updated_lines.append(json.dumps(json_object) + '\n')

# Write the updated content to the final import file
with open('/Users/gmechali/Desktop/datacommons/website/places_for_import.jsonl', 'w') as f:
    f.writelines(updated_lines)

print("Successfully created places_for_import.jsonl with comprehensive place data (top-level fields).")