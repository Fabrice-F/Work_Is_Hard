import math
import hashlib 
from flask import request
""" Comme les constantes n'existe pas en python:
en dehors de creer une classe avec getter setter
Nous avons créer ce fichier Constante&Tools où des méthodes
servent de constante ainsi que quelques méthodes outils"""

def CalculNbPageMax(numberPoste,nbPosteByPage):
    NbPageFloat = numberPoste / nbPosteByPage
    NbPage = math.ceil(NbPageFloat)
    return NbPage
    
def hashMdp(motdePassCLaire):
    h = hashlib.md5(motdePassCLaire.encode())
    return h.hexdigest()

def messageErrorConnexion():
    msg=f"""L'identifiant ou le mot de passe avec lesquels vous avez tenté de vous
    connecter est incorrect ..."""
    return msg

def getVisitorIp(requestRoute):
    return requestRoute.environ['REMOTE_ADDR']