import numpy as np

def alea(IX, IY, IZ):
  inter = 0.0
  # Opérations modulo pour maintenir IX, IY et IZ dans l'intervalle [0, 176]
  IX = 171*(IX % 177) - 2 * (IX // 177)
  IY = 172*(IY % 176) - 35 * (IY // 176)
  IZ = 170*(IZ % 178) - 63 * (IZ // 178)

  # Ajouter 30269, 30307 et 30323 si IX, IY ou IZ est négatif
  if IX < 0:
    IX += 30269
  if IY < 0:
    IY += 30307
  if IZ < 0:
    IZ += 30323
  # Calculer la valeur intermédiaire
  inter = (IX / 30269) + (IY / 30307) + (IZ / 30323)
  # Retourner la partie fractionnaire de la valeur intermédiaire et les nouvelles valeurs de IX, IY et IZ
  return [round(inter - int(inter), 4),IX,IY,IZ] 
