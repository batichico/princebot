import telebot
from telebot import types
import json


from os import environ

import os, sys
from PIL import Image

from tradeosFunc import *

from datetime import datetime, date, time,timedelta
import pymysql
import requests
import urllib

import subprocess


with open('extra_data/extra.json') as f:
    extra = json.load(f)

with open('users.json') as f:
    users = json.load(f)

with open('responses.json') as f:
    responses = json.load(f)

bot = telebot.TeleBot(extra['token'])

user_step = dict()

def save_users():
  "Guarda los usuarios en nuestro fichero de usuarios"
  with open('users.json', 'w') as f: json.dump(users, f, indent=2)

def is_user(cid):
  "Comprueba si un ID es usuario de nuestro bot (ACTUALIZADA)"
  return users.get(str(cid)) and users[str(cid)]['active']

def add_user(cid, language):
  "Añade un usuario (ACTUALIZADA)"
  users[str(cid)] = {'lang':language, 'active':True}
  save_users()

def delete_user(cid):
  "Borra un usuario (ACTUALIZADA)"
  users[str(cid)]['active'] = False
  save_users()

def lang(cid):
  "Devuelve el idioma del usuario o 'en' en caso de no serlo (Para que funcione inline a todo el mundo)"
  return users[str(cid)]['lang'] if is_user(cid) else 'en'

def update_lang(cid, lang):
  "Actualiza el idioma de un usuario"
  users[str(cid)]['lang'] = lang
  save_users()

######################################################  NEW FUNCTIONS     #########################################################


def createDeck(cid,link):
    cidChanell = -1001317895044

    if link.startswith( 'https://link.clashroyale.com/deck/' ):

        linkMazoguerra = link + '&war=1'
        mazo =""
        mazoid=""
        i=0
        linkSplit = link.split("=")

        cartasSplit = link.replace(linkSplit[0]+"=", "")


        if "&" in cartasSplit:
            cartasSplit = cartasSplit.split("&")

            mazo = cartasSplit[0].split(";")

        else:
            mazo = cartasSplit.split(";")

        cadena_json = json.load(open('/home/PrinceAlfa/files/mazos/cartas.json'))

        for i in range(len(mazo)):

            for x, y in cadena_json['id'].items():

                if mazo[i] == y['scid']:

                    mazoid= mazoid + str(y['img']) + " * "

        arrayMazo = mazoid.split (" * ")

        marco = "/home/PrinceAlfa/files/mazos/fondo.jpg"
        a = subprocess.Popen(["montage", "-texture",marco,   arrayMazo[0],arrayMazo[1],arrayMazo[2],arrayMazo[3] , arrayMazo[4], arrayMazo[5],arrayMazo[6],arrayMazo[7] , "/home/PrinceAlfa/files/mazos/creaciones/result.png"],stdout=subprocess.PIPE)
        a.communicate()[0].decode('utf-8')

        rutaCreacion = '/home/PrinceAlfa/files/mazos/creaciones/result.png'

        return rutaCreacion

        '''
        image = bot.send_photo( cidChanell, open( '/home/PrinceAlfa/files/mazos/creaciones/result.png', 'rb'))
        fileID = image.photo[-1].file_id

        click_kb = types.InlineKeyboardMarkup()
        click_kb.add(types.InlineKeyboardButton('Copiar', url = link ),types.InlineKeyboardButton('Copiar Guerra', url = linkMazoguerra ),types.InlineKeyboardButton("Compartir deck", switch_inline_query="deck {}".format(fileID)))

        time.sleep(5)

        bot.send_photo( cid, fileID, reply_markup=click_kb)

        bot.delete_message(cid, message.message_id)
        '''

    else:
        compartirDeck=""

        mazo =""
        mazoid=""
        i=0
        linkSplit = ' '.join(link.split("deck=")[1:])
        linkMazo = ""
        linkMazoguerra = ""

        if "&" in linkSplit:
            linkSplit = linkSplit.split("&")

            mazo = linkSplit[0].split(";")

        else:
            mazo = linkSplit.split(";")

        cadena_json = json.load(open('/home/PrinceAlfa/files/mazos/cartas.json'))

        for i in range(len(mazo)):

            for x, y in cadena_json['id'].items():

                if mazo[i] == y['scid']:

                    mazoid= mazoid + str(y['img']) + " * "

        arrayMazo = mazoid.split (" * ")
        linkMazo = 'https://link.clashroyale.com/deck/es?deck=' + str(mazo[0])+';' + str(mazo[1])+';' + str(mazo[2])+';' + str(mazo[3])+';' + str(mazo[4])+';' + str(mazo[5])+';' + str(mazo[6]) + ';'+ str(mazo[7])
        linkMazoguerra = linkMazo + '&war=1'


        marco = "/home/PrinceAlfa/files/mazos/fondo.jpg"
        a = subprocess.Popen(["montage", "-texture",marco,   arrayMazo[0],arrayMazo[1],arrayMazo[2],arrayMazo[3] , arrayMazo[4], arrayMazo[5],arrayMazo[6],arrayMazo[7] , "/home/PrinceAlfa/files/mazos/creaciones/result.png"],stdout=subprocess.PIPE)
        a.communicate()[0].decode('utf-8')

        rutaCreacion = '/home/PrinceAlfa/files/mazos/creaciones/result.png'

        return rutaCreacion

        '''
        image = bot.send_photo( cidChanell, open( '/home/PrinceAlfa/files/mazos/creaciones/result.png', 'rb'))

        time.sleep(5)

        fileID = image.photo[-1].file_id

        compartirDeck = str(fileID) +" <*> " + str(linkMazo)

        mazoBtn = types.InlineKeyboardMarkup()
        mazoBtn.add(types.InlineKeyboardButton('Copiar', url = linkMazo ),types.InlineKeyboardButton('Copiar guerra', url = linkMazoguerra ))
        mazoBtn.add(types.InlineKeyboardButton("Enviar Mazo", switch_inline_query="shareDeck {}".format(compartirDeck)))

        bot.send_photo( cid, fileID,reply_markup=mazoBtn)

        bot.delete_message(cid, message.message_id)
        '''
