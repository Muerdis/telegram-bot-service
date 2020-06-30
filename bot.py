from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, ConversationHandler
import logging
import requests


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


ALL, END = ['all', 'end']


def start(update, context):
    keyboard = [
        [InlineKeyboardButton("Будильник", callback_data='alarm_clock sleep_state')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Сплю", reply_markup=reply_markup)

    return ALL


def run_action(update, context):
    query = update.callback_query
    query.answer()
    action_info = query.data.split()

    resp = requests.get(f'http://127.0.0.1:5000/api/developer/{action_info[1]}/{action_info[0]}')
    keyboard_data = []
    if resp.status_code == 200:
        resp = resp.json()
        actions = resp.get('actions', [])
        now_state = resp.get('now_state', {})
        for action in actions:
            keyboard_data.append(
                InlineKeyboardButton(action['value'], callback_data=f'{action["key"]} {now_state["key"]}')
            )

        keyboard = [keyboard_data]
        reply_markup = InlineKeyboardMarkup(keyboard)

        query.edit_message_text(
            text=now_state['value'],
            reply_markup=reply_markup
        )
    return ALL


def main():
    updater = Updater('TOKEN', use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ALL: [CallbackQueryHandler(run_action, pattern='alarm_clock sleep_state'),
                  CallbackQueryHandler(run_action, pattern='tired code_state'),
                  CallbackQueryHandler(run_action, pattern='hungry code_state'),
                  CallbackQueryHandler(run_action, pattern='refreshing eat_state'),
                  CallbackQueryHandler(run_action, pattern='overeat eat_state')],
            END: []
        },
        fallbacks=[CommandHandler('start', start)]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
