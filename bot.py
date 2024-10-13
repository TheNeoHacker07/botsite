from telebot import telebot
from telebot import types
from request import format_data, get_json, get_profile

bot_adress = '7943915772:AAFq4Ed-XeOE9mP73kymMo6NMk_Iu188ou8'

bot = telebot.TeleBot(bot_adress)

article_url = 'http://127.0.0.1:5000/article/'

@bot.message_handler(commands=['start'])
def start_message_handler(message):
    bot.send_message(message.chat.id, "hello, i'm your bot helper, if you want to continue write /go")


@bot.message_handler(commands=['go'])
def menu_start_method(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('new articles', callback_data='new')
    btn3 = types.InlineKeyboardButton('add article', callback_data='add')
    btn2 = types.InlineKeyboardButton('my articles', callback_data='mine')
    btn4 = types.InlineKeyboardButton('profile', callback_data='profile')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id,"choose your actions", reply_markup=markup)


@bot.callback_query_handler(func=lambda data:True)
def navigation_keyboards(callback):
    if callback.data == 'new':
        article = get_json(article_url)
        formatted_data = format_data(article)
        bot.send_message(callback.message.chat.id, formatted_data)
    elif callback.data == 'add':
        pass
    
    elif callback.data == 'mine':
        pass

    elif callback.data == 'profile':
        # username = callback.message.text.strip()
        # profile = get_profile(username=username)
        # if not profile:
        #     bot.send_message(callback.message.chat.id, "no user found")

        # profile_info = f'username ----{profile}'

        # bot.send_message(callback.message.chat.id, profile)

        bot.register_next_step_handler(callback.message, get_user_data)

def get_user_data(message):
    username = message.text.strip()
    profile = get_profile(username=username)
    if not profile:
        bot.send_message(message.chat.id, profile)
    bot.send_message(message.chat.id, 'no user found')




    

bot.polling(none_stop=True)

