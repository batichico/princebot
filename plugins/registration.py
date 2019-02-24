from config import *

idUser = 0
hoy = date.today()
name = ""
nickname = ""
tag = ""
usuario=[]

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['registration'].items()])
def function_chests(m):
    cid = m.chat.id
    if m.chat.type != "private":
        click_kb = types.InlineKeyboardMarkup()
        click_button1 = types.InlineKeyboardButton(responses['registration_button'][lang(cid)], url = 't.me/principebetabot' )
        click_kb.row(click_button1)
        bot.send_message(cid, responses['private_registration'][lang(cid)], reply_markup=click_kb, disable_web_page_preview=True)
    else:
        msg=bot.send_message(cid, responses['m_registration'][lang(cid)])
        bot.register_next_step_handler(msg, step_registration)

def step_registration(m):
    global idUser, hoy, name, nickname,tag,usuario
    cid = m.chat.id
    idUser = m.from_user.id
    hoy = datetime.now()
    nun = m.from_user.username
    name = m.from_user.first_name
    nickname = nun
    registrado = False
    estaRegistrado = False
    if (m.from_user.username is None):
        nun = m.new_chat_member.first_name
        if (m.from_user.last_name is not None):
            nun += " "
            nun += m.from_user.last_name
        bot.send_message(cid, "{} {}".format(m.from_user.username, m.from_user.last_name))
    else:
        nun = m.from_user.username
    nunS =  str(nun)
    bot.send_message(cid, responses['a_checking_tag'][lang(cid)])
    tag=m.text
    if "#" in tag.lower():
        tag = tag.replace("#", "")

    estaRegistrado = isDuplicateInDB(tag)

    if estaRegistrado == True:
        bot.send_message(cid,responses['a_is_duplicated'][lang(cid)].format(tag))
    else:
        nombre = tag
        token = extra['crtoken']
        url = 'http://api.royaleapi.com/player/' + nombre
        r = requests.get(url, headers={'auth': token})
        if r.status_code is 200:
            name= r.json()['name']
            if "_" in name.lower():
                name = name.replace("_", "\_")
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton(responses['btn_acept'][lang(cid)], callback_data='acept'),
            types.InlineKeyboardButton(responses['btn_cancel'][lang(cid)], callback_data='cancel'))

            bot.send_message(cid,responses['a_is_duplicated'][lang(cid)].format(name), reply_markup=keyboard, disable_web_page_preview=True)
        else:
            bot.send_message(cid, responses['a_tag_not_exist'][lang(cid)])

@bot.callback_query_handler(func=lambda call: call.data in ['acept', 'cancel'])
def callback_handler(call):
  cid = call.message.chat.id
  mid = call.message.message_id
  calculo = call.data
  global idUser, hoy, name, nickname,tag, usuario
  if calculo == 'acept':

      msg=bot.edit_message_text(responses['a_validation_acept'][lang(cid)],cid,mid,reply_markup=None)

      bot.send_photo( cid, open( '/home/PrinceAlfa/files/accountExample/accountExample.jpg', 'rb'))

      conn = pymysql.connect(user=extra['userDB'], password=extra['userPassDB'],
                                 host=extra['hostDB'],
                                 database=extra['database'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

      x = conn.cursor()
      x.execute("""INSERT INTO Player (idTelegram, idCr,  nicknameTelegram, name,idGroup,fechaRegis,validado )
                 VALUES (%s,%s,%s,%s,%s,%s,%s)""",(idUser,tag,nickname,name,1,hoy,0))
      conn.commit()


      x.close()
      conn.close()
      bot.register_next_step_handler(msg, step_validation)

  elif calculo == 'cancel':

      bot.edit_message_text(responses['a_validation_cancel'][lang(cid)],cid,mid,reply_markup=None)


def step_validation(m):
    cid = m.chat.id
    idUser = m.from_user.id

    if m.photo == None :
        bot.send_message(cid,'Envíame una foto, para poder validar tu cuenta. Tu cuenta queda pendiente de validación hasta que envíes una captura de tu perfil de Clash Royale')

    else:

        fileID = m.photo[-1].file_id
        file_info = bot.get_file(fileID)
        downloaded_file = bot.download_file(file_info.file_path)
        with open("/home/PrinceAlfa/files/newAccounts/newAccount.jpg", 'wb') as new_file:
              new_file.write(downloaded_file)
        path = "/home/PrinceAlfa/files/newAccounts/newAccount.jpg"

        ocr_found = json.loads(ocr_space_file(path))
        lines = ocr_found['ParsedResults'][0]['TextOverlay']['Lines']

        texto_completo = ""
        crTag=""
        for line in lines:
          text_line = str(line['Words'][0]['WordText'])
          if "*" in text_line:
            text_line = text_line.replace("*", "#")
            crTag = text_line
            break
          texto_completo += " " + text_line

          #bot.send_message(chat_id=m.chat.id, text=text_line)
        #bot.send_message(chat_id=m.chat.id, text="El texto completo es " + texto_completo)
        if "#" in crTag.lower():
            crTag = crTag.replace("#", "")

        try:
            respuesta= tagValidation(crTag,idUser)
        except:
            respuesta = "no valido"


        if respuesta == "validado":

            bot.send_message(cid, "Tu tag es: "+ str(crTag))
            bot.send_message(cid,'Ya estas registrado y validado, amig@:)\nYa puedes utilizar los comandos de cr ;)\n \nPulsa el comando /me para ver tus datos de jugador y !cofres para ver el ciclo de cofres')
        else:

            bot.send_message(cid,'La imagen que envías es incorrecta, prueba a sacarla igual que el ejemplo :)')


@bot.message_handler(commands=['ocr'], func=lambda m: m.reply_to_message and m.reply_to_message.photo)
def user_image(m):
  cid = m.chat.id

  fileID = m.reply_to_message.photo[-1].file_id
  file_info = bot.get_file(fileID)
  downloaded_file = bot.download_file(file_info.file_path)
  with open("/home/PrinceAlfa/files/newAccounts/newAccount.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
  path = "/home/PrinceAlfa/files/newAccounts/newAccount.jpg"

  ocr_found = json.loads(ocr_space_file(path))
  lines = ocr_found['ParsedResults'][0]['TextOverlay']['Lines']

  texto_completo = ""
  crTag = ""
  for line in lines:
    text_line = str(line['Words'][0]['WordText'])
    if "*" in text_line:
      text_line = text_line.replace("*", "#")
      crTag = text_line

    if text_line.startswith("8"):
      tag = list(text_line)
      tag[0] = "#"
      "".join(tag)

    texto_completo += " " + text_line

    bot.send_message(chat_id=m.chat.id, text=text_line)
  bot.send_message(chat_id=m.chat.id, text="El texto completo es " + texto_completo)
  if "#" in crTag.lower():
      crTag = crTag.replace("#", "")

  #tagComparation(crTag)
  bot.send_message(cid, "Tu tag es: "+ str(crTag))

def ocr_space_file(filename, overlay=True, api_key= extra['ocrtoken'], language='spa'):


    payload = {'isOverlayRequired': overlay,
               'apikey':  extra['ocrtoken'],
               'language': 'spa',
               }
    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )
    return r.content.decode()
def tagValidation(tag,idUser):
    conn = pymysql.connect(user=extra['userDB'], password=extra['userPassDB'],
                             host=extra['hostDB'],
                             database=extra['database'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

    cursor = conn.cursor()
    sql = "SELECT  idCr FROM Player WHERE idTelegram = %s "
    cursor.execute(sql,(idUser))
    row = cursor.fetchone()
    bdTag = str(row["idCr"])
    arrayBDTag = list(bdTag)
    arrayPhotoTag = list(tag)
    count = 0
    respuesta = ""
    for i in range(len(arrayBDTag)):
        if arrayBDTag[i] == arrayPhotoTag[i]:
            count= count+1
    porcentaje = len(arrayBDTag) - count
    if porcentaje < len(arrayBDTag)/2 :
        sql = "UPDATE Player SET validado=1 WHERE idTelegram= %s AND idCr = %s"
        cursor.execute(sql,(idUser,bdTag))
        respuesta =  "validado"
        conn.commit()
        cursor.close()
        conn.close()
    else:
        respuesta = "no validado"
    return respuesta

####################Functions registro #############################

def isDuplicateInDB(tag):
    registrado = False
    playerTagDB = ""
    conn = pymysql.connect(user=extra['userDB'], password=extra['userPassDB'],
                             host=extra['hostDB'],
                             database=extra['database'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()
    sql = "SELECT  idCr FROM Player WHERE idTelegram = %s "
    cursor.execute(sql,(idUser))
    if cursor.execute(sql,(idUser)) > 1:
        row = cursor.fetchall()
        for i in range(len(row)):
            playerTagDB = str(row[i]["idCr"])
            if "#" in playerTagDB.lower():
                playerTagDB = playerTagDB.replace("#", "")
            if tag == playerTagDB :
                registrado = True
            else :
                registrado = False
    elif  cursor.execute(sql,(idUser)) == 0:
        registrado = False
    else:
        row = cursor.fetchone()
        playerTagDB = str(row["idCr"])
        if "#" in playerTagDB.lower():
            playerTagDB = x.replace("#", "")
        if tag == playerTagDB :
            registrado = True
    cursor.close()
    conn.close()
    return registrado
