#!/usr/bin/env python3

import json
from functools import wraps
from os import chdir, linesep, listdir

from config import TOKEN, WHITELIST
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater
from threading import Thread
from flask import Flask, make_response, request

ALL_LABELS = [
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
]

DEFAULT_NOTIFICATION_SERVER_IP = '10.8.0.14'
DEFAULT_NOTIFICATION_SERVER_PORT = 8080

notification_server_app = Flask(__name__)

global_notification_callback = None


@notification_server_app.route('/notification', methods=['POST'])
def notification():
    global global_notification_callback
    global_notification_callback = request.json

    return "Thank you very much!"


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--path',
                        dest='path',
                        required=True,
                        help='A path to the folder with stored screenshots and their metadata.')
    parser.add_argument('--notification-server',
                        action='store_true',
                        required=False,
                        help='Start the notification web-server. '
                             'The notification server receives updates from the rtsp-model script when a new label is '
                             'discovered.')
    parser.add_argument('--notification-server-ip',
                        dest='notification_server_ip',
                        default=DEFAULT_NOTIFICATION_SERVER_IP,
                        required=False,
                        help=f'An IP address of the notification server to bind to. '
                        f'Default is {DEFAULT_NOTIFICATION_SERVER_IP}')
    parser.add_argument('--notification-server-port',
                        dest='notification_server_port',
                        default=DEFAULT_NOTIFICATION_SERVER_PORT,
                        required=False,
                        help=f'A TCP port of the notification server to bind to. '
                        f'Default is {DEFAULT_NOTIFICATION_SERVER_PORT}')
    options = parser.parse_args()

    return options


options = get_arguments()


def whitelist_only(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        user = update.effective_user
        print(f"@{user.username} ({user.id}) is trying to access a privileged command")
        if user.username not in WHITELIST:
            print(f"Unauthorized access denied for {user.username}.")
            text = (
                "🚫 *ACCESS DENIED*\n"
                "Sorry, you are *not authorized* to use this command"
            )
            update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)
            return
        return func(update, context, *args, **kwargs)

    return wrapped


class RtspFileWatcher:
    def __init__(self, health_check_path):
        self.health_check_path = health_check_path
        self.cameras_json_list = []

        chdir(self.health_check_path)
        for file in listdir('.'):
            if '.json' in file:
                with open(file, 'r') as f:
                    self.cameras_json_list.append(json.load(f))

    def find_by_label(self, label):
        cameras = []
        for camera in self.cameras_json_list:
            if 'labels' in camera:
                for stored_label in camera['labels']:
                    if label in stored_label['name']:
                        cameras.append(camera)
        return cameras

    def get_img_file_handler_by_camera_id(self, camera_id):
        for camera in self.cameras_json_list:
            if camera_id == camera['cameraId']:
                return open(f'{camera_id}.jpg', 'rb')

    def get_camera_by_id(self, camera_id):
        for camera in self.cameras_json_list:
            if camera_id == camera['cameraId']:
                return camera


rtsp_file_watcher = None


def start(update, context):
    """Send a message when the command /start is issued."""
    text = "Registering the RTSP monitor..."
    update.message.reply_text(text)

    global rtsp_file_watcher
    options = get_arguments()
    if rtsp_file_watcher:
        update.message.reply_text('The RTSP monitor is already registered.')
    else:
        rtsp_file_watcher = RtspFileWatcher(options.path)
        update.message.reply_text(f'The RTSP monitor has been initialized with '
                                  f'{len(rtsp_file_watcher.cameras_json_list)} cameras')


@whitelist_only
def help(update, context):
    text = (
                'Use this bot to find cameras by the given labels.\n'
                'The /find command prints the number of cameras.\n'
                'The /monitor command periodically sends screenshots of cameras.\n\n'
                'The /watch command enables the notification listener for the bot. After the watch is established, '
                'the bot starts to receive events '
                'from the rtsp-model to stream them into the active dialog.\n\n'
                'All possible labels are:\n' +
                '\n'.join(ALL_LABELS)
    )
    update.message.reply_text(text)


@whitelist_only
def find(update, context):
    if not rtsp_file_watcher:
        update.message.reply_text('The RTSP monitor is not initialized. Use /start to enable it.')
        return
    labels = context.args

    if not labels:
        update.message.reply_text('Searching all cameras...')
        found_cameras = {}
        for label in ALL_LABELS:
            cameras_by_label = rtsp_file_watcher.find_by_label(label)
            if cameras_by_label:
                found_cameras[label] = cameras_by_label
        if found_cameras:
            message = ''
            for label, cameras in found_cameras.items():
                message += f'{label} - {len(cameras)}\n'
            update.message.reply_text(message)
        return
    else:
        update.message.reply_text(f'Searching by: [{linesep.join(labels)}]')
        for label in labels:
            cameras_by_label = rtsp_file_watcher.find_by_label(label)
            if cameras_by_label:
                update.message.reply_text(f'[{label}] - {len(cameras_by_label)} cameras')


@whitelist_only
def monitor(update, context):
    if not rtsp_file_watcher:
        update.message.reply_text('The RTSP monitor is not initialized. Use /start to enable it.')
        return
    labels = context.args

    if not labels:
        update.message.reply_text('You have to specify a label or a space-separated list of labels to monitor.\n' +
                                  'Use /help for more info.')
    else:
        update.message.reply_text(f'Monitoring cameras by: [{linesep.join(labels)}]')
        for label in labels:
            cameras_by_label = rtsp_file_watcher.find_by_label(label)
            if cameras_by_label:
                for camera in cameras_by_label:
                    camera_id = camera["cameraId"]
                    img_file = f'{camera_id}.jpg'
                    metadata = f"camera-id: {camera_id}; " \
                        f"country: {camera['countryName']}; " \
                        f"city: {camera['city']}; " \
                        f"rtsp-url: {camera['rtspUrl']}"
                    update.message.reply_photo(open(img_file, 'rb'), caption=metadata)


def start_notification_server(app, ip, port):
    app.run(host=ip, port=port)


@whitelist_only
def watch(update, context):
    options = get_arguments()
    if not options.notification_server:
        update.message.reply_text(
                    'The RTSP notification server is not enabled. The bot should be restarted with the correct CLI '
                    'arguments.')
    else:
        update.message.reply_text('Starting the RTSP notification listener.')

        notification_server_thread = Thread(target=start_notification_server,
                                            args=(notification_server_app,
                                                  options.notification_server_ip,
                                                  options.notification_server_port))
        notification_server_thread.start()
        print('The notification server has been started')

        labels = context.args
        if not labels:
            update.message.reply_text('Please specify a label to watch. Use /help for more info')
        else:
            while True:
                global global_notification_callback
                if not global_notification_callback:
                    continue
                else:
                    print('Receiving a new notification')
                    camera_id = global_notification_callback['cameraId']
                    received_labels = global_notification_callback['labels']

                    if any(label in received_labels for label in labels):
                        img_file_handler = rtsp_file_watcher.get_img_file_handler_by_camera_id(camera_id)

                        camera = rtsp_file_watcher.get_camera_by_id(camera_id)
                        metadata = f"camera-id: {camera_id}; " \
                            f"country: {camera['countryName']}; " \
                            f"city: {camera['city']}; " \
                            f"rtsp-url: {camera['rtspUrl']}"
                        update.message.reply_photo(img_file_handler, caption=metadata)
                        global_notification_callback = None


def error(update, context):
    """Log Errors caused by Updates."""
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(TOKEN, use_context=True)
    # Note that this is only necessary in version 12 of python-telegram-bot. Version 13 will have use_context=True
    # set as default.

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("find", find))
    dp.add_handler(CommandHandler("monitor", monitor))
    dp.add_handler(CommandHandler("watch", watch))
    dp.add_error_handler(error)

    updater.start_polling()
    print("BOT DEPLOYED. Ctrl+C to terminate")
    updater.idle()


if __name__ == "__main__":
    main()
