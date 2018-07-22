from config import *

@bot.message_handler(func = lambda m: m.text.lower() in [y for x, y in responses['registration'].items()])
def function_chests(m):
    cid = m.chat.id

    if m.chat.type != "private":
        click_kb = types.InlineKeyboardMarkup()
        click_button1 = types.InlineKeyboardButton(responses['registration_button'][lang(cid)], url = 't.me/principebetabot' )
        click_kb.row(click_button1)
        bot.send_message(cid, responses['private_registration'][lang(cid)], reply_markup=click_kb, disable_web_page_preview=True)
    else:
        bot.send_message(cid, responses['m_registration'][lang(cid)])
