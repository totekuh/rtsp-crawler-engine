#!/usr/bin/env python3
import base64
import json
from pathlib import Path
from threading import Thread
from time import sleep

import cv2
import requests
from requests import Session

DEFAULT_OUTPUT_DIR = 'health-check'
DEFAULT_SLEEP_TIMER_IN_SECONDS = 10
DEFAULT_RTSP_BACKEND_URL = 'http://10.8.0.1:8080'

DEFAULT_THREAD_LIMIT = 50

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


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument('--rtsp-backend-url',
                        dest='rtsp_backend_url',
                        default=DEFAULT_RTSP_BACKEND_URL,
                        required=False,
                        help='Optional. An URL to the backend API. '
                        f'Default is : {DEFAULT_RTSP_BACKEND_URL}')

    ### HEALTH-CHECK EXISTING CAMERAS
    parser.add_argument('--camera-id',
                        dest='id',
                        required=False,
                        help='An identifier of the camera to perform the health-check.')

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
    parser.add_argument('--sleep-timer',
                        dest='sleep_timer',
                        default=DEFAULT_SLEEP_TIMER_IN_SECONDS,
                        type=int,
                        required=False,
                        help='Optional. Only valid with --search and --daemon arguments.'
                             'The specified value indicates the interval in seconds between updates '
                             'if the script works in the background.'
                        f'Default is {DEFAULT_SLEEP_TIMER_IN_SECONDS}')
    parser.add_argument('--output',
                        dest='output',
                        default=DEFAULT_OUTPUT_DIR,
                        required=False,
                        help='An absolute path to a directory where the screenshots '
                             'and metadata from the cameras should be written.'
                        f'Default is {DEFAULT_OUTPUT_DIR}')
    parser.add_argument('--threads',
                        dest='threads',
                        default=DEFAULT_THREAD_LIMIT,
                        type=int,
                        required=False,
                        help='Specify a number of threads to use while performing health-check of the cameras. '
                        f'Default is {DEFAULT_THREAD_LIMIT}')

    options = parser.parse_args()

    return options


class RtspBackendClient:
    def __init__(self,
                 rtsp_backend_url,
                 output_dir):
        self.session = Session()
        self.rtsp_backend_url = rtsp_backend_url
        self.output_dir = output_dir
        Path(self.output_dir).mkdir(exist_ok=True)

    def get_camera(self, camera_id):
        try:
            url = f'{self.rtsp_backend_url}/cameras'
            if camera_id:
                url = f'{url}?id={camera_id}'

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

    def health_check(self, camera):
        camera_url = camera['rtspUrl']
        print(f'Starting the health-check of the camera [id: {camera["cameraId"]}; rtsp-url: {camera_url}]')
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
                    'base64ImageData': base64ImageData,
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
                if self.update_camera(updated_camera):
                    print(f'Health check of the camera [id: {camera["cameraId"]}; '
                          f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has been completed. ')
                else:
                    print(f'Health check of the camera [id: {camera["cameraId"]}; '
                          f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has failed. ')

            else:
                updated_camera = {
                    'status': 'UNCONNECTED',
                    'url': camera['rtspUrl'],
                    'labels': camera['labels']
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
                if self.update_camera(updated_camera):
                    print(f'Health check of the camera [id: {camera["cameraId"]}; '
                          f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has been completed. ')
                else:
                    print(f'Health check of the camera [id: {camera["cameraId"]}; '
                          f'url: {camera["rtspUrl"]}; camera-status: {[camera["status"]]}] has failed. ')
        except Exception as e:
            print(e)

    def update_camera(self, camera):
        try:
            if 'rtspUrl' in camera and 'url' not in camera:
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

rtsp_backend_url = options.rtsp_backend_url
client = RtspBackendClient(rtsp_backend_url, output_dir)


def start_separate_health_check_process(camera_id):
    import os
    import sys

    os.system(f'{sys.argv[0]} --camera-id {camera_id}')


class HealthCheckThread:
    def __init__(self, camera, rtsp_backend_url, output_dir):
        self.camera = camera
        self.rtsp_client = RtspBackendClient(rtsp_backend_url, output_dir)
        self.thread = Thread(target=start_separate_health_check_process, args=(camera['cameraId'],))
        self.thread_name = f'{camera["cameraId"]}-thread'

    def start(self):
        self.thread.start()
        print(f'{self.thread_name} has started for {self.camera["rtspUrl"]}')

    def is_alive(self):
        return self.thread.is_alive()


def health_check(cameras, threads_limit, sleep_timer):
    print(f'Found {len(cameras)} cameras for the health-check')

    health_check_threads = []

    for camera in cameras:
        while len(health_check_threads) >= threads_limit:
            print(f'Health-checker has faced the threads limit, sleeping for {sleep_timer} seconds and continue...')
            sleep(sleep_timer)

            for thread in health_check_threads.copy():
                if not thread.is_alive():
                    health_check_threads.remove(thread)
        camera_thread = HealthCheckThread(camera, rtsp_backend_url, output_dir)
        health_check_threads.append(camera_thread)
        camera_thread.start()

    while any(thread.is_alive() for thread in health_check_threads):
        print(f'Not all threads have finished yet, sleeping for {sleep_timer} seconds and continue...')
        sleep(sleep_timer)

        for thread in health_check_threads.copy():
            if not thread.is_alive():
                health_check_threads.remove(thread)


def download_cameras_and_do_health_check(client, threads_limit, sleep_timer):
    print('Downloading a list of camera ids from the backend API')
    camera_ids = client.get_all_camera_ids()
    if not camera_ids:
        print('The backend API has responded with an empty list of cameras')
    else:
        print(f'{len(camera_ids)} camera ids have been discovered')
        cameras = []
        for i, camera_id in enumerate(camera_ids):
            print(f'Asking the backend API about the camera [{i + 1}/{len(camera_ids)}]')
            camera = client.get_camera(camera_id)
            if camera:
                cameras.append(camera)
        if cameras:
            health_check(cameras, threads_limit, sleep_timer)
        else:
            print('No cameras have been passed for the health-check.')


def main(options):
    if not options.id:
        if options.daemon:
            print('Starting the health-check daemon')
            sleep_timer = options.sleep_timer
            while True:
                download_cameras_and_do_health_check(client, options.threads, options.sleep_timer)
                print(f'Sleeping for {sleep_timer} seconds')
                sleep(sleep_timer)
        else:
            download_cameras_and_do_health_check(client, options.threads, options.sleep_timer)
    else:
        # health check a single camera
        camera_id = options.id
        rtsp_client = RtspBackendClient(rtsp_backend_url, output_dir)
        camera = rtsp_client.get_camera(camera_id)
        if options.daemon:
            print('Starting the health-check daemon')
            sleep_timer = options.sleep_timer
            while True:
                rtsp_client.health_check(camera)
                print(f'Sleeping for {sleep_timer} seconds')
                sleep(sleep_timer)
        else:
            rtsp_client.health_check(camera)


if __name__ == '__main__':
    options = get_arguments()
    main(options)
