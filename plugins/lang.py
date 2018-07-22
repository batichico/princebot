from config import *

keyboard = types.InlineKeyboardMarkup()
keyboard.add(types.InlineKeyboardButton('Español', callback_data='es'),
             types.InlineKeyboardButton('Inglés', callback_data='en'),
             types.InlineKeyboardButton('Euskera', callback_data='eus'))

keyboard_2 = types.InlineKeyboardMarkup()
keyboard_2.add(types.InlineKeyboardButton('Spanish', callback_data='es'),
             types.InlineKeyboardButton('English', callback_data='en'),
             types.InlineKeyboardButton('Euskera', callback_data='eus'))

@bot.message_handler(commands=['lang'], func=lambda m: is_user(m.chat.id))
def lang_handler(m):
  "Función para actualizar el idioma del bot"
  cid = m.chat.id
  bot.send_message(cid, responses['lang'][lang(cid)], reply_markup=keyboard if lang(cid) == 'es' else keyboard_2, parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: call.data in ['en', 'es','eus'])
def callback_handler(call):
    "Función para manejar el uso de los botones para cambiar el idioma"
    cid = call.message.chat.id
    mid = call.message.message_id
    language = call.data
    update_lang(cid, language)
    try:
        bot.edit_message_text(responses['lang_updated'][lang(cid)], cid, mid, reply_markup=keyboard if language == 'es' else keyboard_2, parse_mode="Markdown")
    except:
        pass
