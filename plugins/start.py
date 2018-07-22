from config import *

@bot.message_handler(commands=['start'])
def start_handler(m):
    cid = m.chat.id
    if not is_user(cid):
        uid = m.from_user.id
        uname = m.from_user.first_name
        try:
            language = m.from_user.language_code[:2] if m.from_user.language_code[:2] in ['en', 'es'] else 'en'
        except:
            language = 'en'
        add_user(cid, language)
        bot.send_message(cid, responses['start'][language].format(uname, uid), parse_mode="Markdown")