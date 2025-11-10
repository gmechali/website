import json

# Read the existing JSONL file
with open('/Users/gmechali/Desktop/datacommons/website/places.jsonl', 'r') as f:
    lines = f.readlines()

updated_lines = []
for line in lines:
    data = json.loads(line)
    dcid = data['dcid']
    name = data['name']
    alternative_names = set(data.get('alternativeNames', []))

    # Add more alternative names based on common knowledge
    if dcid == "country/USA":
        alternative_names.update(["United States", "America", "US", "U.S."])
    elif dcid == "country/GBR":
        alternative_names.update(["Great Britain", "UK", "Britain", "United Kingdom of Great Britain and Northern Ireland"])
    elif dcid == "country/CHN":
        alternative_names.update(["China", "People's Republic of China", "PRC"])
    elif dcid == "country/IND":
        alternative_names.update(["India", "Bharat"])
    elif dcid == "country/CAN":
        alternative_names.update(["Canada"])
    elif dcid == "country/AUS":
        alternative_names.update(["Australia"])
    elif dcid == "country/DEU":
        alternative_names.update(["Germany", "Federal Republic of Germany"])
    elif dcid == "country/FRA":
        alternative_names.update(["France", "French Republic"])
    elif dcid == "country/JPN":
        alternative_names.update(["Japan"])
    elif dcid == "country/BRA":
        alternative_names.update(["Brazil", "Federative Republic of Brazil"])
    elif dcid == "country/RUS":
        alternative_names.update(["Russia", "Russian Federation"])
    elif dcid == "country/MEX":
        alternative_names.update(["Mexico", "United Mexican States"])
    elif dcid == "country/KOR":
        alternative_names.update(["South Korea", "Republic of Korea"])
    elif dcid == "country/PRK":
        alternative_names.update(["North Korea", "Democratic People's Republic of Korea"])
    elif dcid == "country/EGY":
        alternative_names.update(["Egypt", "Arab Republic of Egypt"])
    elif dcid == "country/ZAF":
        alternative_names.update(["South Africa", "Republic of South Africa"])
    elif dcid == "country/NLD":
        alternative_names.update(["Netherlands", "Holland"])
    elif dcid == "country/ITA":
        alternative_names.update(["Italy", "Italian Republic"])
    elif dcid == "country/ESP":
        alternative_names.update(["Spain", "Kingdom of Spain"])
    elif dcid == "country/SWE":
        alternative_names.update(["Sweden", "Kingdom of Sweden"])
    elif dcid == "country/NOR":
        alternative_names.update(["Norway", "Kingdom of Norway"])
    elif dcid == "country/DNK":
        alternative_names.update(["Denmark", "Kingdom of Denmark"])
    elif dcid == "country/FIN":
        alternative_names.update(["Finland", "Republic of Finland"])
    elif dcid == "country/IRL":
        alternative_names.update(["Ireland", "Republic of Ireland", "Éire"])
    elif dcid == "country/NZL":
        alternative_names.update(["New Zealand", "Aotearoa"])
    elif dcid == "country/AUT":
        alternative_names.update(["Austria", "Republic of Austria"])
    elif dcid == "country/BEL":
        alternative_names.update(["Belgium", "Kingdom of Belgium"])
    elif dcid == "country/GRC":
        alternative_names.update(["Greece", "Hellenic Republic"])
    elif dcid == "country/PRT":
        alternative_names.update(["Portugal", "Portuguese Republic"])
    elif dcid == "country/CHE":
        alternative_names.update(["Switzerland", "Swiss Confederation"])
    elif dcid == "country/TUR":
        alternative_names.update(["Turkey", "Republic of Turkey"])
    elif dcid == "country/UKR":
        alternative_names.update(["Ukraine"])
    elif dcid == "country/POL":
        alternative_names.update(["Poland", "Republic of Poland"])
    elif dcid == "country/ARG":
        alternative_names.update(["Argentina", "Argentine Republic"])
    elif dcid == "country/CHL":
        alternative_names.update(["Chile", "Republic of Chile"])
    elif dcid == "country/COL":
        alternative_names.update(["Colombia", "Republic of Colombia"])
    elif dcid == "country/PER":
        alternative_names.update(["Peru", "Republic of Peru"])
    elif dcid == "country/VEN":
        alternative_names.update(["Venezuela", "Bolivarian Republic of Venezuela"])
    elif dcid == "country/SAU":
        alternative_names.update(["Saudi Arabia", "Kingdom of Saudi Arabia"])
    elif dcid == "country/ISR":
        alternative_names.update(["Israel", "State of Israel"])
    elif dcid == "country/IRN":
        alternative_names.update(["Iran", "Islamic Republic of Iran", "Persia"])
    elif dcid == "country/IRQ":
        alternative_names.update(["Iraq", "Republic of Iraq"])
    elif dcid == "country/SYR":
        alternative_names.update(["Syria", "Syrian Arab Republic"])
    elif dcid == "country/LBN":
        alternative_names.update(["Lebanon", "Lebanese Republic"])
    elif dcid == "country/JOR":
        alternative_names.update(["Jordan", "Hashemite Kingdom of Jordan"])
    elif dcid == "country/KWT":
        alternative_names.update(["Kuwait", "State of Kuwait"])
    elif dcid == "country/QAT":
        alternative_names.update(["Qatar", "State of Qatar"])
    elif dcid == "country/BHR":
        alternative_names.update(["Bahrain", "Kingdom of Bahrain"])
    elif dcid == "country/OMN":
        alternative_names.update(["Oman", "Sultanate of Oman"])
    elif dcid == "country/YEM":
        alternative_names.update(["Yemen", "Republic of Yemen"])
    elif dcid == "country/PAK":
        alternative_names.update(["Pakistan", "Islamic Republic of Pakistan"])
    elif dcid == "country/BGD":
        alternative_names.update(["Bangladesh", "People's Republic of Bangladesh"])
    elif dcid == "country/THA":
        alternative_names.update(["Thailand", "Kingdom of Thailand", "Siam"])
    elif dcid == "country/VNM":
        alternative_names.update(["Vietnam", "Socialist Republic of Vietnam"])
    elif dcid == "country/IDN":
        alternative_names.update(["Indonesia", "Republic of Indonesia"])
    elif dcid == "country/PHL":
        alternative_names.update(["Philippines", "Republic of the Philippines"])
    elif dcid == "country/MYS":
        alternative_names.update(["Malaysia"])
    elif dcid == "country/SGP":
        alternative_names.update(["Singapore", "Republic of Singapore"])
    elif dcid == "country/CAF":
        alternative_names.update(["Central African Republic", "CAR"])
    elif dcid == "country/COD":
        alternative_names.update(["Congo (DRC)", "Democratic Republic of the Congo"])
    elif dcid == "country/COG":
        alternative_names.update(["Congo (Republic)", "Republic of the Congo"])
    elif dcid == "country/ETH":
        alternative_names.update(["Ethiopia", "Federal Democratic Republic of Ethiopia"])
    elif dcid == "country/KEN":
        alternative_names.update(["Kenya", "Republic of Kenya"])
    elif dcid == "country/NGA":
        alternative_names.update(["Nigeria", "Federal Republic of Nigeria"])
    elif dcid == "country/UGA":
        alternative_names.update(["Uganda", "Republic of Uganda"])
    elif dcid == "country/TZA":
        alternative_names.update(["Tanzania", "United Republic of Tanzania"])
    elif dcid == "country/ZMB":
        alternative_names.update(["Zambia", "Republic of Zambia"])
    elif dcid == "country/ZWE":
        alternative_names.update(["Zimbabwe", "Republic of Zimbabwe"])
    elif dcid == "country/GHA":
        alternative_names.update(["Ghana", "Republic of Ghana"])
    elif dcid == "country/CIV":
        alternative_names.update(["Ivory Coast", "Côte d'Ivoire"])
    elif dcid == "country/SEN":
        alternative_names.update(["Senegal", "Republic of Senegal"])
    elif dcid == "country/MLI":
        alternative_names.update(["Mali", "Republic of Mali"])
    elif dcid == "country/NER":
        alternative_names.update(["Niger", "Republic of Niger"])
    elif dcid == "country/TCD":
        alternative_names.update(["Chad", "Republic of Chad"])
    elif dcid == "country/SDN":
        alternative_names.update(["Sudan", "Republic of the Sudan"])
    elif dcid == "country/SSD":
        alternative_names.update(["South Sudan", "Republic of South Sudan"])
    elif dcid == "country/SOM":
        alternative_names.update(["Somalia", "Federal Republic of Somalia"])
    elif dcid == "country/ERI":
        alternative_names.update(["Eritrea", "State of Eritrea"])
    elif dcid == "country/DJI":
        alternative_names.update(["Djibouti", "Republic of Djibouti"])
    elif dcid == "country/MDG":
        alternative_names.update(["Madagascar", "Republic of Madagascar"])
    elif dcid == "country/MOZ":
        alternative_names.update(["Mozambique", "Republic of Mozambique"])
    elif dcid == "country/AGO":
        alternative_names.update(["Angola", "Republic of Angola"])
    elif dcid == "country/BWA":
        alternative_names.update(["Botswana", "Republic of Botswana"])
    elif dcid == "country/NAM":
        alternative_names.update(["Namibia", "Republic of Namibia"])
    elif dcid == "country/LSO":
        alternative_names.update(["Lesotho", "Kingdom of Lesotho"])
    elif dcid == "country/SWZ":
        alternative_names.update(["Eswatini", "Kingdom of Eswatini", "Swaziland"])
    elif dcid == "country/MWI":
        alternative_names.update(["Malawi", "Republic of Malawi"])
    elif dcid == "country/COM":
        alternative_names.update(["Comoros", "Union of the Comoros"])
    elif dcid == "country/MUS":
        alternative_names.update(["Mauritius", "Republic of Mauritius"])
    elif dcid == "country/SYC":
        alternative_names.update(["Seychelles", "Republic of Seychelles"])
    elif dcid == "country/CPV":
        alternative_names.update(["Cape Verde", "Republic of Cabo Verde"])
    elif dcid == "country/STP":
        alternative_names.update(["Sao Tome and Principe", "Democratic Republic of São Tomé and Príncipe"])
    elif dcid == "country/GNB":
        alternative_names.update(["Guinea-Bissau", "Republic of Guinea-Bissau"])
    elif dcid == "country/GIN":
        alternative_names.update(["Guinea", "Republic of Guinea"])
    elif dcid == "country/SLE":
        alternative_names.update(["Sierra Leone", "Republic of Sierra Leone"])
    elif dcid == "country/LBR":
        alternative_names.update(["Liberia", "Republic of Liberia"])
    elif dcid == "country/MRT":
        alternative_names.update(["Mauritania", "Islamic Republic of Mauritania"])
    elif dcid == "country/ESH":
        alternative_names.update(["Western Sahara", "Sahrawi Arab Democratic Republic"])
    elif dcid == "country/MAR":
        alternative_names.update(["Morocco", "Kingdom of Morocco"])
    elif dcid == "country/DZA":
        alternative_names.update(["Algeria", "People's Democratic Republic of Algeria"])
    elif dcid == "country/TUN":
        alternative_names.update(["Tunisia", "Republic of Tunisia"])
    elif dcid == "country/LBY":
        alternative_names.update(["Libya", "State of Libya"])
    elif dcid == "country/MLT":
        alternative_names.update(["Malta", "Republic of Malta"])
    elif dcid == "country/CYP":
        alternative_names.update(["Cyprus", "Republic of Cyprus"])
    elif dcid == "country/ALB":
        alternative_names.update(["Albania", "Republic of Albania"])
    elif dcid == "country/BIH":
        alternative_names.update(["Bosnia and Herzegovina"])
    elif dcid == "country/HRV":
        alternative_names.update(["Croatia", "Republic of Croatia"])
    elif dcid == "country/MNE":
        alternative_names.update(["Montenegro"])
    elif dcid == "country/SRB":
        alternative_names.update(["Serbia", "Republic of Serbia"])
    elif dcid == "country/MKD":
        alternative_names.update(["North Macedonia", "Republic of North Macedonia"])
    elif dcid == "country/BGR":
        alternative_names.update(["Bulgaria", "Republic of Bulgaria"])
    elif dcid == "country/ROU":
        alternative_names.update(["Romania"])
    elif dcid == "country/MDA":
        alternative_names.update(["Moldova", "Republic of Moldova"])
    elif dcid == "country/BLR":
        alternative_names.update(["Belarus", "Republic of Belarus"])
    elif dcid == "country/LTU":
        alternative_names.update(["Lithuania", "Republic of Lithuania"])
    elif dcid == "country/LVA":
        alternative_names.update(["Latvia", "Republic of Latvia"])
    elif dcid == "country/EST":
        alternative_names.update(["Estonia", "Republic of Estonia"])
    elif dcid == "country/ISL":
        alternative_names.update(["Iceland", "Republic of Iceland"])
    elif dcid == "country/FRO":
        alternative_names.update(["Faroe Islands"])
    elif dcid == "country/GRL":
        alternative_names.update(["Greenland"])
    elif dcid == "country/SJM":
        alternative_names.update(["Svalbard and Jan Mayen"])
    elif dcid == "country/KAZ":
        alternative_names.update(["Kazakhstan", "Republic of Kazakhstan"])
    elif dcid == "country/KGZ":
        alternative_names.update(["Kyrgyzstan", "Kyrgyz Republic"])
    elif dcid == "country/TJK":
        alternative_names.update(["Tajikistan", "Republic of Tajikistan"])
    elif dcid == "country/TKM":
        alternative_names.update(["Turkmenistan"])
    elif dcid == "country/UZB":
        alternative_names.update(["Uzbekistan", "Republic of Uzbekistan"])
    elif dcid == "country/AFG":
        alternative_names.update(["Afghanistan", "Islamic Republic of Afghanistan"])
    elif dcid == "country/PAK":
        alternative_names.update(["Pakistan", "Islamic Republic of Pakistan"])
    elif dcid == "country/NPL":
        alternative_names.update(["Nepal", "Federal Democratic Republic of Nepal"])
    elif dcid == "country/BTN":
        alternative_names.update(["Bhutan", "Kingdom of Bhutan"])
    elif dcid == "country/MMR":
        alternative_names.update(["Myanmar", "Burma", "Republic of the Union of Myanmar"])
    elif dcid == "country/LAO":
        alternative_names.update(["Laos", "Lao People's Democratic Republic"])
    elif dcid == "country/KHM":
        alternative_names.update(["Cambodia", "Kingdom of Cambodia"])
    elif dcid == "country/MNG":
        alternative_names.update(["Mongolia"])
    elif dcid == "country/TWN":
        alternative_names.update(["Taiwan", "Republic of China"])
    elif dcid == "country/HKG":
        alternative_names.update(["Hong Kong", "Hong Kong Special Administrative Region"])
    elif dcid == "country/MAC":
        alternative_names.update(["Macau", "Macao Special Administrative Region"])
    elif dcid == "country/PRK":
        alternative_names.update(["North Korea", "Democratic People's Republic of Korea", "DPRK"])
    elif dcid == "country/KOR":
        alternative_names.update(["South Korea", "Republic of Korea", "ROK"])
    elif dcid == "country/JPN":
        alternative_names.update(["Japan"])
    elif dcid == "country/FSM":
        alternative_names.update(["Federated States of Micronesia"])
    elif dcid == "country/MHL":
        alternative_names.update(["Marshall Islands", "Republic of the Marshall Islands"])
    elif dcid == "country/PLW":
        alternative_names.update(["Palau", "Republic of Palau"])
    elif dcid == "country/PNG":
        alternative_names.update(["Papua New Guinea", "Independent State of Papua New Guinea"])
    elif dcid == "country/SLB":
        alternative_names.update(["Solomon Islands"])
    elif dcid == "country/VUT":
        alternative_names.update(["Vanuatu", "Republic of Vanuatu"])
    elif dcid == "country/FJI":
        alternative_names.update(["Fiji", "Republic of Fiji"])
    elif dcid == "country/TON":
        alternative_names.update(["Tonga", "Kingdom of Tonga"])
    elif dcid == "country/WSM":
        alternative_names.update(["Samoa", "Independent State of Samoa"])
    elif dcid == "country/TUV":
        alternative_names.update(["Tuvalu"])
    elif dcid == "country/KIR":
        alternative_names.update(["Kiribati", "Republic of Kiribati"])
    elif dcid == "country/NRU":
        alternative_names.update(["Nauru", "Republic of Nauru"])
    elif dcid == "country/NIU":
        alternative_names.update(["Niue"])
    elif dcid == "country/COK":
        alternative_names.update(["Cook Islands"])
    elif dcid == "country/TKL":
        alternative_names.update(["Tokelau"])
    elif dcid == "country/WLF":
        alternative_names.update(["Wallis and Futuna"])
    elif dcid == "country/NCL":
        alternative_names.update(["New Caledonia"])
    elif dcid == "country/PYF":
        alternative_names.update(["French Polynesia"])
    elif dcid == "country/PCN":
        alternative_names.update(["Pitcairn Islands"])
    elif dcid == "country/FLK":
        alternative_names.update(["Falkland Islands"])
    elif dcid == "country/SGS":
        alternative_names.update(["South Georgia and the South Sandwich Islands"])
    elif dcid == "country/HMD":
        alternative_names.update(["Heard Island and McDonald Islands"])
    elif dcid == "country/IOT":
        alternative_names.update(["British Indian Ocean Territory"])
    elif dcid == "country/ATF":
        alternative_names.update(["French Southern Territories"])
    elif dcid == "country/BVT":
        alternative_names.update(["Bouvet Island"])
    elif dcid == "country/ATA":
        alternative_names.update(["Antarctica"])
    elif dcid == "country/ATB":
        alternative_names.update(["British Antarctic Territory"])
    elif dcid == "country/UMI":
        alternative_names.update(["U.S. Minor Outlying Islands"])
    elif dcid == "country/CXR":
        alternative_names.update(["Christmas Island"])
    elif dcid == "country/CCK":
        alternative_names.update(["Cocos (Keeling) Islands"])
    elif dcid == "country/NFK":
        alternative_names.update(["Norfolk Island"])
    elif dcid == "country/AIA":
        alternative_names.update(["Anguilla"])
    elif dcid == "country/BMU":
        alternative_names.update(["Bermuda"])
    elif dcid == "country/VGB":
        alternative_names.update(["British Virgin Islands"])
    elif dcid == "country/CYM":
        alternative_names.update(["Cayman Islands"])
    elif dcid == "country/FLK":
        alternative_names.update(["Falkland Islands"])
    elif dcid == "country/GIB":
        alternative_names.update(["Gibraltar"])
    elif dcid == "country/GRL":
        alternative_names.update(["Greenland"])
    elif dcid == "country/GLP":
        alternative_names.update(["Guadeloupe"])
    elif dcid == "country/GUF":
        alternative_names.update(["French Guiana"])
    elif dcid == "country/MTQ":
        alternative_names.update(["Martinique"])
    elif dcid == "country/MYT":
        alternative_names.update(["Mayotte"])
    elif dcid == "country/MSR":
        alternative_names.update(["Montserrat"])
    elif dcid == "country/REU":
        alternative_names.update(["Réunion"])
    elif dcid == "country/SHN":
        alternative_names.update(["Saint Helena"])
    elif dcid == "country/MAF":
        alternative_names.update(["Saint Martin"])
    elif dcid == "country/SPM":
        alternative_names.update(["Saint Pierre and Miquelon"])
    elif dcid == "country/SXM":
        alternative_names.update(["Sint Maarten"])
    elif dcid == "country/TCA":
        alternative_names.update(["Turks and Caicos Islands"])
    elif dcid == "country/VIR":
        alternative_names.update(["U.S. Virgin Islands"])
    elif dcid == "country/ALA":
        alternative_names.update(["Åland Islands"])
    elif dcid == "country/BES":
        alternative_names.update(["Bonaire, Sint Eustatius and Saba"])
    elif dcid == "country/BLM":
        alternative_names.update(["Saint Barthélemy"])
    elif dcid == "country/CUW":
        alternative_names.update(["Curaçao"])
    elif dcid == "country/GGY":
        alternative_names.update(["Guernsey"])
    elif dcid == "country/IMN":
        alternative_names.update(["Isle of Man"])
    elif dcid == "country/JEY":
        alternative_names.update(["Jersey"])
    elif dcid == "country/MCO":
        alternative_names.update(["Monaco"])
    elif dcid == "country/SMR":
        alternative_names.update(["San Marino"])
    elif dcid == "country/VAT":
        alternative_names.update(["Vatican City", "Holy See"])
    elif dcid == "country/XKS":
        alternative_names.update(["Kosovo", "Republic of Kosovo"])
    elif dcid == "wikidataId/Q130340667":
        alternative_names.update(["Arab League"])
    elif dcid == "wikidataId/Q23681":
        alternative_names.update(["Central America"])
    elif dcid == "wikidataId/Q244165":
        alternative_names.update(["Benelux"])
    elif dcid == "wikidataId/Q29999":
        alternative_names.update(["Kingdom of the Netherlands"])
    elif dcid == "wikidataId/Q31354462":
        alternative_names.update(["African Union"])
    elif dcid == "wikidataId/Q40362":
        alternative_names.update(["Melanesia"])
    elif dcid == "wikidataId/Q756617":
        alternative_names.update(["Polynesia"])

    data['alternativeNames'] = list(alternative_names)
    updated_lines.append(json.dumps(data) + '\n')

# Write the updated content back to the file
with open('/Users/gmechali/Desktop/datacommons/website/places.jsonl', 'w') as f:
    f.writelines(updated_lines)

print("Successfully updated places.jsonl with more alternative names.")
