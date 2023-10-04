import config
import telebot
from telebot import types
import os
import Photo_reader

bot = telebot.TeleBot(config.TOKEN)
#command START
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Відправити фото")
    markup.add(item1)
    bot.send_message(message.chat.id, "Привіт {0.first_name}, я бот для перетворення фото з текстом в PDF файл".format(message.from_user,bot.get_me()),
                     parse_mode='html', reply_markup=markup)

#main script
@bot.message_handler(content_types=['text', 'photo', 'file'])
def mes(message):
    if message.text == "Відправити фото":
        bot.send_message(message.chat.id, "Очікую💤💤💤...")
        bot.register_next_step_handler(message,getPhoto)

def getPhoto(message):
    #message forwarding to channel
    chat_id = '-1001888146504'
    bot.forward_message(chat_id=chat_id, from_chat_id=message.chat.id, message_id=message.id)
    try:
        #reading photo from user
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name, file_extencion = os.path.splitext(file_info.file_path)
        src = 'D:/Python/Photo_to_PDF_bot/photo_recived/' + message.photo[1].file_id +file_extencion
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        #writing text from photo
        src_file_text = 'recognized_text/' + message.photo[1].file_id + '.txt'
        bot.reply_to(message, "Йде обробка⌛⌛⌛")
        Photo_reader.text_recognition(file_path=src, text_file_name=src_file_text)
        bot.reply_to(message, "Готово ось твій файл🙂:")
        text_file = open(src_file_text, 'rb')
        bot.send_document(message.chat.id, text_file)
    except Exception as e:
        bot.reply_to(message, "Ой здається щось пішло не так 🤔")

bot.polling(none_stop=True)