from config import *

def crearTradeo (idGrupo, idUsuario, nombreCreador):
  file_path = "tradeos/"+str(idGrupo)+".json"
  directory = os.path.dirname(file_path)
  idGrupoJSON = [idGrupo]
  ofrece = []
  pide = ""
  img = 31231223123
  meterTrade = {'idGrupo':idGrupoJSON, 'ofrece':ofrece, 'pide':pide, 'img':img, 'idMessage':0, 'idCreador':idUsuario, 'nombreCreador':nombreCreador, 'ofertas_gente': []}
  if not os.path.exists(directory):
    os.makedirs(directory)
  if os.path.isfile(file_path):
    with open(file_path, "r") as jsonFile:
      data = json.load(jsonFile)
    data.append(meterTrade)
    with open(file_path, "w") as outfile:
      json.dump(data, outfile, indent=4)
  else:
    with open(file_path, "w") as outfile:
      json.dump([meterTrade], outfile, indent=4)


def getOfertas(idGrupo, idMessage, idUsuario):
  file_path = "tradeos/"+str(idGrupo)+".json"
  with open(file_path, "r+") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == int(idMessage) and x.get('idCreador') == int(idUsuario):
      return x.get('ofertas_gente')
  return None


def getNuevoTexto(texto_original, idGrupo, idMessage, idUsuario):
  ofertas = getOfertas(idGrupo, idMessage, idUsuario)
  texto_extra = ""
  for x in ofertas:
    if x.get('cartas'):
      texto_extra += "{}: {}\n".format(x.get('nombreUsuario'), ', '.join(x.get('cartas')))
  texto_nuevo = "{}\n\n{}".format(texto_original, texto_extra)
  return texto_nuevo


def guardarOfertaNueva(idGrupo, idMessage, nombreUsuario, idUsuario, carta):
  file_path = "tradeos/"+str(idGrupo)+".json"
  with open(file_path, "r+") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == int(idMessage): # Buscamos el tradeo
      ofertas = x.get('ofertas_gente')# Obtenemos sus ofertas
      ids = [y.get('idUsuario') for y in ofertas] if ofertas else []
      borrarUsu = {}
      if idUsuario in ids:
        for y in ofertas: # Recorremos la ofertas
          if int(idUsuario) == int(y.get('idUsuario')): # Si el usuario ya ha ofrecido algo
            if carta not in y.get('cartas'):
              y['cartas'].append(carta)
            else:
              y['cartas'].remove(carta)
            if not y.get('cartas'):
              borrarUsu = y
        if borrarUsu:
          ofertas.remove(borrarUsu)
      else:
        ofertas.append({
            'nombreUsuario': nombreUsuario,
            'cartas':[carta],
            'idUsuario': int(idUsuario)
        })
      x['ofertas_gente'] = ofertas
  with open(file_path, "w") as outfile:
    json.dump(data, outfile, indent=4)


def getUsuarioPeticion(idGrupo, idUsuario, idMessage):
  file_path = "tradeos/"+str(idGrupo)+".json"
  with open(file_path, "r+") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == int(idMessage) and x.get('idCreador') == int(idUsuario):
      return x.get('nombreCreador'), x.get('pide')


def addOferta(idGrupo,idUsuario,nombreCarta):
  file_path = "tradeos/"+str(idGrupo)+".json"
  with open(file_path, "r+") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == 0 and x.get('idCreador') == idUsuario:
      x["ofrece"] = [y.strip() for y in nombreCarta.split(',')]

  with open(file_path, "w") as outfile:
    json.dump(data, outfile, indent=4)



def addPeticion(idGrupo,idUsuario,peticion):
  file_path = "tradeos/"+str(idGrupo)+".json"
  directory = os.path.dirname(file_path)

  with open(file_path, "r+") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == 0 and x.get('idCreador') == idUsuario:
      x["pide"] = peticion

  with open(file_path, "w") as outfile:
      json.dump(data, outfile, indent=4)


def leerDatos(idGrupo,idUsuario,idMessage):
  file_path = "tradeos/"+str(idGrupo)+".json"
  with open(file_path, "r") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == int(idMessage) and x.get('idCreador') == int(idUsuario):
      peticion = x['pide']
      oferta = x['ofrece']
  print("peticion " +peticion)
  print(oferta)

  return peticion,oferta



def cambiarIdMensaje(idGrupo, idUsuario, idMessage):

  file_path = "tradeos/"+str(idGrupo)+".json"

  with open(file_path, "r") as jsonFile:
    data = json.load(jsonFile)
  for x in data:
    if x.get('idMessage') == 0 and x.get('idCreador') == idUsuario:
      x['idMessage'] = idMessage

  with open(file_path, "w") as outfile:
    json.dump(data, outfile, indent=4)

#crearTradeo(idGrupo,idMessage)

#addOferta(idGrupo,idMessage,nombreCarta)

#addPeticion(idGrupo,idMessage,peticion)

#cambiarIdMensaje(idMessage)

#datos = leerDatos(idGrupo,idMessage)

#print(datos)
