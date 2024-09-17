import telebot
from telebot import types
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def button(message) :
    markup = types.InlineKeyboardMarkup(row_width=2)
    item = types.InlineKeyboardButton('поиск животного', callback_data='question_1')
    item2 = types.InlineKeyboardButton('породы собак', callback_data='question_2')
    item3 = types.InlineKeyboardButton('породы кошек', callback_data='question_3')
    item4 = types.InlineKeyboardButton('факт дня', callback_data='question_4')
    markup.add(item, item2, item3, item4)
    bot.send_message(message.chat.id, 'Привет,я бот который с радостю тебе расскажет факты о животных или факт дня!', reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callback(call):
    if call.message:
        if call.data == 'question_1':
            # Создается новая клавиатура с кнопкой "Назад"
            back_markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('Назад', callback_data='back')
            back_markup.add(back_button)

            # Редактируется сообщение, убираются старые кнопки и добавляется кнопка "Назад"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Введите название животного для поиска.\nНажмите 'Назад' для возврата.",
                                  reply_markup=back_markup)

        elif call.data == 'question_2':
            # Создается новая клавиатуру с кнопкой "Назад"
            back_markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('Назад', callback_data='back')
            back_markup.add(back_button)

            # Редактируется сообщение, показываем информацию о собаках и кнопку "Назад"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Вот популярные породы собак:\nНажмите 'Назад' для возврата.",
                                  reply_markup=back_markup)

        elif call.data == 'question_3':
            # Создается новая клавиатуру с кнопкой "Назад"
            back_markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('Назад', callback_data='back')
            back_markup.add(back_button)

            # Редактируется сообщение, показывает информацию о кошках и кнопку "Назад"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Вот популярные породы кошек:\nНажмите 'Назад' для возврата.",
                                  reply_markup=back_markup)

        elif call.data == 'question_4':
            # Создается новая клавиатуру с кнопкой "Назад"
            back_markup = types.InlineKeyboardMarkup(row_width=1)
            back_button = types.InlineKeyboardButton('Назад', callback_data='back')
            back_markup.add(back_button)

            # Редактируется сообщение, показывается факт дня и кнопку "Назад"
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Факт дня:\nНажмите 'Назад' для возврата.",
                                  reply_markup=back_markup)

        elif call.data == 'back':
            # Восстанавливаются изначальные кнопки
            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton('Поиск животного', callback_data='question_1')
            item2 = types.InlineKeyboardButton('Породы собак', callback_data='question_2')
            item3 = types.InlineKeyboardButton('Породы кошек', callback_data='question_3')
            item4 = types.InlineKeyboardButton('Факт дня', callback_data='question_4')

            markup.add(item1, item2, item3, item4)

            # возвращаются старые кнопки
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Привет! Я крутой чел), который с радостью расскажет тебе информацию о животных о животных или предложит факт дня!",
                                  reply_markup=markup)

# Запуск бота
bot.polling(none_stop=True)