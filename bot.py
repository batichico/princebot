#!/usr/bin/env python3
from config import *
import importdir

importdir.do('plugins', globals())

#################################################
#                    POLLING                    #
#################################################

bot.polling()
