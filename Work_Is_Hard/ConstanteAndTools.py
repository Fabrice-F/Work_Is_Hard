import math
import hashlib
import random

from flask import request
from Classes import *
""" Comme les constantes n'existe pas en python:
en dehors de creer une classe avec getter setter
Nous avons créer ce fichier Constante&Tools où des méthodes
servent de constante ainsi que quelques méthodes outils"""


def CalculNbPageMax(numberPoste, nbPosteByPage):
    NbPageFloat = numberPoste / nbPosteByPage
    NbPage = math.ceil(NbPageFloat)
    return NbPage


def hashMdp(motdePassClaire):
    h = hashlib.md5(motdePassClaire.encode())
    return h.hexdigest()


def messageErrorConnexion():
    msg = """L'identifiant ou le mot de passe avec lesquels vous avez tenté de vous
    connecter sont incorrect ..."""
    return msg


def messageErrorChampsVide():
    msg = """L'un des champs que vous avez renseigné est vide ..."""
    return msg


def getVisitorIp(requestRoute):
    return requestRoute.environ['REMOTE_ADDR']


def MapSessionToUser(session):
    idUser = session["IdUtilisateur"]
    Pseudo = session["PseudoUtilisateur"]
    Nom = session["NomUtilisateur"]
    Prenom = session["PrenomUtilisateur"]
    Age = session["DateNaissanceUtilisateur"]
    IdRole = session["IdRoleUtilisateur"]
    User = Utilisateur(idUser, Pseudo, Nom, Prenom, Age, IdRole)
    return User


def MapArrayResultBddToArrayUtilisateur(arrayBdd):
    UsersArray = []
    for resultBdd in arrayBdd:
        UsersArray.append(Utilisateur(
            resultBdd[0], resultBdd[1], resultBdd[2], resultBdd[3], resultBdd[4], resultBdd[5]))
    return UsersArray


def MapResultToMessageInformation(result):
    return MessageInformation(result[0], result[1], result[2])


def imageConfirmPoste():
    arrayImg = [
        "https://media.giphy.com/media/kRXnZwKrPTwVq/giphy.gif",
        "https://media.giphy.com/media/OE6FE4GZF78nm/giphy.gif",
        "https://media.giphy.com/media/QYwB8ai7mtORGRAxJZ/giphy.gif",
        "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
        "https://media.giphy.com/media/3oEjI5VtIhHvK37WYo/giphy.gif",
        "https://media.giphy.com/media/2lfllWGtBaXOSrErQb/giphy.gif",
        "https://media.giphy.com/media/3HAYjf986boJO698zIY/giphy.gif",
        "https://media.giphy.com/media/jL6OeIhk3zPi/giphy.gif",
        "https://media.giphy.com/media/7TtvTUMm9mp20/giphy.gif"
    ]
    return random.choice(arrayImg)


def isNullOrEmpty(*stringAVerifier):
    boolNullorEmpty = False
    for string in stringAVerifier:
        if string.isspace() or string.strip() == False or len(string) == 0:
            boolNullorEmpty = True
    return boolNullorEmpty
