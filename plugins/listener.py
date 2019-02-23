from config import *

def listener(messages):
    for m in messages:
        userName = m.from_user.first_name
        userId = m.from_user.id
        logMessage = userName + " " + str(userId) + " said: "  + m.text
        print(logMessage)


bot.set_update_listener(listener)
