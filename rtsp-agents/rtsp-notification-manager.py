#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from functools import wraps
from os import linesep, listdir, chdir

from telegram import ParseMode
from telegram.ext import CommandHandler, Updater

from config import TOKEN, WHITELIST

ALL_LABELS = [
    'background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus',
    'car', 'cat', 'chair', 'cow', 'diningtable', 'dog', 'horse', 'motorbike',
    'person', 'pottedplant', 'sheep', 'sofa', 'train', 'tv'
]


def get_arguments():
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('--path',
                        dest='path',
                        required=True,
                        help='A path to the folder with stored screenshots and their metadata.')
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
        for label in ALL_LABELS:
            cameras_by_label = rtsp_file_watcher.find_by_label(label)
            if cameras_by_label:
                update.message.reply_text(f'[{label}] - {len(cameras_by_label)} cameras')
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
                    img_file = f'{camera["cameraId"]}.jpg'
                    metadata = f"country: {camera['countryName']}; city: {camera['city']}; rtsp-url: {camera['rtspUrl']}"
                    update.message.reply_photo(open(img_file, 'rb'), caption=metadata)


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
    dp.add_error_handler(error)

    updater.start_polling()
    print("BOT DEPLOYED. Ctrl+C to terminate")
    updater.idle()


if __name__ == "__main__":
    main()
