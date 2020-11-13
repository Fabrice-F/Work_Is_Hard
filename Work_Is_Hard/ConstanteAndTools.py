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


def calcul_nb_page_max(numberPoste, NB_POSTE_BY_PAGE):
    nb_page_float = numberPoste / NB_POSTE_BY_PAGE
    nb_page = math.ceil(nb_page_float)
    return nb_page


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
    id_user = session["IdUtilisateur"]
    pseudo = session["PseudoUtilisateur"]
    nom = session["NomUtilisateur"]
    prenom = session["PrenomUtilisateur"]
    date_naissance = session["DateNaissanceUtilisateur"]
    id_role = session["IdRoleUtilisateur"]
    user = Utilisateur(id_user, pseudo, nom, prenom, date_naissance, id_role)
    return user


def map_array_result_bdd_to_array_utilisateur(array_bdd):
    users_array = []
    for result_bdd in array_bdd:
        users_array.append(Utilisateur(
            result_bdd[0], result_bdd[1], result_bdd[2], result_bdd[3], result_bdd[4], result_bdd[5]))
    return users_array


def map_result_to_message_information(result):
    return MessageInformation(result[0], result[1], result[2])


def image_confirmation():
    array_img = [
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
    return random.choice(array_img)


def is_null_or_empty(*string_a_verifier):
    bool_null_or_empty = False
    for string in string_a_verifier:
        if string.isspace() or string.strip() == False or len(string) == 0:
            bool_null_or_empty = True
    return bool_null_or_empty


def is_correct_string_regex(*string_a_verifier):
    pattern = "^[a-zA-Z0-9]*$"
    is_string_ok = True
    for s in string_a_verifier:
        if not re.match(pattern, s):
            return s
    return is_string_ok

def size_string_is_correct(string,mini,maxi):
    if len(string)<mini or len(string)>maxi:
        return False
    return True

def verif_date_de_naissance(dateNaissance):
    date_naissance_format = datetime.datetime.strptime(dateNaissance, '%Y-%m-%d')
    date_du_jour_moin_18_ans = datetime.datetime.today()- datetime.timedelta(days=18*365.24)
    return date_naissance_format<date_du_jour_moin_18_ans
        