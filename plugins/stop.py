from config import *

@bot.message_handler(commands=['stop'])
def stop_handler(m):
    cid = m.chat.id
    uid = m.from_user.id
    uname = m.from_user.first_name
    if is_user(cid):
        bot.send_message(cid, responses['stop'][lang(cid)].format(uname, uid), parse_mode="Markdown")
        delete_user(cid)