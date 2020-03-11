#!/usr/bin/python3.7
from argparse import ArgumentParser
import os
from ast import literal_eval


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-m',
                        '--masscan',
                        dest='ip_range',
                        required=True,
                        help='Specify an IP address, an IP range '
                             'or a new-line separated file with IP addresses/networks to scan for the cameras.')
    parser.add_argument('-o',
                        '--output',
                        dest='output',
                        default='cameras.txt',
                        required=False,
                        help='Optional. The output file with discovered cameras')
    options = parser.parse_args()
    return options


def do_masscan(ip_range):
    import subprocess

    masscan_result_file = 'masscan.json'
    port = '554'
    rate = 10000000  # we will scan on the maximum speed

    if os.path.exists(ip_range):
        ip_range = f'-iL {ip_range}'

    command = f'masscan {ip_range} -p{port} -oJ ./{masscan_result_file} --rate {rate}'
    try:
        subprocess.check_call(command.split(' '))
        print('Masscan has finished')
        return masscan_result_file
    except Exception as e:
        print(f'Unexpected error during the masscan: {e}')


def convert(input_file):
    url_to_cameras = []
    masscan_results = []
    try:
        with open(input_file, 'r') as f:
            masscan_results = [res.strip() for res in f.readlines() if 'ip' in res]
    except Exception as e:
        print(f'Unexpected error while reading the masscan results: {e}')
        exit(1)
    for target in masscan_results:
        if 'finished' in target:
            continue
        if target.endswith(','):
            target = target[:-1]
        res = literal_eval(target)
        for port in res["ports"]:
            address = f'rtsp://{res["ip"]}:{port["port"]}'
            url_to_cameras.append(address)
    return url_to_cameras


def save(url_to_cameras, output_file):
    with open(output_file, 'w') as f:
        print('\n'.join(url_to_cameras), file=f)
    print(f'{len(url_to_cameras)} cameras have been saved into {output_file}')


options = get_arguments()
result_file = do_masscan(options.ip_range)
if not result_file:
    print('Masscan has failed to get the cameras')
    exit(1)
addresses = convert(result_file)
save(addresses, options.output)
