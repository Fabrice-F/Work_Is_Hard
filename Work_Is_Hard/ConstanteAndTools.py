import math
import hashlib
import random
import re
import datetime
from flask import request
from Classes import *

""" Comme les constantes n'existe pas en python:
en dehors de creer une classe avec getter setter
Nous avons créer ce fichier Constante&Tools où des méthodes
servent de constante ainsi que quelques méthodes outils"""


def calcul_nb_page_max(numberPoste, nbPosteByPage):
    NbPageFloat = numberPoste / nbPosteByPage
    NbPage = math.ceil(NbPageFloat)
    return NbPage


def hash_password(motdePassClaire):
    h = hashlib.md5(motdePassClaire.encode())
    return h.hexdigest()


def message_error_connexion():
    msg = """L'identifiant ou le mot de passe avec lesquels vous avez tenté de vous
    connecter sont incorrect ..."""
    return msg


def message_error_champs_vide():
    msg = """L'un des champs que vous avez renseigné est vide ..."""
    return msg


def get_visitor_ip(requestRoute):
    return requestRoute.environ['REMOTE_ADDR']


def map_session_to_user(session):
    idUser = session["IdUtilisateur"]
    Pseudo = session["PseudoUtilisateur"]
    Nom = session["NomUtilisateur"]
    Prenom = session["PrenomUtilisateur"]
    Age = session["DateNaissanceUtilisateur"]
    IdRole = session["IdRoleUtilisateur"]
    User = Utilisateur(idUser, Pseudo, Nom, Prenom, Age, IdRole)
    return User


def map_array_result_bdd_to_array_utilisateur(arrayBdd):
    UsersArray = []
    for resultBdd in arrayBdd:
        UsersArray.append(Utilisateur(
            resultBdd[0], resultBdd[1], resultBdd[2], resultBdd[3], resultBdd[4], resultBdd[5]))
    return UsersArray


def map_result_to_message_information(result):
    return MessageInformation(result[0], result[1], result[2])


def image_confirmation():
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


def is_null_or_empty(*stringAVerifier):
    boolNullorEmpty = False
    for string in stringAVerifier:
        if string.isspace() or string.strip() == False or len(string) == 0:
            boolNullorEmpty = True
    return boolNullorEmpty


def is_correct_string_regex(*stringAVerifier):
    pattern = "^[a-zA-Z0-9]*$"
    isStringOk = True
    for s in stringAVerifier:
        if not re.match(pattern, s):
            return s
    return isStringOk

def size_string_is_correct(string,mini,maxi):
    if len(string)<mini or len(string)>maxi:
        return False
    return True

def verif_date_de_naissance(dateNaissance):
    dateNaissanceDateFormat = datetime.datetime.strptime(dateNaissance, '%Y-%m-%d')
    dateMoins18 = datetime.datetime.today()- datetime.timedelta(days=18*365.24)
    return dateNaissanceDateFormat<dateMoins18
        