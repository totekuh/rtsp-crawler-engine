#!/usr/bin/python3.7

import json
from datetime import datetime
from enum import Enum
from argparse import ArgumentParser, RawTextHelpFormatter

import cv2

DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_arguments():
    parser = ArgumentParser(formatter_class=RawTextHelpFormatter)
    parser.add_argument('-u', '--url', dest='url',
                        help='URL to rtsp stream to view. '
                             'Should be in the following format: "rtsp://115.21.242.154:554"')
    parser.add_argument('-s', '--stream', action='store_true',
                        help='Watch the continues stream from a valid camera')
    parser.add_argument('-bj', '--batch-json', dest='batch_json_file',
                        help='Provide a new-line separated file with JSON downloaded from the Shodan API '
                             '(using command: shodan download search_query) '
                             'to lookup and retrieve working streams.')
    parser.add_argument('-bl', '--batch-list', dest='batch_list_file',
                        help='Provide a new-line separated file with rtsp url\'s to perform a batch lookup. '
                             'URL should be in the following format:"rtsp://10.10.10.10:554"')
    parser.add_argument('-o', '--output', dest='output',
                        help='Optional. Output JSON file to store the results. Default file name is "prey.json".')
    parser.add_argument('-i', '--import', dest='import_url',
                        help='Optional. The import endpoint of the backend rest API to store probed cameras.')
    options = parser.parse_args()
    if not options.url and not options.batch_json_file and not options.batch_list_file:
        parser.error('URL to the RTSP stream or a batch json/list file must be specified. Use --help for more info.')
    if options.batch_json_file and options.batch_list_file:
        parser.error('You can not provide a batch json file and a batch list file both. Choose something.')
    if not options.output:
        options.output = 'prey.json'
    if not options.import_url:
        print('The import endpoint was not provided, results would be written to a file.')
    return options


class RtspClient:
    def __init__(self, output_file, import_endpoint=None):
        self.camera_reader = None
        self.output_file = output_file
        self.import_endpoint = import_endpoint

    class Target:
        class CameraStatus(Enum):
            UNCONNECTED = 0,
            NOT_FOUND = 1,
            UNAUTHORIZED = 2,
            OPEN = 3

        def __init__(self, url, ip=None, port=None, country_name=None, isp=None, country_code=None,
                     city=None):
            self.url = url
            self.ip = ip
            self.port = port
            self.country_name = country_name
            self.isp = isp
            self.country_code = country_code
            self.city = city
            self.status = self.CameraStatus.UNCONNECTED

        def to_dict(self):
            target = \
                {
                    # '@timestamp': datetime.now().strftime(DEFAULT_DATETIME_FORMAT),
                    'url': self.url,
                    'status': self.status.name,
                    'countryCode': self.country_code,
                    'countryName': self.country_name,
                    'city': self.city,
                    'isp': self.isp
                }
            return target

    def batch_json(self, batch_json_file):
        with open(batch_json_file, 'r', encoding='utf-8') as batch_json:
            targets = [line.replace('\n', '') for line in batch_json.readlines()]
            for target in targets:
                res = json.loads(target)
                ip_camera = RtspClient.Target(
                    url=f'rtsp://{res["ip_str"]}:{res["port"]}',
                    ip=res['ip_str'],
                    port=res['port'],
                    isp=res['isp'],
                    country_name=res['location']['country_name'],
                    country_code=res['location']['country_code'],
                    city=res['location']['city'])
                self.lookup(ip_camera)

    def batch_list(self, batch_list_file):
        with open(batch_list_file, 'r', encoding='utf-8') as batch_json:
            targets = [line.replace('\n', '') for line in batch_json.readlines()]
            for target in targets:
                ip = target.split('://')[1].split(':')[0]
                port = target.split('://')[1].split(':')[1]
                ip_camera = RtspClient.Target(
                    url=target,
                    ip=ip,
                    port=port,
                    isp=None,
                    country_name=None,
                    country_code=None,
                    city=None)
                self.lookup(ip_camera)

    def do_connect(self, target, stream=False):
        url = target.url
        print('Connecting to ' + url)
        self.camera_reader = cv2.VideoCapture(url)
        is_connected, frame = self.camera_reader.read()
        if is_connected:
            print('Connected.')
            target.status = target.CameraStatus.OPEN
            if stream:
                print('Starting stream...')
                while True:
                    is_connected, frame = self.camera_reader.read()
                    if is_connected:
                        cv2.imshow("View", frame)

                    pressed_key = cv2.waitKey(1)
                    if pressed_key & 0xFF == ord("q"):  # Exit condition
                        break
        else:
            print('Connection failed.')

    def lookup(self, target, stream=False):
        self.do_connect(target, stream)
        self.dump(target)
        if self.import_endpoint:
            self.send(target)

    def dump(self, target):
        print(f'Storing {target.url} / {target.status.name}')
        with open(self.output_file, 'a', encoding='utf-8') as f:
            json.dump(target.to_dict(), f)
            f.write('\n')

    def send(self, target):
        try:
            import requests
            session = requests.Session()
            response = session.put(url=self.import_endpoint,
                                    json=target.to_dict(),
                                    headers={
                                        "Content-Type": "application/json"
                                    })
            print(f'Camera [{target.url}] import API response: \n{response.status_code}\n{response.text}')
        except Exception as e:
            if 'refused' in str(e):
                print('Backend API is not responding. Is there a reachable server?')
            else:
                print(f'Unexpected error while communication with the API: {e}')


options = get_arguments()

rtsp_client = RtspClient(options.output, import_endpoint=options.import_url)
if not options.url:
    if options.batch_json_file:
        rtsp_client.batch_json(options.batch_json_file)
    if options.batch_list_file:
        rtsp_client.batch_list(options.batch_list_file)
else:
    rtsp_client.lookup(RtspClient.Target(url=options.url), stream=options.stream)