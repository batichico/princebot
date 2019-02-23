from config import *

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['chests'].items()])
def function_chests(m):
    cid = m.chat.id
    bot.send_message(cid, responses['m_chests'][lang(cid)])
