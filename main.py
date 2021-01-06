import sys
import logging
from io import BytesIO

from PIL import Image
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from src.filter_cv import CVFilter

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def read_token():
    try:
        with open('token', 'r') as f:
            return f.readline()
    except FileNotFoundError:
        return 0


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def save_photo(path_to_file, photo) -> True:
    image = Image.open(photo)
    image.save(path_to_file)
    return True


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    file = context.bot.get_file(update.message.photo[-1].file_id)
    filter_cv = CVFilter(file=file.download_as_bytearray())
    image = filter_cv.set_filter()
    image = BytesIO(image)
    context.bot.send_photo(chat_id=update.message.chat_id, photo=image)


def main():
    """Start the bot."""
    # Read TOKEN
    token = read_token()

    if not token:
        sys.exit()

    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(token=token, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
