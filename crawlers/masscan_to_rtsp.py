#!/usr/bin/python3.7
from argparse import ArgumentParser
from ast import literal_eval


def get_arguments():
    parser = ArgumentParser()
    parser.add_argument('-m', '--masscan', dest='ip_range',
                        help='Do a masscan to get the cameras.')
    parser.add_argument('-a', '--aggressive', action='store_true',
                        help='Optional. Aggressively scan each target.')
    parser.add_argument('-f', '--file', dest='file',
                        help='Instead of doing an actual masscan, use a masscan JSON result '
                             'to parse and convert to the capable rtsp_probe format')
    parser.add_argument('-o', '--output', dest='output',
                        help='Optional. Output file with RTSP url\'s to feed into the rtsp_probe')
    options = parser.parse_args()
    if options.ip_range and options.file:
        parser.error('You can not specify a masscan and a file in the same time. Choose something.')
    if not options.file and not options.ip_range:
        parser.error('Input file or an IP range must be specified. Use --help for more info')
    if not options.output:
        options.output = 'streams.txt'
    return options


def do_masscan(ip_range, aggressive=False):
    import subprocess
    masscan_result_file = 'masscan.json'
    port = '554' if not aggressive else '80,554,443,8000,80,37777,37778,8899,34567,8091,110'
    rate = 10000000  # we will scan on the maximum speed

    command = f'masscan {ip_range} -p{port} -oJ ./{masscan_result_file} --rate {rate}'
    print('Starting a masscan')
    if ';' in command or '&' in command or '|' in command or '#' in command:
        raise Exception("I can break rules, too. Goodbye")
    try:
        subprocess.check_call(command.split(' '))
        print('Masscan successfully finished')
        return masscan_result_file
    except Exception as e:
        print(f'Unexpected error during masscan: {e}')


def convert(input_file):
    url_to_cameras = []
    masscan_results = []
    try:
        masscan_results = [res.replace('\n', '') for res in open(input_file, 'r').readlines() if 'ip' in res]
    except Exception as e:
        print(f'Unexpected error while reading masscan results: {e}')
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
    print(f'{len(url_to_cameras)} targets')
    return url_to_cameras


def save(url_to_cameras, output_file):
    if len(url_to_cameras) < 1:
        raise Exception("Input list with rtsp addresses is empty, nothing to save")
    with open(output_file, 'w') as f:
        print('\n'.join(url_to_cameras), file=f)
    print(f'Saved into {output_file}')


options = get_arguments()
result_file = options.file
if options.ip_range:
    result_file = do_masscan(options.ip_range, options.aggressive)
    if not result_file:
        print('Masscan failed')
        exit(1)
addresses = convert(result_file)
save(addresses, options.output)
