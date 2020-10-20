from flask import Flask, url_for, render_template , request   # render_template permet de mettre des pages html
from Mecanisme import *
from markupsafe import escape
import hashlib , sqlite3


app = Flask(__name__)

@app.route('/')
def index():
    return GoToPage("Accueil.html")
    

@app.route('/login')
#def login():
#    conn = sqlite3.connect('WorkIsHard.db')
#    c = conn.cursor()
#    for row in c.execute('SELECT * FROM Utilisateur'):
#        userOne = Utilisateur(row[0],row[1],row[2],row[3],row[4],row[5])
#    return f"{userOne.IdUtilisateur} | {userOne.PseudoUtilisateur} | {userOne.MdpUtilisateur} | {userOne.NomUtilisateur} | {userOne.AgeUtilisateur}"
def login():
    for row in ExecuteRequest('SELECT * FROM Utilisateur'):
        userOne = Utilisateur(row[0],row[1],row[2],row[3],row[4],row[5])
    return f"{userOne.IdUtilisateur} | {userOne.PseudoUtilisateur} | {userOne.MdpUtilisateur} | {userOne.NomUtilisateur} | {userOne.AgeUtilisateur}"


@app.route('/user/<username>')
def profile(username):
    return '{}\'s profile'.format(escape(username))

@app.route('/inscription')
def inscription():
    return render_template("inscription.html")


@app.route('/connexion/', methods=['POST'])
def connexion():
    pseudo = request.form["pseudo"]
    mdp = request.form["password"]
    h = hashlib.md5(mdp.encode())
    conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()
    
    resultArray = c.execute(f"SELECT * FROM Utilisateur WHERE PseudoUtilisateur = '{pseudo}'").fetchall()
    if len(resultArray)==1:
        result =  resultArray[0]
    else:
        return render_template("Error/ErrorConnexion.html")

    userDemandeConnexion= Utilisateur(result[0], result[1], result[2], result[3], result[4],result[5])
    print("pseudo :" , pseudo)
    print("mdp :" , h.hexdigest())
    print("pseudo BDD:" , userDemandeConnexion.PseudoUtilisateur)
    print("mdp BDD:" , userDemandeConnexion.MdpUtilisateur)

    if userDemandeConnexion.PseudoUtilisateur==pseudo and userDemandeConnexion.MdpUtilisateur== h.hexdigest():
        return render_template("test.html",champsA = pseudo)
    else:
        return render_template("Error/ErrorConnexion.html")


class Utilisateur:
    def __init__(self, identifiant, pseudo,mdp,nom,prenom,age):
        self.IdUtilisateur=identifiant
        self.PseudoUtilisateur=pseudo
        self.MdpUtilisateur=mdp
        self.NomUtilisateur=nom
        self.PrenomUtilisateur=prenom 
        self.AgeUtilisateur=age



