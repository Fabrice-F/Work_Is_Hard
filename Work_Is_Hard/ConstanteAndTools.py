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


def MapSessionToUser(session):
    idUser= session["IdUtilisateur"]
    Pseudo=session["PseudoUtilisateur"]
    Mdp=session["MdpUtilisateur"]
    Nom=session["NomUtilisateur"]
    Prenom=session["PrenomUtilisateur"]
    Age=session["AgeUtilisateur"]
    IdRole= session["IdRoleUtilisateur"]
    User= Utilisateur(idUser,Pseudo,Mdp,Nom,Prenom,Age,IdRole)
    return User

def MapArrayResultBddToArrayUtilisateur(arrayBdd):
    UsersArray = []
    for resultBdd in arrayBdd :
        UsersArray.append(Utilisateur(resultBdd[0], resultBdd[1], resultBdd[2], resultBdd[3], resultBdd[4],resultBdd[5],resultBdd[6]))
    return UsersArray




class Utilisateur:
    def __init__(self, identifiant, pseudo,mdp,nom,prenom,age,role):
        self.IdUtilisateur=identifiant
        self.PseudoUtilisateur=pseudo
        self.MdpUtilisateur=mdp
        self.NomUtilisateur=nom
        self.PrenomUtilisateur=prenom 
        self.AgeUtilisateur=age
        self.IdRoleUtilisateur=role
        self.NomRole = self.getNomRole()
    def getNomRole(self):
        if self.IdRoleUtilisateur ==1:
            return "Posteur"
        elif self.IdRoleUtilisateur ==2:
            return "Modérateur"
        else:
            return "Administrateur"

class Poste:
    def __init__(self, pseudo,titre, adresse,date):
        self.PseudoUtilisateurPoste=pseudo
        self.titrePoste=titre
        self.adressePoste=adresse
        self.datePoste=date 

