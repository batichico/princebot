from config import *

import tradeosFunc

@bot.message_handler(commands=['tradeos'])
def tradeos(m):
  cid = m.chat.id
  idGrupo = cid
  idMessage = m.message_id
  idUsuario = m.from_user.id
  nombreCreador = m.from_user.first_name
  crearTradeo(idGrupo, idUsuario, nombreCreador)
  msg= bot.send_message(cid, 'Dime que carta quieres pedir')
  bot.register_next_step_handler(msg, step_pedirCarta)

def step_pedirCarta(m):
  cid = m.chat.id
  idUsuario = m.from_user.id
  idGrupo = cid
  peticion = m.text.lower()

  addPeticion(idGrupo, idUsuario, peticion)

  msg= bot.send_message(cid, 'Dime que cartas puedes ofrecer. Separa las cartas con "," ')
  bot.register_next_step_handler(msg, step_ofrecer)


def step_ofrecer(m):

  cid = m.chat.id
  idGrupo = cid
  userName = m.from_user.username
  idUsuario = m.from_user.id

  oferta = m.text.lower()
  addOferta(idGrupo,idUsuario,oferta)
  peticion, listaOfertas = leerDatos(idGrupo,idUsuario,0)

  arrayBotonesOfertas = []
  arrayNombresOfertas = []
  botoneraOfertas = types.InlineKeyboardMarkup()
  #aqui meto el codigo de listar  con * con listaOfertas
  for i in listaOfertas:
    arrayBotonesOfertas.append(types.InlineKeyboardButton(i,callback_data="{}|{}".format(i, idUsuario))) # mago 52033876
  botoneraOfertas.add(*arrayBotonesOfertas)

  msg = bot.send_message(cid, "{} quiere hacer un tradeo, el pide : {}".format(userName, peticion), reply_markup=botoneraOfertas, parse_mode="HTML")
  cambiarIdMensaje(idGrupo, idUsuario, msg.message_id)

@bot.callback_query_handler(func=lambda call: True)
def callback_handlerCuentas(call):
  carta, idUsuario = call.data.split('|') # carta = 'mago' | idUsuario = '52033876'
  cid = call.message.chat.id # id del chat
  mid = call.message.message_id # id del mensaje a editar
  nomusu = call.from_user.first_name # nombre del usuario pulsado
  idusu = call.from_user.id # id usuario pulsado
  texto = call.message.text # texto del mensaje a editar
  userName, peticion = getUsuarioPeticion(cid, idUsuario, mid)
  guardarOfertaNueva(cid, mid, nomusu, idusu, carta)
  texto_original = "{} quiere hacer un tradeo, el pide : {}".format(userName, peticion)
  nuevo_texto = getNuevoTexto(texto_original, cid, mid, idUsuario)
  peticion, listaOfertas = leerDatos(cid,idUsuario,mid)
  arrayBotonesOfertas = []
  arrayNombresOfertas = []
  botoneraOfertas = types.InlineKeyboardMarkup()
  for i in listaOfertas:
    arrayBotonesOfertas.append(types.InlineKeyboardButton(i,callback_data="{}|{}".format(i, idUsuario)))
  botoneraOfertas.add(*arrayBotonesOfertas)

  bot.edit_message_text(nuevo_texto, cid, mid, reply_markup=botoneraOfertas, parse_mode="HTML")
