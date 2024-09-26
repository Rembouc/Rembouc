import os
import re
import time
from datetime import datetime
from collections import defaultdict
import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from telebot import types

# Загрузка переменных окружения
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(TOKEN)

# Функции для обработки текста
def clean_text(text):
    text = re.sub(r'\(.*?\)', '', text)
    text = re.sub(r'\[.*?]', '', text)
    return text.strip()

def format_animal_name(animal_name):
    return re.sub(r'\s+', '_', animal_name.strip())

# Функции для получения информации о животных
def get_animal_paragraph_and_image(animal_name):
    formatted_name = format_animal_name(animal_name)
    animal_url = f"https://ru.wikipedia.org/wiki/{formatted_name}"
    animal_paragraphs = []
    animal_image_url = None

    try:
        response = requests.get(animal_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        animals_inf = soup.find(class_="mw-content-ltr mw-parser-output").find_all("p")
        for paragraph in animals_inf:
            paragraph_text = paragraph.text.replace("\n", "")
            animal_paragraphs.append(paragraph_text)

        image = soup.find(class_="infobox-image")
        if image:
            animal_image_url = "https:" + image.find("img")["src"]

        return {
            "info": animal_paragraphs[:3],
            "image_url": animal_image_url,
            "article_url": animal_url
        }
    except Exception as e:
        return {
            "info": [f"Не удалось найти информацию о животном: {animal_name}. Ошибка: {str(e)}"],
            "image_url": None,
            "article_url": None
        }

# Функции для получения пород собак и кошек
def get_dog_breeds():
    dog_breeds_url = "https://www.purinaone.ru/dog/articles/breeds/samye-populyarnye-porody-sobak-s-fotografiyami-i-nazvaniyami"
    popular_dog_breeds = []
    dog_response = requests.get(dog_breeds_url)
    dog_response.raise_for_status()
    soup = BeautifulSoup(dog_response.text, 'html.parser')
    dog_breeds = soup.find_all("b")

    for dog_breed in dog_breeds:
        breed_name = dog_breed.text.strip()
        breed_name = re.sub(r'^\d+\.\s*', '', breed_name)
        breed_name = breed_name.rstrip('.')
        popular_dog_breeds.append(breed_name)

    popular_dog_breeds.sort()
    return [f"{idx + 1}. {breed}" for idx, breed in enumerate(popular_dog_breeds)]

def get_cat_breeds():
    cat_breeds_url = "https://goodhands.vet/blog/voprosy/samye-populyarnye-porody-koshek-v-rossii/"
    popular_cat_breeds = []
    cat_response = requests.get(cat_breeds_url)
    cat_response.raise_for_status()
    soup = BeautifulSoup(cat_response.text, 'html.parser')
    cat_breeds = soup.find_all("h3")

    for cat_breed in cat_breeds[:8]:
        breed_name = cat_breed.text.strip()
        breed_name = breed_name.rstrip('.')
        popular_cat_breeds.append(breed_name)

    popular_cat_breeds.sort()
    return [f"{idx + 1}. {breed}" for idx, breed in enumerate(popular_cat_breeds)]

# Функции для работы с событиями и окружающей средой
def get_environmental_text():
    environmental_url = "https://greenmystery.ru/blog/ecologia_problems/"
    environmental_response = requests.get(environmental_url)
    environmental_response.raise_for_status()
    soup = BeautifulSoup(environmental_response.text, 'html.parser')
    environmental_text = soup.find(class_="WYSIWYG").text
    environmental_text = environmental_text.replace("\n", "")
    return environmental_text

def get_event_of_the_day():
    day = datetime.now().day
    events = {
        1: "1 числа января 1959 года: запущена первая собака в космос — Лайка.",
        2: "2 числа февраля 1960 года: установлен мировой рекорд для самого быстрого гепарда.",
        3: "3 числа марта 1971 года: в Австралии началась программа защиты кенгуру.",
        4: "4 числа апреля 2001 года: в зоопарке Лондона родился первый белый медведь.",
        5: "5 числа мая 1985 года: в Калифорнии была основана организация по охране морских млекопитающих.",
        6: "6 числа июня 1995 года: зарегистрирован новый вид черепах в Бразилии.",
        7: "7 числа июля 2003 года: прошла первая выставка экзотических животных в России.",
        8: "8 числа августа 2012 года: в зоопарке Новой Зеландии родился редкий вид попугая.",
        9: "9 числа сентября 2015 года: был открыт новый заповедник для диких животных в Африке.",
        10: "10 числа октября 2008 года: в Китае был найден новый вид ящериц.",
        11: "11 числа ноября 2014 года: в Индии прошла конференция по охране тигров.",
        12: "12 числа декабря 1999 года: в Австралии зарегистрирована новая порода собак.",
        13: "13 числа января 2000 года: в зоопарке Сиднея родился первый в мире белый тигр.",
        14: "14 числа февраля 2011 года: была создана первая в мире ферма для диких животных.",
        15: "15 числа марта 2007 года: был найден новый вид рыб в Индийском океане.",
        16: "16 числа апреля 1992 года: в мире стало известно о новой породе лошадей.",
        17: "17 числа мая 2005 года: в зоопарке Токио родился первый в мире белый медведь.",
        18: "18 числа июня 1998 года: была открыта первая в мире клиника по охране диких животных.",
        19: "19 числа июля 2004 года: в Калифорнии прошел первый день защиты дельфинов.",
        20: "20 числа августа 2013 года: в Новой Зеландии был зарегистрирован новый вид морских свинок.",
        21: "21 числа сентября 1990 года: в Бразилии началась программа по охране ягуаров.",
        22: "22 числа октября 2016 года: в Китае зарегистрирована новая порода овец.",
        23: "23 числа ноября 2001 года: в зоопарке Лондона родился первый черный жираф.",
        24: "24 числа декабря 2010 года: в зоопарке Нью-Йорка родился первый в мире белый носорог.",
        25: "25 числа января 2002 года: в Китае была найдена новая порода тигров.",
        26: "26 числа февраля 2009 года: прошел первый международный день защиты пингвинов.",
        27: "27 числа марта 2015 года: в зоопарке Токио родилась первая в мире панда с искусственным оплодотворением.",
        28: "28 числа апреля 1993 года: в Австралии зарегистрирована новая порода крокодилов.",
        29: "29 числа мая 2006 года: в Новой Зеландии был найден новый вид пингвинов.",
        30: "30 числа июня 1994 года: в мире зарегистрирована новая порода лемуров.",
        31: "31 числа июля 2008 года: в Бразилии открыта первая в мире ферма по разведению морских свинок."
    }
    return events.get(day, "Нет события на этот день.")

# Инициализация пользователя
user_start_greeted = []
user_states = {}
user_sent_messages = defaultdict(list)

# Обработчики команд и кнопок
@bot.message_handler(commands=['start'])
def button(message):
    if message.from_user.id not in user_start_greeted:
        bot.send_message(message.chat.id, 'Привет! Я бот, который расскажет тебе информацию о животных или предложит факт дня!')
        user_start_greeted.append(message.from_user.id)

    show_main_buttons(message.chat.id)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    chat_id = call.message.chat.id
    # Удаляем старые сообщения
    for msg_id in user_sent_messages[chat_id]:
        try:
            bot.delete_message(chat_id, msg_id)
        except telebot.apihelper.ApiTelegramException:
            pass
    user_sent_messages[chat_id].clear()

    # Основной разметка
    back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))

    if call.data == 'question_1':
        msg = bot.send_message(call.message.chat.id, "Введите название животного для поиска на Википедии:")
        bot.register_next_step_handler(msg, search_animal)
        user_sent_messages[chat_id].append(msg.message_id)
    elif call.data == 'question_2':
        user_states[chat_id] = 'waiting_for_dog_breed'
        dog_breeds = get_dog_breeds()
        msg = bot.send_message(chat_id, f"Популярные породы собак:\n" + '\n'.join(dog_breeds) + "\nВведите номер породы для получения информации:", reply_markup=back_markup)
        user_sent_messages[chat_id].append(msg.message_id)
    elif call.data == 'question_3':
        user_states[chat_id] = 'waiting_for_cat_breed'
        cat_breeds = get_cat_breeds()
        msg = bot.send_message(chat_id, f"Популярные породы кошек:\n" + '\n'.join(cat_breeds) + "\nВведите номер породы для получения информации:", reply_markup=back_markup)
        user_sent_messages[chat_id].append(msg.message_id)
    elif call.data == 'question_4':
        fact_of_the_day = get_event_of_the_day()
        msg = bot.send_message(call.message.chat.id, fact_of_the_day, reply_markup=back_markup)
        user_sent_messages[chat_id].append(msg.message_id)
    elif call.data == 'question_5':
        environmental_text = get_environmental_text()
        msg = bot.send_message(call.message.chat.id, f"Информация о спасении животных:\n{environmental_text}", reply_markup=back_markup)
        user_sent_messages[chat_id].append(msg.message_id)
    elif call.data == 'back':
        # Убираем состояние при возврате назад
        user_states.pop(chat_id, None)
        show_main_buttons(chat_id)

# Пример изменения в функции search_animal
def search_animal(message):
    animal_name = message.text
    animal_info = get_animal_paragraph_and_image(animal_name)

    paragraphs = [clean_text(paragraph) for paragraph in animal_info['info']]
    back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))

    if animal_info['image_url']:
        caption = paragraphs[0][:1024]
        sent_message = bot.send_photo(message.chat.id, animal_info['image_url'], caption=caption)
        user_sent_messages[message.chat.id].append(sent_message.message_id)
        # Сохраняем идентификатор сообщения
        msg = bot.send_message(message.chat.id, "Вы можете нажать 'Назад', чтобы удалить это сообщение.")
        user_sent_messages[message.chat.id].append(msg.message_id)
        for paragraph in paragraphs[1:]:
            msg = bot.send_message(message.chat.id, paragraph)
            user_sent_messages[message.chat.id].append(msg.message_id)

        # Отправка ссылки на статью
        if animal_info['article_url']:
            msg = bot.send_message(message.chat.id, f"Читать далее: {animal_info['article_url']}")
            user_sent_messages[message.chat.id].append(msg.message_id)
    else:
        for paragraph in paragraphs:
            msg = bot.send_message(message.chat.id, paragraph)
            user_sent_messages[message.chat.id].append(msg.message_id)

        # Отправка ссылки на статью
        if animal_info['article_url']:
            msg = bot.send_message(message.chat.id, f"Читать далее: {animal_info['article_url']}")
            user_sent_messages[message.chat.id].append(msg.message_id)

    # Отправка кнопки "Назад"
    msg = bot.send_message(message.chat.id, "Что-то еще?", reply_markup=back_markup)
    user_sent_messages[message.chat.id].append(msg.message_id)

def show_main_buttons(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('🔎поиск животного🔎', callback_data='question_1')
    item2 = types.InlineKeyboardButton('🐶породы собак🐶', callback_data='question_2')
    item3 = types.InlineKeyboardButton('🐱породы кошек🐱', callback_data='question_3')
    item4 = types.InlineKeyboardButton('📃факт дня📃', callback_data='question_4')
    item5 = types.InlineKeyboardButton('🏗спасение животных🌍', callback_data='question_5')
    markup.add(item, item2, item3, item4, item5)
    msg = bot.send_message(chat_id, "Выберите действие:", reply_markup=markup)
    user_sent_messages[chat_id].append(msg.message_id)

def search_animal_by_breed(message, breed_name):
    animal_info = get_animal_paragraph_and_image(breed_name)

    paragraphs = [clean_text(paragraph) for paragraph in animal_info['info']]
    if animal_info['image_url']:
        bot.send_photo(message.chat.id, animal_info['image_url'], caption=paragraphs[0][:1024])
        for paragraph in paragraphs[1:]:
            bot.send_message(message.chat.id, paragraph)
    else:
        bot.send_message(message.chat.id, f"Информация о породе: {breed_name}")
        for paragraph in paragraphs:
            bot.send_message(message.chat.id, paragraph)

    # Отправка ссылки на статью
    if animal_info['article_url']:
        bot.send_message(message.chat.id, f"Читать далее: {animal_info['article_url']}")


@bot.callback_query_handler(func=lambda call: call.data == 'question_2')
def handle_dog_breed_query(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = 'waiting_for_dog_breed'
    dog_breeds = get_dog_breeds()
    back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))

    msg = bot.send_message(chat_id, f"Популярные породы собак:\n" + '\n'.join(dog_breeds), reply_markup=back_markup)
    user_sent_messages[chat_id] = [msg.message_id]

@bot.callback_query_handler(func=lambda call: call.data == 'question_3')
def handle_cat_breed_query(call):
    chat_id = call.message.chat.id
    user_states[chat_id] = 'waiting_for_cat_breed'
    cat_breeds = get_cat_breeds()
    back_markup = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))

    msg = bot.send_message(chat_id, f"Популярные породы кошек:\n" + '\n'.join(cat_breeds), reply_markup=back_markup)
    user_sent_messages[chat_id] = [msg.message_id]

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == 'waiting_for_dog_breed')
def handle_dog_breed_selection(message):
    chat_id = message.chat.id
    dog_breeds = get_dog_breeds()
    try:
        number = int(message.text) - 1
        if 0 <= number < len(dog_breeds):
            breed_name = re.sub(r'^\d+\.\s*', '', dog_breeds[number])
            show_dog_breed_info(message, breed_name)
        else:
            bot.send_message(chat_id, "Номер породы вне диапазона. Попробуйте снова.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный номер породы.")

@bot.message_handler(func=lambda message: message.chat.id in user_states and user_states[message.chat.id] == 'waiting_for_cat_breed')
def handle_cat_breed_selection(message):
    chat_id = message.chat.id
    cat_breeds = get_cat_breeds()
    try:
        number = int(message.text) - 1
        if 0 <= number < len(cat_breeds):
            breed_name = re.sub(r'^\d+\.\s*', '', cat_breeds[number])
            show_cat_breed_info(message, breed_name)
        else:
            bot.send_message(chat_id, "Номер породы вне диапазона. Попробуйте снова.")
    except ValueError:
        bot.send_message(chat_id, "Пожалуйста, введите корректный номер породы.")

def show_dog_breed_info(message, breed_name):
    animal_info = get_animal_paragraph_and_image(breed_name)
    paragraphs = [clean_text(paragraph) for paragraph in animal_info['info']]

    # Удаляем старые сообщения
    for msg_id in user_sent_messages[message.chat.id]:
        try:
            bot.delete_message(message.chat.id, msg_id)
        except telebot.apihelper.ApiTelegramException:
            pass

    if animal_info['image_url']:
        sent_photo_msg = bot.send_photo(message.chat.id, animal_info['image_url'], caption=paragraphs[0][:1024])
        user_sent_messages[message.chat.id].append(sent_photo_msg.message_id)
        for paragraph in paragraphs[1:]:
            msg = bot.send_message(message.chat.id, paragraph)
            user_sent_messages[message.chat.id].append(msg.message_id)

    # Кнопка "Назад"
    back_to_breeds_markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))
    msg = bot.send_message(message.chat.id, "Что-то еще?", reply_markup=back_to_breeds_markup)
    user_sent_messages[message.chat.id].append(msg.message_id)

def show_cat_breed_info(message, breed_name):
    animal_info = get_animal_paragraph_and_image(breed_name)
    paragraphs = [clean_text(paragraph) for paragraph in animal_info['info']]

    # Удаляем старые сообщения
    for msg_id in user_sent_messages[message.chat.id]:
        try:
            bot.delete_message(message.chat.id, msg_id)
        except telebot.apihelper.ApiTelegramException:
            pass

    if animal_info['image_url']:
        sent_photo_msg = bot.send_photo(message.chat.id, animal_info['image_url'], caption=paragraphs[0][:1024])
        user_sent_messages[message.chat.id].append(sent_photo_msg.message_id)
        for paragraph in paragraphs[1:]:
            msg = bot.send_message(message.chat.id, paragraph)
            user_sent_messages[message.chat.id].append(msg.message_id)

    # Кнопка "Назад"
    back_to_breeds_markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton('🔙Назад🔙', callback_data='back'))
    msg = bot.send_message(message.chat.id, "Что-то еще?", reply_markup=back_to_breeds_markup)
    user_sent_messages[message.chat.id].append(msg.message_id)


# Обработчики команд и кнопок
@bot.callback_query_handler(func=lambda call: call.data == 'back')
def handle_back(call):
    chat_id = call.message.chat.id
    # Удаляем сообщение с информацией о породе или животном
    if call.message.reply_to_message:
        try:
            bot.delete_message(chat_id, call.message.reply_to_message.message_id)
        except telebot.apihelper.ApiTelegramException:
            pass

    # Снова показываем основные кнопки
    show_main_buttons(chat_id)

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
