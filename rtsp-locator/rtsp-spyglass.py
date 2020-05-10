#!/usr/bin/env python3
from time import sleep
from os import system
import requests
import os

def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--import-endpoint',
                        dest='import_endpoint',
                        required=True,
                        help='An URL to the import service of the backend API. ')
    parser.add_argument('--country-code',
                        dest='country_code',
                        required=False,
                        help='A country code to use while searching for the exposed cameras. '
                             'If this argument is omitted, then script scans all existing country codes.')
    parser.add_argument('--shodan-api-key',
                        dest='shodan_api_key',
                        required=False,
                        help='A Shodan api-key to perform requests vid Shodan Search Engine '
                             'instead of the blind Internet scanning')

    return parser.parse_args()


options = get_arguments()
COUNTRIES = [{
    "country_code": "AF",
    "country_name": "Afghanistan"
},
    {
        "country_code": "AL",
        "country_name": "Albania"
    },
    {
        "country_code": "DZ",
        "country_name": "Algeria"
    },
    {
        "country_code": "AS",
        "country_name": "American Samoa"
    },
    {
        "country_code": "AD",
        "country_name": "Andorra"
    },
    {
        "country_code": "AO",
        "country_name": "Angola"
    },
    {
        "country_code": "AI",
        "country_name": "Anguilla"
    },
    {
        "country_code": "AQ",
        "country_name": "Antarctica"
    },
    {
        "country_code": "AG",
        "country_name": "Antigua and Barbuda"
    },
    {
        "country_code": "AR",
        "country_name": "Argentina"
    },
    {
        "country_code": "AM",
        "country_name": "Armenia"
    },
    {
        "country_code": "AW",
        "country_name": "Aruba"
    },
    {
        "country_code": "AU",
        "country_name": "Australia"
    },
    {
        "country_code": "AT",
        "country_name": "Austria"
    },
    {
        "country_code": "AZ",
        "country_name": "Azerbaijan"
    },
    {
        "country_code": "BS",
        "country_name": "Bahamas"
    },
    {
        "country_code": "BH",
        "country_name": "Bahrain"
    },
    {
        "country_code": "BD",
        "country_name": "Bangladesh"
    },
    {
        "country_code": "BB",
        "country_name": "Barbados"
    },
    {
        "country_code": "BY",
        "country_name": "Belarus"
    },
    {
        "country_code": "BE",
        "country_name": "Belgium"
    },
    {
        "country_code": "BZ",
        "country_name": "Belize"
    },
    {
        "country_code": "BJ",
        "country_name": "Benin"
    },
    {
        "country_code": "BM",
        "country_name": "Bermuda"
    },
    {
        "country_code": "BT",
        "country_name": "Bhutan"
    },
    {
        "country_code": "BO",
        "country_name": "Bolivia, Plurinational State of"
    },
    {
        "country_code": "BQ",
        "country_name": "Bonaire, Sint Eustatius and Saba"
    },
    {
        "country_code": "BA",
        "country_name": "Bosnia and Herzegovina"
    },
    {
        "country_code": "BW",
        "country_name": "Botswana"
    },
    {
        "country_code": "BV",
        "country_name": "Bouvet Island"
    },
    {
        "country_code": "BR",
        "country_name": "Brazil"
    },
    {
        "country_code": "IO",
        "country_name": "British Indian Ocean Territory"
    },
    {
        "country_code": "BN",
        "country_name": "Brunei Darussalam"
    },
    {
        "country_code": "BG",
        "country_name": "Bulgaria"
    },
    {
        "country_code": "BF",
        "country_name": "Burkina Faso"
    },
    {
        "country_code": "BI",
        "country_name": "Burundi"
    },
    {
        "country_code": "KH",
        "country_name": "Cambodia"
    },
    {
        "country_code": "CM",
        "country_name": "Cameroon"
    },
    {
        "country_code": "CA",
        "country_name": "Canada"
    },
    {
        "country_code": "CV",
        "country_name": "Cape Verde"
    },
    {
        "country_code": "KY",
        "country_name": "Cayman Islands"
    },
    {
        "country_code": "CF",
        "country_name": "Central African Republic"
    },
    {
        "country_code": "TD",
        "country_name": "Chad"
    },
    {
        "country_code": "CL",
        "country_name": "Chile"
    },
    # {
    #     "country_code": "CN",
    #     "country_name": "China"
    # },
    {
        "country_code": "CX",
        "country_name": "Christmas Island"
    },
    {
        "country_code": "CC",
        "country_name": "Cocos (Keeling) Islands"
    },
    {
        "country_code": "CO",
        "country_name": "Colombia"
    },
    {
        "country_code": "KM",
        "country_name": "Comoros"
    },
    {
        "country_code": "CG",
        "country_name": "Congo"
    },
    {
        "country_code": "CD",
        "country_name": "Congo, the Democratic Republic of the"
    },
    {
        "country_code": "CK",
        "country_name": "Cook Islands"
    },
    {
        "country_code": "CR",
        "country_name": "Costa Rica"
    },
    {
        "country_code": "HR",
        "country_name": "Croatia"
    },
    {
        "country_code": "CU",
        "country_name": "Cuba"
    },
    {
        "country_code": "CY",
        "country_name": "Cyprus"
    },
    {
        "country_code": "CZ",
        "country_name": "Czech Republic"
    },
    {
        "country_code": "DK",
        "country_name": "Denmark"
    },
    {
        "country_code": "DJ",
        "country_name": "Djibouti"
    },
    {
        "country_code": "DM",
        "country_name": "Dominica"
    },
    {
        "country_code": "DO",
        "country_name": "Dominican Republic"
    },
    {
        "country_code": "EC",
        "country_name": "Ecuador"
    },
    {
        "country_code": "EG",
        "country_name": "Egypt"
    },
    {
        "country_code": "SV",
        "country_name": "El Salvador"
    },
    {
        "country_code": "GQ",
        "country_name": "Equatorial Guinea"
    },
    {
        "country_code": "ER",
        "country_name": "Eritrea"
    },
    {
        "country_code": "EE",
        "country_name": "Estonia"
    },
    {
        "country_code": "ET",
        "country_name": "Ethiopia"
    },
    {
        "country_code": "FK",
        "country_name": "Falkland Islands (Malvinas)"
    },
    {
        "country_code": "FO",
        "country_name": "Faroe Islands"
    },
    {
        "country_code": "FJ",
        "country_name": "Fiji"
    },
    {
        "country_code": "FI",
        "country_name": "Finland"
    },
    {
        "country_code": "FR",
        "country_name": "France"
    },
    {
        "country_code": "GF",
        "country_name": "French Guiana"
    },
    {
        "country_code": "PF",
        "country_name": "French Polynesia"
    },
    {
        "country_code": "TF",
        "country_name": "French Southern Territories"
    },
    {
        "country_code": "GA",
        "country_name": "Gabon"
    },
    {
        "country_code": "GM",
        "country_name": "Gambia"
    },
    {
        "country_code": "GE",
        "country_name": "Georgia"
    },
    {
        "country_code": "DE",
        "country_name": "Germany"
    },
    {
        "country_code": "GH",
        "country_name": "Ghana"
    },
    {
        "country_code": "GI",
        "country_name": "Gibraltar"
    },
    {
        "country_code": "GR",
        "country_name": "Greece"
    },
    {
        "country_code": "GL",
        "country_name": "Greenland"
    },
    {
        "country_code": "GD",
        "country_name": "Grenada"
    },
    {
        "country_code": "GP",
        "country_name": "Guadeloupe"
    },
    {
        "country_code": "GU",
        "country_name": "Guam"
    },
    {
        "country_code": "GT",
        "country_name": "Guatemala"
    },
    {
        "country_code": "GG",
        "country_name": "Guernsey"
    },
    {
        "country_code": "GN",
        "country_name": "Guinea"
    },
    {
        "country_code": "GW",
        "country_name": "Guinea-Bissau"
    },
    {
        "country_code": "GY",
        "country_name": "Guyana"
    },
    {
        "country_code": "HT",
        "country_name": "Haiti"
    },
    {
        "country_code": "HM",
        "country_name": "Heard Island and McDonald Islands"
    },
    {
        "country_code": "VA",
        "country_name": "Holy See (Vatican City State)"
    },
    {
        "country_code": "HN",
        "country_name": "Honduras"
    },
    {
        "country_code": "HK",
        "country_name": "Hong Kong"
    },
    {
        "country_code": "HU",
        "country_name": "Hungary"
    },
    {
        "country_code": "IS",
        "country_name": "Iceland"
    },
    {
        "country_code": "IN",
        "country_name": "India"
    },
    {
        "country_code": "ID",
        "country_name": "Indonesia"
    },
    # {"country_code": "IR", "country_name": "Iran, Islamic Republic of"},
    # {"country_code": "IQ", "country_name": "Iraq"},
    {
        "country_code": "IE",
        "country_name": "Ireland"
    },
    {
        "country_code": "IM",
        "country_name": "Isle of Man"
    },
    {
        "country_code": "IL",
        "country_name": "Israel"
    },
    {
        "country_code": "IT",
        "country_name": "Italy"
    },
    {
        "country_code": "JM",
        "country_name": "Jamaica"
    }, {
        "country_code": "JP",
        "country_name": "Japan"
    },
    {
        "country_code": "JE",
        "country_name": "Jersey"
    },
    {
        "country_code": "JO",
        "country_name": "Jordan"
    }, {
        "country_code": "KZ",
        "country_name": "Kazakhstan"
    },
    {
        "country_code": "KE",
        "country_name": "Kenya"
    },
    {
        "country_code": "KI",
        "country_name": "Kiribati"
    },
    {
        "country_code": "KP",
        "country_name": "Korea, Democratic People's Republic of"
    },
    {
        "country_code": "KR",
        "country_name": "Korea, Republic of"
    },
    {
        "country_code": "KW",
        "country_name": "Kuwait"
    },
    {
        "country_code": "KG",
        "country_name": "Kyrgyzstan"
    },
    {
        "country_code": "LA",
        "country_name": "Lao People's Democratic Republic"
    },
    {
        "country_code": "LV",
        "country_name": "Latvia"
    },
    {
        "country_code": "LB",
        "country_name": "Lebanon"
    },
    {
        "country_code": "LS",
        "country_name": "Lesotho"
    },
    {
        "country_code": "LR",
        "country_name": "Liberia"
    },
    {
        "country_code": "LY",
        "country_name": "Libya"
    },
    {
        "country_code": "LI",
        "country_name": "Liechtenstein"
    },
    {
        "country_code": "LT",
        "country_name": "Lithuania"
    },
    {
        "country_code": "LU",
        "country_name": "Luxembourg"
    },
    {
        "country_code": "MO",
        "country_name": "Macao"
    },
    {
        "country_code": "MK",
        "country_name": "Macedonia, the Former Yugoslav Republic of"
    },
    {
        "country_code": "MG",
        "country_name": "Madagascar"
    },
    {
        "country_code": "MW",
        "country_name": "Malawi"
    }, {
        "country_code": "MY",
        "country_name": "Malaysia"
    },
    {
        "country_code": "MV",
        "country_name": "Maldives"
    },
    {
        "country_code": "ML",
        "country_name": "Mali"
    },
    {
        "country_code": "MT",
        "country_name": "Malta"
    },
    {
        "country_code": "MH",
        "country_name": "Marshall Islands"
    },
    {
        "country_code": "MQ",
        "country_name": "Martinique"
    },
    {
        "country_code": "MR",
        "country_name": "Mauritania"
    },
    {
        "country_code": "MU",
        "country_name": "Mauritius"
    },
    {
        "country_code": "YT",
        "country_name": "Mayotte"
    },
    {
        "country_code": "MX",
        "country_name": "Mexico"
    },
    {
        "country_code": "FM",
        "country_name": "Micronesia, Federated States of"
    },
    {
        "country_code": "MD",
        "country_name": "Moldova, Republic of"
    },
    {
        "country_code": "MC",
        "country_name": "Monaco"
    },
    {
        "country_code": "MN",
        "country_name": "Mongolia"
    },
    {
        "country_code": "ME",
        "country_name": "Montenegro"
    },
    {
        "country_code": "MS",
        "country_name": "Montserrat"
    },
    {
        "country_code": "MA",
        "country_name": "Morocco"
    },
    {
        "country_code": "MZ",
        "country_name": "Mozambique"
    },
    {
        "country_code": "MM",
        "country_name": "Myanmar"
    },
    {
        "country_code": "NA",
        "country_name": "Namibia"
    },
    {
        "country_code": "NR",
        "country_name": "Nauru"
    },
    {
        "country_code": "NP",
        "country_name": "Nepal"
    },
    {
        "country_code": "NL",
        "country_name": "Netherlands"
    },
    {
        "country_code": "NC",
        "country_name": "New Caledonia"
    },
    {
        "country_code": "NZ",
        "country_name": "New Zealand"
    },
    {
        "country_code": "NI",
        "country_name": "Nicaragua"
    },
    {
        "country_code": "NE",
        "country_name": "Niger"
    },
    {
        "country_code": "NG",
        "country_name": "Nigeria"
    },
    {
        "country_code": "NU",
        "country_name": "Niue"
    },
    {
        "country_code": "NF",
        "country_name": "Norfolk Island"
    },
    {
        "country_code": "MP",
        "country_name": "Northern Mariana Islands"
    },
    {
        "country_code": "NO",
        "country_name": "Norway"
    },
    {
        "country_code": "OM",
        "country_name": "Oman"
    },
    {
        "country_code": "PK",
        "country_name": "Pakistan"
    },
    {
        "country_code": "PW",
        "country_name": "Palau"
    },
    {
        "country_code": "PS",
        "country_name": "Palestine, State of"
    },
    {
        "country_code": "PA",
        "country_name": "Panama"
    },
    {
        "country_code": "PG",
        "country_name": "Papua New Guinea"
    },
    {
        "country_code": "PY",
        "country_name": "Paraguay"
    },
    {
        "country_code": "PE",
        "country_name": "Peru"
    },
    {
        "country_code": "PH",
        "country_name": "Philippines"
    },
    {
        "country_code": "PN",
        "country_name": "Pitcairn"
    },
    {
        "country_code": "PL",
        "country_name": "Poland"
    },
    {
        "country_code": "PT",
        "country_name": "Portugal"
    },
    {
        "country_code": "PR",
        "country_name": "Puerto Rico"
    },
    {
        "country_code": "QA",
        "country_name": "Qatar"
    },
    {
        "country_code": "RE",
        "country_name": "Reunion"
    },
    {
        "country_code": "RO",
        "country_name": "Romania"
    },
    # {"country_code": "RU", "country_name": "Russian Federation"},
    {
        "country_code": "BL",
        "country_name": "Saint Bartholemy"
    },
    {
        "country_code": "SH",
        "country_name": "Saint Helena, Ascension and Tristan da Cunha"
    },
    {
        "country_code": "KN",
        "country_name": "Saint Kitts and Nevis"
    },
    {
        "country_code": "LC",
        "country_name": "Saint Lucia"
    },
    {
        "country_code": "MF",
        "country_name": "Saint Martin (French part)"
    },
    {
        "country_code": "PM",
        "country_name": "Saint Pierre and Miquelon"
    },
    {
        "country_code": "VC",
        "country_name": "Saint Vincent and the Grenadines"
    },
    {
        "country_code": "WS",
        "country_name": "Samoa"
    },
    {
        "country_code": "SM",
        "country_name": "San Marino"
    },
    {
        "country_code": "ST",
        "country_name": "Sao Tome and Principe"
    },
    {
        "country_code": "SA",
        "country_name": "Saudi Arabia"
    },
    {
        "country_code": "SN",
        "country_name": "Senegal"
    },
    {
        "country_code": "RS",
        "country_name": "Serbia"
    },
    {
        "country_code": "SC",
        "country_name": "Seychelles"
    },
    {
        "country_code": "SL",
        "country_name": "Sierra Leone"
    },
    {
        "country_code": "SG",
        "country_name": "Singapore"
    },
    {
        "country_code": "SX",
        "country_name": "Sint Maarten (Dutch part)"
    },
    {
        "country_code": "SK",
        "country_name": "Slovakia"
    },
    {
        "country_code": "SI",
        "country_name": "Slovenia"
    },
    {
        "country_code": "SB",
        "country_name": "Solomon Islands"
    },
    {
        "country_code": "SO",
        "country_name": "Somalia"
    },
    {
        "country_code": "ZA",
        "country_name": "South Africa"
    },
    {
        "country_code": "GS",
        "country_name": "South Georgia and the South Sandwich Islands"
    },
    {
        "country_code": "SS",
        "country_name": "South Sudan"
    },
    {
        "country_code": "ES",
        "country_name": "Spain"
    },
    {
        "country_code": "LK",
        "country_name": "Sri Lanka"
    },
    {
        "country_code": "SD",
        "country_name": "Sudan"
    },
    {
        "country_code": "SR",
        "country_name": "Suriname"
    },
    {
        "country_code": "SJ",
        "country_name": "Svalbard and Jan Mayen"
    },
    {
        "country_code": "SZ",
        "country_name": "Swaziland"
    },
    {
        "country_code": "SE",
        "country_name": "Sweden"
    },
    {
        "country_code": "CH",
        "country_name": "Switzerland"
    },
    {
        "country_code": "SY",
        "country_name": "Syrian Arab Republic"
    },
    {
        "country_code": "TW",
        "country_name": "Taiwan, Province of China"
    },
    {
        "country_code": "TJ",
        "country_name": "Tajikistan"
    },
    {
        "country_code": "TZ",
        "country_name": "Tanzania, United Republic of"
    },
    {
        "country_code": "TH",
        "country_name": "Thailand"
    },
    {
        "country_code": "TL",
        "country_name": "Timor-Leste"
    },
    {
        "country_code": "TG",
        "country_name": "Togo"
    },
    {
        "country_code": "TK",
        "country_name": "Tokelau"
    },
    {
        "country_code": "TO",
        "country_name": "Tonga"
    },
    {
        "country_code": "TT",
        "country_name": "Trinidad and Tobago"
    },
    {
        "country_code": "TN",
        "country_name": "Tunisia"
    },
    {
        "country_code": "TR",
        "country_name": "Turkey"
    },
    {
        "country_code": "TM",
        "country_name": "Turkmenistan"
    },
    {
        "country_code": "TC",
        "country_name": "Turks and Caicos Islands"
    },
    {
        "country_code": "TV",
        "country_name": "Tuvalu"
    },
    {
        "country_code": "UG",
        "country_name": "Uganda"
    },
    {
        "country_code": "UA",
        "country_name": "Ukraine"
    },
    {
        "country_code": "AE",
        "country_name": "United Arab Emirates"
    },
    {
        "country_code": "GB",
        "country_name": "United Kingdom"
    },
    {
        "country_code": "US",
        "country_name": "United States"
    },
    {
        "country_code": "UM",
        "country_name": "United States Minor Outlying Islands"
    },
    {
        "country_code": "UY",
        "country_name": "Uruguay"
    },
    {
        "country_code": "UZ",
        "country_name": "Uzbekistan"
    },
    {
        "country_code": "VU",
        "country_name": "Vanuatu"
    },
    {
        "country_code": "VE",
        "country_name": "Venezuela, Bolivarian Republic of"
    },
    {
        "country_code": "VN",
        "country_name": "Viet Nam"
    },
    {
        "country_code": "VG",
        "country_name": "Virgin Islands, British"
    },
    {
        "country_code": "VI",
        "country_name": "Virgin Islands, U.S."
    },
    {
        "country_code": "WF",
        "country_name": "Wallis and Futuna"
    },
    {
        "country_code": "EH",
        "country_name": "Western Sahara"
    },
    {
        "country_code": "YE",
        "country_name": "Yemen"
    },
    {
        "country_code": "ZM",
        "country_name": "Zambia"
    },
    {
        "country_code": "ZW",
        "country_name": "Zimbabwe"
    }]

print("Starting the RTSP spyglass")

import_endpoint = options.import_endpoint
print(f'Testing connection to the backend API.')
try:
    response = requests.head(import_endpoint.replace('/import', '/ids'))
except Exception as e:
    print(f'Failed to connect to the backend API: {e}')
    exit(1)
if not response.ok:
    raise Exception(f'The backend API has responded with unsuccessful status code: {response.status_code}')

print('Starting the main loop')
if options.country_code:
    filtered_countries = [country for country in COUNTRIES if
                          country['country_code'].lower() == options.country_code.lower()]
else:
    filtered_countries = COUNTRIES
print(f'Will go through {len(filtered_countries)} number of countries in searching for exposed cameras')

if options.shodan_api_key:
    shodan_api_key = options.shodan_api_key
    if ';' in shodan_api_key or '|' in shodan_api_key or '&&' in shodan_api_key or '#' in shodan_api_key:
        raise Exception("I can break rules, too. Goodbye.")
    system(f'shodan init {shodan_api_key}')
    for country in filtered_countries:
        country_name = country['country_name']
        print(f'Using Shodan Search Engine to gather cameras from {country_name}')
        country_code = country['country_code']
        system(f"shodan download {country_code} 'port:554 country:{country_code}'")
        output_file = f'{country_code}.json.gz'
        if os.path.exists(output_file):
            print('Unpacking the shodan result file')
            system(f'gunzip {output_file}')
            print('Starting the rtsp crawler to identify each camera')
            system(f'python3 -u rtsp-probe.py -bj {country_code}.json --import {import_endpoint}')
        else:
            print(f'Shodan has not created any result file for {country_name}')
else:
    print('No shodan api key was found, starting the blind Internet scan')
    for country in filtered_countries:
        country_code = country['country_code']
        print(f'Collecting IP addresses of {country_code}/{country["country_name"]}')
        system(f'python3 -u geoip2-ipv4.py --country-code {country_code}')
        with open(f'{country_code}-ips.txt', 'r') as ips_file:
            subnets = [line.strip() for line in ips_file.readlines() if line.strip()]
        for subnet in subnets:
            print(f'Scanning {subnet} to find exposed RTSP services')
            output_file = f'{country_code}-cameras.txt'
            system(f'python3 -u rtsp-masscan.py --masscan {subnet} --output {output_file}')
            system(f'python3 -u rtsp-probe.py -bl {output_file} --import {import_endpoint}')
