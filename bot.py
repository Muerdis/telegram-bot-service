from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler
import logging


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


ALL, END = ['all', 'end']
SLEEP_STATE, CODE_STATE, EAT_STATE = ['sleep_state', 'code_state', 'eat_state']


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Будильник", callback_data=str(CODE_STATE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Сплю", reply_markup=reply_markup)

    return ALL


def sleep_state(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Будильник", callback_data=str(CODE_STATE)),]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Сплю",
        reply_markup=reply_markup
    )
    return ALL


def code_state(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Устал", callback_data=str(SLEEP_STATE)),
         InlineKeyboardButton("Проголодался", callback_data=str(EAT_STATE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Пишу код",
        reply_markup=reply_markup
    )
    return ALL


def eat_state(update, context):
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("Объелся", callback_data=str(SLEEP_STATE)),
         InlineKeyboardButton("Подкрепился", callback_data=str(CODE_STATE))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(
        text="Ем печеньки",
        reply_markup=reply_markup
    )
    return ALL


def main():
    updater = Updater("TOKEN", use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ALL: [CallbackQueryHandler(sleep_state, pattern='^' + str(SLEEP_STATE) + '$'),
                  CallbackQueryHandler(code_state, pattern='^' + str(CODE_STATE) + '$'),
                  CallbackQueryHandler(eat_state, pattern='^' + str(EAT_STATE) + '$')],
            END: []
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
