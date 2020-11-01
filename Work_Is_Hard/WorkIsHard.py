from flask import Flask, url_for, render_template ,session, request, redirect   # render_template permet de mettre des pages html
from Dao import *
from markupsafe import escape
import hashlib , sqlite3
from datetime import *
from ConstanteAndTools import *

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

@app.route('/Administration')
def Administration():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur']== 3:
        ArrayUser = SelectAllUser()
        AllUser= MapArrayResultBddToArrayUtilisateur(ArrayUser)
        return render_template("Administration.html",user=session['utilisateur'],allUser =AllUser)
    else :
        return redirect(url_for('index'))

@app.route("/ChangementRole", methods=['POST'])
def ChangementRole():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur']== 3:    
        pseudoUser = request.form["pseudoUser"]
        idUser = request.form["idUser"]    
        AncienRoleUser = request.form["AncienRoleUser"]    
        NouveauRoleUser = request.form["NouveauRoleUser"]    
        mdpOfAdmin = hashMdp(request.form["AdminPwd"])
        print(pseudoUser)
        print(idUser)
        print(AncienRoleUser)
        print(NouveauRoleUser)
        print(mdpOfAdmin)
        return "True"
    else :
        return redirect(url_for('index'))

#TODO: Refaire le systeème de connexion
@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdp = hashMdp(request.form["password"])
    result = connexionUtilisateur(pseudo,mdp)
    if result ==False:
        return render_template("Error/ErrorPage.html",messageError=messageErrorConnexion())

    userDemandeConnexion= Utilisateur(result[0], result[1], result[2], result[3], result[4],result[5],result[6])
    if userDemandeConnexion.PseudoUtilisateur==pseudo and userDemandeConnexion.MdpUtilisateur== mdp:
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




