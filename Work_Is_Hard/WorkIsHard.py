from flask import Flask, url_for, render_template ,session, request, redirect   # render_template permet de mettre des pages html
from Dao import *
from markupsafe import escape
import hashlib , sqlite3
from datetime import *
from ConstanteAndTools import *
import threading

lock = threading.Lock()


TempsSession = 60 
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=TempsSession)

@app.route('/')
def index():
    resultArray = getLastPoste()
    nbPosteTotal = getNbPoste()
    posteArray = []
    for result in resultArray:
        posteArray.append(Poste(result[0],result[1],result[2],result[3]))
    if 'utilisateur' in session:
        return render_template("Accueil.html",posteArray=posteArray,nbPosteTotal =nbPosteTotal,user=session['utilisateur'])
    return render_template("Accueil.html",posteArray=posteArray ,nbPosteTotal=nbPosteTotal)


@app.route('/inscription')
def inscription():
    return render_template("inscription.html")


@app.route('/ConfirmationInscription', methods=['POST'])
def ConfirmationInscription():
    # Conncexion a la base de donnée
    conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()
    

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


    # print(pseudo)
    # print(nom)
    # print(prenom)
    # print(motdepasse_hashe)
    # print(confmdp_hashe)
    # print(datenaissance) 

    
    # Insertion des données dans la BDD
    c.execute("INSERT INTO Utilisateur (PseudoUtilisateur, NomUtilisateur, Prenom, MotDePasseUtilisateur, AgeUtilisateur) VALUES (?, ?, ?, ?, ?)", (pseudo, nom, prenom, motdepasse_hashe, datenaissance))

    #Commit de la connexion
    conn.commit()

    #Fermeture de connexion
    conn.close()

    return render_template("inscription.html")

    

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




#TODO: Refaire le systeème de connexion
@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdp = request.form["password"]
    h = hashlib.md5(mdp.encode())
    conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()
    
    resultArray = c.execute(f"SELECT * FROM Utilisateur WHERE PseudoUtilisateur = '{pseudo}'").fetchall()
    if len(resultArray)==1:
        result =  resultArray[0]
    else:
        return render_template("Error/ErrorPage.html",messageError=messageErrorConnexion())

    userDemandeConnexion= Utilisateur(result[0], result[1], result[2], result[3], result[4],result[5])

    if userDemandeConnexion.PseudoUtilisateur==pseudo and userDemandeConnexion.MdpUtilisateur== h.hexdigest():
        session['utilisateur'] = userDemandeConnexion.__dict__
        return redirect(url_for('index'))
    else:
        return render_template("Error/ErrorPage.html",messageError=messageErrorConnexion())


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/GestionDeCompte')
def GestionDeCompte():
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
        else:
            return "problème d'insertion à la base de donnée"
    else:
        return redirect(url_for('index'))


@app.route('/page<idPage>')
def getPage(idPage):

    numPage= int(idPage)
    posteArray = []

    nbPosteTotal = getNbPoste()
    resultArray = getPosteByPage(idPage)
    NbPageMax = CalculNbPageMax(nbPosteTotal,nbPosteByPage)

    for result in resultArray:
        posteArray.append(Poste(result[0],result[1],result[2],result[3]))

    if 'utilisateur' in session:
        return render_template("Accueil.html",posteArray=posteArray,page= numPage,nbPosteTotal=nbPosteTotal,NbPageMax=NbPageMax,user=session['utilisateur'])
    else:
        return render_template("Accueil.html",posteArray=posteArray,page= numPage,nbPosteTotal=nbPosteTotal,NbPageMax=NbPageMax )




@app.route('/DemandeSiPseudoDisponible',methods=['POST'])
def DemandeSiPseudoDisponible():
    if 'utilisateur' not in session:
        return redirect(url_for('index'))   

    pseudoVoulu = request.form["PseudoVoulu"]
    IsPseudoDisponible = IfPseudoDisponible(pseudoVoulu)
    if IsPseudoDisponible :
        UserId= session['utilisateur']["IdUtilisateur"]
        UserPseudo= session['utilisateur']["PseudoUtilisateur"]
        if UpdatePseudo(pseudoVoulu,UserPseudo,UserId):
            return "True"
        else:
            return "Echec pendant la mise à jour du pseudo"
    else:
        return "Le pseudo n'est pas disponible"
    return 

@app.route('/DemandeChangementPassword',methods=['POST']) #methode appelé en AJAX
def DemandeChangementPassword():
    if 'utilisateur' not in session:
        return redirect(url_for('index'))
    
    UserId= session['utilisateur']["IdUtilisateur"]
    UserPseudo= session['utilisateur']["PseudoUtilisateur"]
    UserPasswordCurrent= session['utilisateur']["MdpUtilisateur"]
    AncienMotDePasseSaisie = hashMdp(request.form["AncienMotDePasse"])
    NewMotDePasse = hashMdp(request.form["NewMotDePasse"])
    ConfirmationMotDePasse = hashMdp(request.form["ConfirmationMotDePasse"])

    if(NewMotDePasse !=ConfirmationMotDePasse):
        return "Le nouveau mot de passe et la confirmation ne sont pas identique"
    if(UserPasswordCurrent !=AncienMotDePasseSaisie):
        return "L'ancien mot de passe est incorrect"

    if UpdateMdp(NewMotDePasse,UserPseudo,UserId):
        return "True"
    else:
        return "Echec pendant la mise à jour du mot de passe"


@app.route('/testAjax')
def test():
    return "AJAX FONCTIONNEL"


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



