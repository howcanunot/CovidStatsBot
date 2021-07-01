import telebot
import threading
from config import token
from parse_data import get_info, max_cases, regression_week, stats_week
from telebot import types


bot = telebot.TeleBot(token)

select_country_flag = False
func = ''


def __init_inline_markup():
    markup = types.InlineKeyboardMarkup(row_width=3)

    markup.add(types.InlineKeyboardButton('Get Information', callback_data='get inf'))
    markup.add(types.InlineKeyboardButton('Max cases', callback_data='max'))
    markup.add(types.InlineKeyboardButton('Predict', callback_data='pr'))
    markup.add(types.InlineKeyboardButton('7 days graphic', callback_data='plot'))

    return markup


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    if message.text == "/start":
        bot.send_message(message.chat.id, '''There are four functions that you can use:\n
1. Get information. This function gives you all todays data about one specific data.
2. Max cases. This function gives you country with maximum amount of new cases and.
3. Predict. This function is based on the algorithm that predicts an amount of new cases tomorrow. You can choose from taking data for 1 week and 1 month.
4. 7 days graphic. This function gives you a graphic with numbers of new Covid cases during last 7 days. Also we can provide you with last month stats''', reply_markup=__init_inline_markup())
    else:
        bot.send_message(message.chat.id, '''Be sure that you type your country in correct way. You can find correct name in the list below:\n
- United States
- United Kingdom
- Sounth Korea
- Cote d'Ivoire
- United Arab Emirate
- Brunei''')


@bot.callback_query_handler(func=lambda call: True)
def event_handler(call):

    updates = {'new': 1, 'in progress': 2, 'resolved': 3, 'feedback': 4, 'closed': 5}
    global select_country_flag, func
    if call.data == 'get inf':
        try:
            func = 'get inf'
            select_country_flag = True
            bot.send_message(call.message.chat.id, text='Input country name:')
        except Exception as ex:
            bot.send_message(call.message.chat.id, 'Something went wrong: {}'.format(ex))
    elif call.data == 'max':
        cases = max_cases(None)
        bot.send_message(call.message.chat.id, text='Max cases country:\n<b>{}-{}</b>'.format(cases[0], cases[1]), parse_mode='HTML')
    elif call.data == 'pr':
        try:
            select_country_flag = True
            func = 'pr'
            bot.send_message(call.message.chat.id, text='Input country name:')
        except Exception as ex:
            bot.send_message(call.message.chat.id, 'Something went wrong: {}'.format(ex))
    elif call.data == 'plot':
        try:
            select_country_flag = True
            func = 'plot'
            bot.send_message(call.message.chat.id, text='Input country name:')
        except Exception as ex:
            bot.send_message(call.message.chat.id, 'Something went wrong: {}'.format(ex))


@bot.message_handler(content_types=['text'])
def reply_stats(message):
    global select_country_flag
    if select_country_flag and func == 'get inf':
        try:
            bot.send_message(message.chat.id, text=get_info(message.text))
            select_country_flag = False
        except:
            bot.send_message(message.chat.id, text='Incorrect country name. Please try again')
    elif select_country_flag and func == 'pr':
        try:
            bot.send_message(message.chat.id, text='Predicted number of new cases tomorrow:{}'.format(regression_week(message.text)))
            select_country_flag = False

        except:
            bot.send_message(message.chat.id, text='Incorrect country name. Please try again')

    elif select_country_flag and func == 'plot':
        try:
            stats_week(message.text)
            img = open('saved_figure1.png', 'rb')
            bot.send_photo(message.chat.id, photo=img)
            select_country_flag = False
            img.close()
        except:
            bot.send_message(message.chat.id, text='Incorrect country name. Please try again')


def __start_thread():
    bot.polling()


def start():
    thread = threading.Thread(target=__start_thread)
    thread.start()
    return thread
