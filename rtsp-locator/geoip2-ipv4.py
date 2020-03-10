#!/usr/bin/env python3
import json
import os

import requests

DEFAULT_GEOIP2_DATASET_FILE = 'geoip2-ipv4.json'
DEFAULT_OUTPUT_FILE = 'ips.txt'


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--geoip2-ipv4',
                        dest='geoip2_ipv4',
                        default=DEFAULT_GEOIP2_DATASET_FILE,
                        required=False,
                        help='Specify an absolute path to the initial geoip2-ipv4 dataset. '
                        f'The default value is: {DEFAULT_GEOIP2_DATASET_FILE}. '
                             'If the file is not present on the system or the argument is omitted, '
                             'the script then downloads it from the datahub.io')
    parser.add_argument('--country-code',
                        dest='country_code',
                        required=False,
                        help='Specify a country code to filter out required networks.')
    parser.add_argument('--output',
                        dest='output',
                        default=DEFAULT_OUTPUT_FILE,
                        required=False,
                        help='An output file with extacted IP addresses. '
                        f'Default is {DEFAULT_OUTPUT_FILE}')
    options = parser.parse_args()

    return options


# create the extended dataset file

# first, we load the initial dataset with IP addresses
def load_geoip2_dataset(dataset_file=DEFAULT_GEOIP2_DATASET_FILE):
    if os.path.exists(DEFAULT_GEOIP2_DATASET_FILE):
        print('geoip2-ipv2 dataset is downloaded, extracting the IP addresses')
    else:
        print('Downloading the initial geoip2-ipv2 dataset')
        with open(dataset_file, 'w') as f:
            json.dump(json.loads(requests
                                 .get('https://datahub.io/core/geoip2-ipv4/r/geoip2-ipv4.json')
                                 .content),
                      f)

    with open(dataset_file, 'r') as f:
        dataset = json.loads(f.read())
    print(f'{len(dataset)} networks have been loaded')
    return dataset


options = get_arguments()
output_file = options.output
geoip2_dataset = load_geoip2_dataset(options.geoip2_ipv4)
if options.country_code:
    country_code = options.country_code
    output_file = f'{country_code}-{output_file}'
    geoip2_dataset = [row for row in geoip2_dataset if row['country_iso_code'] == country_code]

print(f'Storing {len(geoip2_dataset)} number of networks')
with open(output_file, 'w') as f:
    for line in geoip2_dataset:
        f.write(line['network'])
        f.write(os.linesep)
