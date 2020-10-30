from flask import Flask, url_for, render_template , request   # render_template permet de mettre des pages html
from werkzeug.security import generate_password_hash, check_password_hash
from Mecanisme import *
from markupsafe import escape
import hashlib , sqlite3



app = Flask(__name__)

@app.route('/')
def index():
    return render_template("Accueil.html")
    

@app.route('/login')
def login():
    for row in ExecuteRequest('SELECT * FROM Utilisateur'):
        userOne = Utilisateur(row[0],row[1],row[2],row[3],row[4],row[5])
    return f"{userOne.IdUtilisateur} | {userOne.PseudoUtilisateur} | {userOne.MdpUtilisateur} | {userOne.NomUtilisateur} | {userOne.AgeUtilisateur}"


@app.route('/test')
def profile():
    return render_template("test.html",champsA="La phrase de la page test")

@app.route('/inscription')
def inscription():
    return render_template("inscription.html")

@app.route('/ConfirmationInscription', methods=['POST'])
def ConfirmationInscription():

    # Récupération des informations de la page inscription.html
    pseudo = request.form["pseudo"]
    nom = request.form["nom"]
    prenom = request.form["prenom"]
    motdepasse = request.form["motdepasse"]
    confmdp = request.form["confmdp"]
    datenaissance = request.form["datenaissance"]

    #hash des mots de passes 
    motdepasse_hashe = hashlib.sha256(motdepasse.encode('ascii')).hexdigest()
    confmdp_hashe = hashlib.sha256(confmdp.encode('ascii')).hexdigest()


    print(pseudo)
    print(nom)
    print(prenom)
    print(motdepasse_hashe)
    print(confmdp_hashe)
    print(datenaissance) 

    return render_template("inscription.html")
    # Conncexion a la base de donnée
    # conn = sqlite3.connect('WorkIsHard.db')
    # c = conn.cursor()
    
    # # Insertion des données dans la BDD
    # c.execute("INSERT INTO Utilisateur(pseudo, nom, prenom, motdepasse, confmdp, datenaissance) VALUES(%s, %s, %s, %s, %s, %s)", (pseudo, nom, prenom, motdepasse, confmdp, datenaissance))

    #  if len(resultArray)==1:
    #     result =  resultArray[0]
    # else:
    #     return render_template("Error/ErrorConnexion.html")


    # #Commit de la connexion
    # conn.commit()

    # #Fermeture de connexion
    # conn.close()

    

    """print(pseudo)
    print(nom)
    print(prenom)
    print(motdepasse)
    print(confmdp)
    print(datenaissance)

    return render_template("inscription.html")
    """

    """hashage du mots de passe  
       hashage de la confrmation  mots de passe
       comparer si le hash du mot de passe est identique au hash de la fconfirmation """


    """conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()*


    resultArray = c.execute(f"SELECT * FROM Utilisateur WHERE PseudoUtilisateur = '{pseudo}'").fetchall()
    if len(resultArray)==1:
        return render_template("Error/testErreur.html")
    else:
        return "Votre compte a bien été crée"
    """



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



