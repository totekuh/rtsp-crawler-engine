#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from functools import wraps

from config import TOKEN, WHITELIST
from telegram import ParseMode
from telegram.ext import CommandHandler, Updater


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


def start(update, context):
    """Send a message when the command /start is issued."""
    text = (
        "Starting the rtsp notification listener.\n"
    )
    update.message.reply_text(text)


@whitelist_only
def healthcheck(update, context):
    pass


# if context.args:
#     update.message.reply_text(text, parse_mode=ParseMode.MARKDOWN)


def error(update, context):
    """Log Errors caused by Updates."""
    print(f"Update {update} caused error {context.error}")


def main():
    updater = Updater(TOKEN, use_context=True)
    # Note that this is only necessary in version 12 of python-telegram-bot. Version 13 will have use_context=True
    # set as default.

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("healthcheck", healthcheck))
    dp.add_error_handler(error)

    updater.start_polling()
    print("BOT DEPLOYED. Ctrl+C to terminate")

    updater.idle()


if __name__ == "__main__":
    main()
