#!/usr/bin/env python3
import base64
import json
from pathlib import Path
from time import sleep

import cv2
import requests
from requests import Session

DEFAULT_OUTPUT_DIR = 'health-check'
DEFAULT_SLEEP_TIMER_IN_SECONDS = 10
DEFAULT_RTSP_BACKEND_URL = 'http://10.8.0.1:8080'

camera_statuses = [
    # Clearly exposed cameras. Just go for it.
    'OPEN',
    # The RTSP stream exists, but there are no valid credentials.
    'UNAUTHORIZED',
    # The RTSP stream exists, but the actual URL is not determined.
    'NOT_FOUND',
    # The RTSP stream doesn't exist or the server has refused to connect.
    'UNCONNECTED'
]

camera_keywords = [
    'HOT',
    'WOMAN',
    'MAN',
    'CHILDREN',
    'CREEPY',
    'AUTISTIC',
    'SLAVERY'
]


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--rtsp-backend-url',
                        dest='rtsp_backend_url',
                        default=DEFAULT_RTSP_BACKEND_URL,
                        required=False,
                        help='Optional. An URL to the backend API. '
                        f'Default is : {DEFAULT_RTSP_BACKEND_URL}')

    # GET A CAMERA
    parser.add_argument('--get',
                        action='store_true',
                        required=False,
                        help='Get a single camera from the RTSP database. '
                             'Should be used in pair with the following '
                             'arguments: --id or --rtsp-url')
    parser.add_argument('--id',
                        dest='id',
                        required=False,
                        help='Optional. Get a single camera by its identifier.')
    parser.add_argument('--rtsp-url',
                        dest='rtsp_url',
                        required=False,
                        help='Optional. Get a single camera by its rtsp URL. '
                             'Must be in the following format: '
                             'rtsp://10.10.10.10:554/')

    # SEARCH SPECIFIC CAMERAS
    parser.add_argument('--search',
                        action='store_true',
                        required=False,
                        help='Search the rest API for a list of cameras by the given rules.')
    parser.add_argument('--country-code',
                        dest='country_code',
                        required=False,
                        help='Optional. Only valid with --search argument. '
                             'Search for the cameras by the given country code.')
    parser.add_argument('--city',
                        dest='city',
                        required=False,
                        help='Optional. Only valid with --search argument. '
                             'Search for the cameras by the given city name.')
    parser.add_argument('--camera-status',
                        dest='camera_status',
                        choices=camera_statuses,
                        required=False,
                        help='Optional. Only valid with --search argument. '
                             'Search for the cameras by the given camera status.')
    parser.add_argument('--keyword',
                        dest='keyword',
                        choices=camera_keywords,
                        required=False,
                        help='Optional. Only valid with --search argument. '
                             'Search for the cameras by the given keyword.')
    parser.add_argument('--sleep-timer',
                        dest='sleep_timer',
                        default=DEFAULT_SLEEP_TIMER_IN_SECONDS,
                        required=False,
                        help='Optional. Only valid with --search and --daemon arguments.'
                             'The specified value indicates the interval in seconds between updates '
                             'if the script works in the background.'
                        f'Default is {DEFAULT_SLEEP_TIMER_IN_SECONDS}')

    ### HEALTH-CHECK EXISTING CAMERAS
    parser.add_argument('--health-check',
                        action='store_true',
                        required=True,
                        help='Access the rtsp backend API to retrieve a list of cameras '
                             'and periodically health check their status. '
                             'When this argument is given, the script rechecks the status of existing cameras and '
                             'push back the results of their status to the running server '
                             'as well as capturing the screenshot and the metadata from the camera.')

    ### OTHER PROPERTIES
    parser.add_argument('--daemon',
                        action='store_true',
                        required=False,
                        help='Send the script to work in the background. '
                             'During the work, the script periodically checks the backend API '
                             'to update the status of cameras and download new screenshots. '
                             'When the --health-check and --daemon arguments are given, '
                             'the script repeatedly checks the status of the downloaded cameras '
                             'and pushes the status back to the backend API')
    parser.add_argument('--output',
                        dest='output',
                        default=DEFAULT_OUTPUT_DIR,
                        required=False,
                        help='An absolute path to a directory where the screenshots '
                             'and metadata from the cameras should be written.'
                        f'Default is {DEFAULT_OUTPUT_DIR}')

    options = parser.parse_args()

    if options.get and not options.id and not options.rtsp_url:
        parser.error('Please specify --id or --rtsp-url argument in a pair with --get. '
                     'Use --help for more info.')
    if options.sleep_timer:
        options.sleep_timer = int(options.sleep_timer)

    return options


class RtspBackendClient:
    def __init__(self,
                 rtsp_backend_url,
                 output_dir):
        self.session = Session()
        self.rtsp_backend_url = rtsp_backend_url
        self.output_dir = output_dir

    def get_cameras(self, camera_id=None, camera_rtsp_url=None):
        if camera_id and camera_rtsp_url:
            raise Exception("Stop doing that.")
        try:
            url = f'{self.rtsp_backend_url}/cameras'
            if camera_id:
                url = f'{url}?id={camera_id}'
            if camera_rtsp_url:
                url = f'{url}?rtspUrl={camera_rtsp_url}'

            resp = self.session.get(url)
            if resp.ok:
                return resp.json()
            else:
                print(resp.status_code)
                print(resp.text)
        except Exception as e:
            print(e)

    def get_all_camera_ids(self):
        try:
            url = f'{self.rtsp_backend_url}/cameras/ids'

            resp = self.session.get(url)
            if resp.ok:
                return resp.json()['cameraIds']
            else:
                print(resp.status_code)
                print(resp.text)
        except Exception as e:
            print(e)

    def search_cameras(self, params):
        try:
            url = f'{self.rtsp_backend_url}/cameras/search'

            resp = self.session.post(url, json=params)
            if resp.ok:
                return resp.json()
            else:
                print(resp.status_code)
                print(resp.text)
        except Exception as e:
            print(e)

    def write_base64_screenshot_to_file_for_open_cameras(self, cameras):
        for camera in cameras['cameras']:
            if camera['status'] == 'OPEN' and camera['base64ImageData']:
                self.write_base64_encoded_images_to_file(camera)

    def write_base64_encoded_images_to_file(self, camera):
        camera_id = camera['cameraId']
        imgdata = base64.b64decode(camera['base64ImageData'])
        with open(f'{self.output_dir}/{camera_id}.jpg', 'wb') as f:
            f.write(imgdata)

    def health_check(self, camera):
        camera_url = camera['rtspUrl']
        try:
            camera_reader = cv2.VideoCapture(camera_url)
            is_connected, frame = camera_reader.read()
            if is_connected:
                # convert the captured frame to a base64 string
                img_file_name = f'{self.output_dir}/{camera["cameraId"]}.jpg'
                cv2.imwrite(img_file_name, frame)
                with open(img_file_name, "rb") as image_file:
                    base64ImageData = base64.b64encode(image_file.read()).decode('utf-8')

                updated_camera = {
                    'status': 'OPEN',
                    'url': camera['rtspUrl'],
                    'base64ImageData': base64ImageData
                }
                with open(f'{self.output_dir}/{camera["cameraId"]}.json', 'w', encoding='utf-8') as f:
                    camera_to_save = {
                        'countryCode': camera['countryCode'],
                        'countryName': camera['countryName'],
                        'city': camera['city'],
                        'rtspUrl': camera['rtspUrl'],
                        'cameraId': camera['cameraId'],
                        'status': updated_camera['status']
                    }
                    json.dump(camera_to_save, f)
                return self.update_camera(updated_camera)
            else:
                updated_camera = {
                    'status': 'UNCONNECTED',
                    'url': camera['rtspUrl'],
                }
                with open(f'{self.output_dir}/{camera["cameraId"]}.json', 'w', encoding='utf-8') as f:
                    camera_to_save = {
                        'countryCode': camera['countryCode'],
                        'countryName': camera['countryName'],
                        'city': camera['city'],
                        'rtspUrl': camera['rtspUrl'],
                        'cameraId': camera['cameraId'],
                        'status': 'UNCONNECTED'
                    }
                    json.dump(camera_to_save, f)
                return self.update_camera(updated_camera)
        except Exception as e:
            print(e)

    def update_camera(self, camera):
        try:
            if 'rtspUrl' in camera:
                camera['url'] = camera['rtspUrl']
            resp = requests.put(f'{rtsp_backend_url}/cameras/import', json=camera)
            if resp.ok:
                return resp.json()
            else:
                print(resp.status_code)
                print(resp.text)
        except Exception as e:
            print(e)


options = get_arguments()
output_dir = options.output

Path(output_dir).mkdir(exist_ok=True)

rtsp_backend_url = options.rtsp_backend_url
client = RtspBackendClient(rtsp_backend_url, output_dir)


def get_camera(client, id=None, rtsp_url=None):
    camera = client.get_cameras(camera_id=id, camera_rtsp_url=rtsp_url)
    if camera and camera['status'] == 'OPEN' and camera['base64ImageData']:
        client.write_base64_encoded_images_to_file(camera)
    else:
        print('No such cameras has been found in the RTSP database.')
        exit()


def search_cameras(client,
                   country_code=None,
                   camera_status=None,
                   city=None,
                   keyword=None,
                   top=None):
    search_params = {}
    if country_code:
        search_params['countryCode'] = country_code
    if camera_status:
        search_params['status'] = camera_status
    else:
        search_params['status'] = 'OPEN'
    if city:
        search_params['city'] = city
    if keyword:
        search_params['keywords'] = [keyword]
    if top:
        search_params['status'] = 'OPEN'
        search_params['order'] = 'CREATION_TIMESTAMP_DESC'
    cameras = client.search_cameras(params=search_params)
    if cameras and cameras['cameras']:
        client.write_base64_screenshot_to_file_for_open_cameras(cameras)
    else:
        print('No cameras have been found in the RTSP database.')
        exit()


def health_check(cameras):
    print(f'Found {len(cameras)} cameras for the health-check')
    for i, camera in enumerate(cameras):
        is_updated = client.health_check(camera)
        if is_updated:
            print(f'Health check of the camera [id: {camera["cameraId"]}; '
                  f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has been completed. '
                  f'[{i + 1}/{len(cameras)}]')
        else:
            print(f'Health check of the camera [id: {camera["cameraId"]}; '
                  f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has failed. '
                  f'[{i + 1}/{len(cameras)}]')


def download_cameras_and_do_health_check(client):
    print('Downloading a list of camera ids from the backend API')
    camera_ids = client.get_all_camera_ids()
    if not camera_ids:
        print('No cameras have been downloaded from the backend API')
    else:
        print(f'{len(camera_ids)} camera ids have been discovered')
    cameras = []
    for i, camera_id in enumerate(camera_ids):
        camera = client.get_cameras(camera_id)
        print(f'Asking the backend API about the camera [{i}/{len(camera_ids)}]')
        if camera:
            cameras.append(camera)
    if cameras:
        health_check(cameras)
    else:
        print('No cameras have been passed for the health-check.')


### GET A CAMERA / GET ALL CAMERAS
if options.get:
    if options.daemon:
        # work in the background
        sleep_timer = options.sleep_timer
        while True:
            get_camera(client, id=options.id, rtsp_url=options.rtsp_url)
            print(f'Sleeping for {sleep_timer} seconds')
            sleep(sleep_timer)
    else:
        # work in the foreground
        get_camera(client, id=options.id, rtsp_url=options.rtsp_url)

### SEARCH SPECIFIC CAMERAS
if options.search:
    if options.daemon:
        sleep_timer = options.sleep_timer
        while True:
            search_cameras(client,
                           camera_status=options.camera_status,
                           city=options.city,
                           keyword=options.keyword,
                           top=options.top)
            print(f'Sleeping for {sleep_timer} seconds')
            sleep(sleep_timer)
    else:
        search_cameras(client,
                       camera_status=options.camera_status,
                       city=options.city,
                       keyword=options.keyword,
                       top=options.top)

### HEALTH-CHECK THE CAMERAS
if options.health_check:
    if options.daemon:
        print('Starting the health-check daemon')
        sleep_timer = options.sleep_timer
        while True:
            download_cameras_and_do_health_check(client)
            print(f'Sleeping for {sleep_timer} seconds')
            sleep(sleep_timer)
    else:
        download_cameras_and_do_health_check(client)
