from config import *

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['command_my_info'].items()])
def function_my_info(m):
    cid = m.chat.id
    idUser = m.from_user.id
    name = ""
    lstPlayersInfo = getPlayerTag(idUser)
    accountsKeyBoard = types.InlineKeyboardMarkup()
    arrayButtonsAccounts = []
    if len(lstPlayersInfo)>0:
        for playerInfo in lstPlayersInfo:
            arrayButtonsAccounts.append(types.InlineKeyboardButton(playerInfo[0],callback_data="playerInfo / "+playerInfo[0]+" / "+playerInfo[1]))
        accountsKeyBoard.add(*arrayButtonsAccounts,types.InlineKeyboardButton('Volver', callback_data='ver'))
        bot.send_message(cid,responses['name_accounts'][lang(cid)], reply_markup=accountsKeyBoard)
    else:
        bot.send_message(cid, responses['a_not_registered'][lang(cid)])

@bot.callback_query_handler(func=lambda call: call.data in ['playerMenu'])
def callback_player_menu(call):
    cid = call.message.chat.id
    mid = call.message.message_id
    callInfo = call.data
    idUser =  call.from_user.id
    accountsKeyBoard = types.InlineKeyboardMarkup()
    arrayButtonsAccounts = []
    lstPlayersInfo = getPlayerTag(idUser)
    if len(lstPlayersInfo)>0:
        for playerInfo in lstPlayersInfo:
            arrayButtonsAccounts.append(types.InlineKeyboardButton(playerInfo[0],callback_data="playerInfo / "+playerInfo[0]+" / "+playerInfo[1]))
        accountsKeyBoard.add(*arrayButtonsAccounts,types.InlineKeyboardButton('Volver', callback_data='ver'))
        bot.send_message(cid,responses['name_accounts'][lang(cid)], reply_markup=accountsKeyBoard)
    else:
        bot.send_message(cid, responses['a_not_registered'][lang(cid)])

@bot.callback_query_handler(func=lambda call: call.data.startswith('playerInfo'))
def callback_player_Info(call):
      cid = call.message.chat.id
      mid = call.message.message_id
      callInfo = call.data
      idUser =  call.from_user.id
      nameCr = callInfo.split(" / ")[1]
      idCr = callInfo.split(" / ")[2]

      playerMenuKeyboard = types.InlineKeyboardMarkup()
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_info'][lang(cid)],  callback_data='info / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_chests'][lang(cid)],  callback_data='chests / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_war_level'][lang(cid)],  callback_data='warLevel / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_games_history'][lang(cid)],  callback_data='gamesHistory / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_clan'][lang(cid)],  callback_data='clan / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_decks'][lang(cid)],  callback_data='decks / '+nameCr+' / '+idCr ))
      playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_return'][lang(cid)],  callback_data='playerMenu' ))

      messageText= responses['menu_player_message'][lang(cid)].format(nameCr)
      bot.edit_message_text(messageText,cid,mid,reply_markup=playerMenuKeyboard , parse_mode='markdown'  )

@bot.callback_query_handler(func=lambda call: call.data.startswith('chests'))
def callback_player_info_chests(call):

    cid = call.message.chat.id
    mid = call.message.message_id
    callInfo = call.data
    idUser =  call.from_user.id
    nameCr = callInfo.split(" / ")[1]
    idCr = callInfo.split(" / ")[2]
    messageText = ""
    name = ""

    playerMenuKeyboard = types.InlineKeyboardMarkup()
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_info'][lang(cid)],  callback_data='info / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_chests'][lang(cid)],  callback_data='chests / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_war_level'][lang(cid)],  callback_data='warLevel / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_games_history'][lang(cid)],  callback_data='gamesHistory / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_clan'][lang(cid)],  callback_data='clan / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_decks'][lang(cid)],  callback_data='decks / '+nameCr+' / '+idCr ))
    playerMenuKeyboard.add(types.InlineKeyboardButton(responses['menu_player_name_return'][lang(cid)],  callback_data='return' ))

    token = extra['crtoken']
    url = 'http://api.royaleapi.com/player/' + idCr + '/chests'
    r = requests.get(url, headers={'auth': token})
    if r.status_code is 200:
        data = r.json()
        megaLightning = r.json()['megaLightning']
        magical = r.json()['magical']
        legendary = r.json()['legendary']
        epic = r.json()['epic']
        giant = r.json()['giant']
        upcoming = r.json()['upcoming']
        nextOnesStr=""
        for chest in upcoming:
            if chest == "silver":
                chest = responses['name_silver_chest'][lang(cid)]
            if chest == 'gold':
                chest = responses['name_gold_chest'][lang(cid)]
            if chest == 'giant':
                chest = responses['name_giant_chest'][lang(cid)]
            if chest == 'magical':
                chest = responses['name_magical_chest'][lang(cid)]
            if chest == 'epic':
                chest = responses['name_epic_chest'][lang(cid)]
            if chest == 'megaLightning':
                chest = responses['name_mega_lightning_chest'][lang(cid)]
            if chest == 'legendary':
                chest = responses['name_legendary_chest'][lang(cid)]
            nextOnesStr = nextOnesStr + chest + ','

        megaLightningStr = '    *' + responses['name_mega_lightning_chest'][lang(cid)] +'*: ' + str(megaLightning)
        magicalStr = '    *' + responses['name_magical_chest'][lang(cid)] +'*: ' + str(magical)
        legendaryStr = '    *' + responses['name_legendary_chest'][lang(cid)] +'*: ' + str(legendary)
        epicgStr = '    *' + responses['name_epic_chest'][lang(cid)] +'*: ' + str(epic)
        giantStr = '    *' + responses['name_giant_chest'][lang(cid)] +'*: ' + str(giant)
        bestChestsStr = megaLightningStr + "\n" + magicalStr + "\n" + legendaryStr + "\n" +  epicgStr + "\n" +  giantStr
        messageText = name + ' ' + responses['name_chets'][lang(cid)] + ' 📦 :\n' + bestChestsStr + '\n    '+ responses['name_upcoming_chets'][lang(cid)] + ': ' + nextOnesStr

    else:
      messageText = responses['name_api_down'][lang(cid)])

    bot.edit_message_text(messageText,cid,mid,reply_markup=playerMenuKeyboard , parse_mode='markdown'  )

def getPlayerTag (idUser):
    playerTagDB = ""
    playerNameDB = ""
    playersInfoList = []
    conn = pymysql.connect(user=extra['userDB'], password=extra['userPassDB'],
                             host=extra['hostDB'],
                             database=extra['database'],
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    sql = "SELECT  idCr,name FROM Player WHERE idTelegram = %s "
    cursor.execute(sql,(idUser))

    if cursor.execute(sql,(idUser)) > 1:
        row = cursor.fetchall()
        for i in range(len(row)):
            playerTagDB = str(row[i]["idCr"])
            playerNameDB = str(row[i]["name"])
            if "#" in playerTagDB.lower():
                playerTagDB = playerTagDB.replace("#", "")
            playersInfoList.append([playerNameDB,playerTagDB])
    else:
        row = cursor.fetchone()
        if row != None :
            playerTagDB = str(row["idCr"])
            playerNameDB = str(row[i]["name"])
            if "#" in playerTagDB.lower():
                playerTagDB = playerTagDB.replace("#", "")
            playersInfoList.append([playerNameDB,playerTagDB])

    cursor.close()
    conn.close()
    return playersInfoList
