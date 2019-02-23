from config import *

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['clanwar'].items()])
def function_chests(m):

    cid = m.chat.id
    bot.send_message(cid, responses['m_clanwar'][lang(cid)])

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['war'].items()])
def function_chests(m):

    cid = m.chat.id
    bot.send_message(cid, responses['m_war'][lang(cid)])

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['recolection'].items()])
def function_chests(m):

    cid = m.chat.id
    bot.send_message(cid, responses['m_recolection'][lang(cid)])
