#!/usr/bin/env python3
from config import *
import importdir

importdir.do('plugins', globals())

#################################################
#                    POLLING                    #
#################################################

bot.send_message(239822769, "Bot encendido")
bot.polling()
