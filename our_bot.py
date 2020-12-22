import config
import telebot
from telebot import types  # кнопки
from string import Template


# 1438805825: AAHDHNndstIeUV0OY7JUg8jI0tglBS_iViQ
bot = telebot.TeleBot(config.token)

user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['fullname', 'major']

        for key in keys:
            self.key = None

# если /help, /start


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/reg')
   
    markup.add(itembtn1, itembtn2)

    bot.send_message(message.chat.id, "Здравствуйте "
                     + message.from_user.first_name
                     + ", я бот, чтобы вы хотели узнать?", reply_markup=markup)

# /about


@bot.message_handler(commands=['about'])
def send_about(message):
    bot.send_message(message.chat.id, "We are MATH 20 "
                     + "students ")

# /reg


@bot.message_handler(commands=["reg"])
def user_reg(message):
    markup = types.ReplyKeyboardMarkup(
        one_time_keyboard=True, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Исфана')
    itembtn2 = types.KeyboardButton('Ош')
    itembtn3 = types.KeyboardButton('Баткен')
    itembtn4 = types.KeyboardButton('Бишкек')
    itembtn5 = types.KeyboardButton('Лондон')
    itembtn6 = types.KeyboardButton('Москва')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5, itembtn6)

    msg = bot.send_message(
        message.chat.id, 'Сиз жашаган шаар?', reply_markup=markup)
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        # удалить старую клавиатуру
        markup = types.ReplyKeyboardRemove(selective=False)

        msg = bot.send_message(chat_id, 'Фамилия Имя Отчество', reply_markup=markup)

        # ваша заявка "Имя пользователя"
        bot.send_message(chat_id, getRegData(
            user, 'Ваша заявка', message.from_user.first_name), parse_mode="Markdown")
        # отправить в группу
        bot.send_message(config.chat_id, getRegData(
            user, 'Заявка от бота', bot.get_me().username), parse_mode="Markdown")

    except Exception as e:
        bot.reply_to(message, 'ooops!!')

# формирует вид заявки регистрации
# нельзя делать перенос строки Template
# в send_message должно стоять parse_mode="Markdown"


def getRegData(user, title, name):
    t = Template('$title *$name* \n Город: *$userCity* \n ФИО: *$fullname*')

    return t.substitute({
        'title': title,
        'name': name,
        'userCity': user.city,
        'fullname': user.fullname,
        
    })

# произвольный текст


@bot.message_handler(content_types=["text"])
def send_help(message):
    bot.send_message(
        message.chat.id, 'О нас - /about\nРегистрация - /reg\nПомощь - /help')



# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)

# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
print(bot.get_chat("dilbaraasanalieva").id)

# print(bot.get_chat('dilbaraasanalieva').id)
