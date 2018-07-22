import telebot
from telebot import types
import json

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
