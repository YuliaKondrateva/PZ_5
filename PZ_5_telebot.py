import telebot
from telebot import types

bot = telebot.TeleBot('7149234218:AAETc-OsLYjYq4Eui3RXiyZpIZ8R8oFTkh4')

# Словарь для хранения данных пользователей
user_data = {}

# Старт и регистрация
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Напиши /reg для регистрации.")

@bot.message_handler(commands=['reg'])
def start_registration(message):
    bot.send_message(message.chat.id, "Как тебя зовут?")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    user_data[message.chat.id] = {'name': message.text}
    bot.send_message(message.chat.id, "Какая у тебя фамилия?")
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    user_data[message.chat.id]['surname'] = message.text
    bot.send_message(message.chat.id, "Сколько тебе лет?")
    bot.register_next_step_handler(message, get_age)

def get_age(message):
    try:
        age = int(message.text)
        user_data[message.chat.id]['age'] = age

        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_yes, key_no)

        user = user_data[message.chat.id]
        question = f"Тебе {user['age']} лет, тебя зовут {user['name']} {user['surname']}?"
        bot.send_message(message.chat.id, text=question, reply_markup=keyboard)

    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введи возраст цифрами!")
        bot.register_next_step_handler(message, get_age)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, "Данные сохранены!")
        # Здесь можно добавить сохранение в базу данных или файл, если нужно.
    elif call.data == "no":
        bot.send_message(call.message.chat.id, "Напиши /reg.")

# Запуск бота
bot.polling(none_stop=True)
