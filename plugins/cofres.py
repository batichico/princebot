from config import *

@bot.message_handler(func = lambda m: m.text and m.text.lower() in [y for x, y in responses['chests'].items()])
def function_chests(m):
    cid = m.chat.id
    idUser = m.from_user.id
    name = ""
    lstPlayersTags = getPlayerTag(idUser)
    nextOnesStr = ""
    bestChestsStr = ""
    if len(lstPlayersTags)>0:
        for playerTag in lstPlayersTags:

            token = extra['crtoken']
            url = 'http://api.royaleapi.com/player/' + playerTag
            r = requests.get(url, headers={'auth': token})
            if r.status_code is 200:
                name= r.json()['name']
                if "_" in name.lower():
                    name = name.replace("_", "\_")
            url = 'http://api.royaleapi.com/player/' + playerTag + '/chests'
            r = requests.get(url, headers={'auth': token})
            if r.status_code is 200:
                data = r.json()
                #bot.send_message(cid,str(data))
                megaLightning = r.json()['megaLightning']
                magical = r.json()['magical']
                legendary = r.json()['legendary']
                epic = r.json()['epic']
                giant = r.json()['giant']
                upcoming = r.json()['upcoming']
            else:
                bot.send_message(cid, 'La API se ha caido')
                break
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

            bot.send_message(cid, messageText, parse_mode='markdown'  )
            nextOnesStr =""
    else:
        bot.send_message(cid, responses['a_not_registered'][lang(cid)])

def getPlayerTag (idUser):
    playerTagDB = ""
    playersTagsList = []
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
            playersTagsList.append(playerTagDB)
    else:
        row = cursor.fetchone()
        if row != None :
            playerTagDB = str(row["idCr"])
            if "#" in playerTagDB.lower():
                playerTagDB = playerTagDB.replace("#", "")
            playersTagsList.append(playerTagDB)

    cursor.close()
    conn.close()
    return playersTagsList
