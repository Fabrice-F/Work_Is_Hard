from flask import Flask, url_for, render_template ,session, request, redirect   # render_template permet de mettre des pages html
from Dao import *
from markupsafe import escape
import hashlib , sqlite3
from datetime import *

TempsSession = 5 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=TempsSession)

@app.route('/')
def index():
    resultArray = getLastPoste()
    posteArray = []
    for result in resultArray:
        posteArray.append(Poste(result[0],result[1],result[2],result[3]))
    if 'utilisateur' in session:
        return render_template("Accueil.html",posteArray=posteArray,user=session['utilisateur'])
    return render_template("Accueil.html",posteArray=posteArray)


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

    if userDemandeConnexion.PseudoUtilisateur==pseudo and userDemandeConnexion.MdpUtilisateur== h.hexdigest():
        session['utilisateur'] = userDemandeConnexion.__dict__
        return redirect(url_for('index'))
    else:
        return render_template("Error/ErrorConnexion.html")

@app.route('/logOut')
def logOut():
    session.clear()
    return redirect(url_for('index'))

@app.route('/GestionDeCompte')
def login():
    if 'utilisateur' in session:
        return render_template("GestionDeCompte.html",user=session['utilisateur'])
    else:
        return render_template("inscription.html")

@app.route('/CreationDePoste')
def CreationDePoste():
    if 'utilisateur' in session:
        return render_template("CreationDePoste.html",user=session['utilisateur'])
    else:
        return redirect(url_for('index'))

@app.route('/publiePost', methods=['POST'])
def publiePost():
    if 'utilisateur' in session:
        TitrePoste = request.form["TitrePoste"]
        LienImg = request.form["LienImg"]
        UserId = session['utilisateur']["IdUtilisateur"]
        if InsertPoste(UserId,TitrePoste,LienImg):
            return redirect(url_for('index'))
        #TODO: Ajout de la date / userQuiEnvoiLePost / pour enregistrer dans la db
        else:
            return "problème d'insertion à la base de donnée"
    else:
        return redirect(url_for('index'))

@app.route('/page<idPage>')
def getPage(idPage):
    if 'utilisateur' in session:
        nbPage= int(idPage)
        return render_template("Accueil.html",user=session['utilisateur'],page= nbPage)
    else:
        nbPage= int(idPage)
        return render_template("Accueil.html",page= nbPage)




@app.route('/base')
def accesBase():
    return render_template("heritageJinja/base.html")

@app.route('/ChildBase1')
def ChildBase1():
    return render_template("heritageJinja/ChildBase1.html")


class Utilisateur:
    def __init__(self, identifiant, pseudo,mdp,nom,prenom,age):
        self.IdUtilisateur=identifiant
        self.PseudoUtilisateur=pseudo
        self.MdpUtilisateur=mdp
        self.NomUtilisateur=nom
        self.PrenomUtilisateur=prenom 
        self.AgeUtilisateur=age

class Poste:
    def __init__(self, pseudo,titre, adresse,date):
        self.PseudoUtilisateurPoste=pseudo
        self.titrePoste=titre
        self.adressePoste=adresse
        self.datePoste=date 



