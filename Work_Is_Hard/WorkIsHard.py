# render_template permet de mettre des pages html
from markupsafe import escape
import hashlib
import sqlite3
import re
from flask import Flask, url_for, render_template, session, request, redirect
from Dao import *
from datetime import *
from ConstanteAndTools import *
from Classes import *

TempsSession = 60
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.permanent_session_lifetime = timedelta(minutes=TempsSession)


@app.route('/')
def index():
    resultArray = getLastPoste()
    nbPosteTotal = getNbPoste()

    msgTmp = getLastMessageInformation()
    if(msgTmp == False):
        messageInfo = MessageInformation("vide", "Aucun", datetime.now())
    else:
        messageInfo = MapResultToMessageInformation(msgTmp)
    posteArray = []
    for result in resultArray:
        posteArray.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
    if 'utilisateur' in session:
        return render_template("Accueil.html", posteArray=posteArray,
                               nbPosteTotal=nbPosteTotal, messageInfo=messageInfo,
                               user=session['utilisateur'])

    return render_template("Accueil.html", posteArray=posteArray,
                           nbPosteTotal=nbPosteTotal, messageInfo=messageInfo)


@app.route('/inscription')
def inscription():
    return render_template("inscription.html")


@app.route('/ConfirmationInscription', methods=['POST'])
def ConfirmationInscription():
    pattern_regex_info_user = "^[a-zA-Z0-9]*$"
    reg= "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$"
    pattern_regex_password_user = re.compile(reg)

    nom = request.form["nom"]
    prenom = request.form["prenom"]    
    pseudo = request.form["pseudo"]
    mot_de_passe_clair = request.form["motdepasse"]
    confirm_mdp = request.form["confirm_mdp"]
    datenaissance = request.form["datenaissance"]

    
    #♣TODO : Faire uen regex pour le nom et le prenom juste avec majuscule et miniscule ( sans chiffre)

    if isNullOrEmpty(nom) or not re.match(pattern_regex_info_user,nom):
        error ="Le champs nom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    if isNullOrEmpty(prenom) or not re.match(pattern_regex_info_user,prenom):
        error ="Le champs prenom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    if isNullOrEmpty(pseudo) or not re.match(pattern_regex_info_user,pseudo):
        error ="Le champs pseudo est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)
    
    
    if len(pseudo)<5:
        error ="Le Le champs pseudo ne comporte pas 5 caractères"
        return render_template("inscription.html", error=error)
        
    #♣TODO :  Vérifier si le pseudo n'est pas supérieur a 15 caractères.

    if isNullOrEmpty(mot_de_passe_clair):
        error ="Le champs mot de passe est vide ou remplie d'espace"
        return render_template("inscription.html", error=error)

    if isNullOrEmpty(confirm_mdp):
        error ="Le champs confirmation mots de passe est vide ou remplie d'espace"
        return render_template("inscription.html", error=error)

    if not re.search(pattern_regex_password_user, mot_de_passe_clair):
        error ="Le champs mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    if not re.search(pattern_regex_password_user, confirm_mdp):
        error ="Le champs confirmation mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    if mot_de_passe_clair != confirm_mdp:
        error ="Le mots de passe et sa confirmation ne sont pas identique."
        return render_template("inscription.html", error=error)

    if isNullOrEmpty(datenaissance):
        error ="Le date de naissance est vide n'est pas remplie"
        return render_template("inscription.html", error=error)


    mdp = hashMdp(mot_de_passe_clair)

    if IfPseudoDisponible(pseudo) == True:
        if insert_user_inscription(pseudo, nom, prenom, mdp, datenaissance):
            imgPosteOk = imageConfirmPoste()
            return render_template("Transition.html", redirect=True, imgPosteOk=imgPosteOk, message="Votre inscription c'est bien déroulé, vous aller être redirigé vers la page d'accueil !")
        else:
            return "problème d'inscription"
    else: #si pseudo existe 
        error="Le pseudo est déja pris" 
        return render_template("inscription.html", pseudo=pseudo, error=error)


@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdpClair = request.form["password"]

    if isNullOrEmpty(pseudo, mdpClair):
        return render_template("Error/ErrorPage.html", messageError=messageErrorChampsVide())

    mdp = hashMdp(mdpClair)
    result = connexionUtilisateur(pseudo, mdp)
    if result == False:
        return render_template("Error/ErrorPage.html", messageError=messageErrorConnexion())

    userDemandeConnexion = Utilisateur(
        result[0], result[1], result[2], result[3], result[4], result[5])
    mdpCurrentUser = getUserCurrentPasswd(
        userDemandeConnexion.PseudoUtilisateur, userDemandeConnexion.IdUtilisateur)

    if(mdpCurrentUser == False):
        return render_template("Error/ErrorPage.html", messageError=messageErrorConnexion())

    if userDemandeConnexion.PseudoUtilisateur == pseudo and mdpCurrentUser == mdp:
        session['utilisateur'] = userDemandeConnexion.__dict__
        return redirect(url_for('index'))
    else:
        return render_template("Error/ErrorPage.html", messageError=messageErrorConnexion())


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/GestionDeCompte')
def GestionDeCompte():
    if 'utilisateur' in session:
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        return render_template("GestionDeCompte.html", user=session['utilisateur'], messageInfo=messageInfo)
    else:
        return render_template("inscription.html")


@app.route('/CreationDePoste')
def CreationDePoste():
    if 'utilisateur' in session:
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        return render_template("CreationDePoste.html", user=session['utilisateur'], messageInfo=messageInfo)
    else:
        return redirect(url_for('index'))


@app.route('/publiePost', methods=['POST'])
def publiePost():
    if 'utilisateur' in session:
        TitrePoste = request.form["TitrePoste"]
        LienImg = request.form["LienImg"]

        if isNullOrEmpty(TitrePoste, LienImg):
            return render_template("Error/ErrorPage.html", messageError=messageErrorChampsVide())

        UserId = session['utilisateur']["IdUtilisateur"]

        imgPosteOk = imageConfirmPoste()

        if getModeModeration() == 1:
            if InsertPosteAttenteModeration(UserId, TitrePoste, LienImg):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, imgPosteOk=imgPosteOk, message="Votre poste a été pris en compte et est en attente de validation")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
        else:
            if InsertPoste(UserId, TitrePoste, LienImg):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, imgPosteOk=imgPosteOk, message="Votre poste à été intégré !")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
    else:
        return redirect(url_for('index'))


@app.route('/page<idPage>')
def getPage(idPage):

    numPage = int(idPage)
    posteArray = []
    nbPosteTotal = getNbPoste()
    resultArray = getPosteByPage(idPage)
    NbPageMax = CalculNbPageMax(nbPosteTotal, nbPosteByPage)

    msgTmp = getLastMessageInformation()
    if(msgTmp == False):
        messageInfo = MessageInformation("vide", "Aucun", datetime.now())
    else:
        messageInfo = MapResultToMessageInformation(msgTmp)

    for result in resultArray:
        posteArray.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if 'utilisateur' in session:
        return render_template("Accueil.html", posteArray=posteArray, page=numPage, nbPosteTotal=nbPosteTotal, NbPageMax=NbPageMax, messageInfo=messageInfo, user=session['utilisateur'])
    else:
        return render_template("Accueil.html", posteArray=posteArray, page=numPage, nbPosteTotal=nbPosteTotal, NbPageMax=NbPageMax, messageInfo=messageInfo)


# Fonction appelée en ajax
@app.route('/DemandeSiPseudoDisponible', methods=['POST'])
def DemandeSiPseudoDisponible():
    if 'utilisateur' not in session:  # test pour voir si poas d'utilisateur dans session
        return redirect(url_for('index'))

    pseudoVoulu = request.form["PseudoVoulu"]
    if isNullOrEmpty(pseudoVoulu):
        return messageErrorChampsVide()

    IsPseudoDisponible = IfPseudoDisponible(pseudoVoulu)
    if IsPseudoDisponible:
        UserId = session['utilisateur']["IdUtilisateur"]
        UserPseudo = session['utilisateur']["PseudoUtilisateur"]
        if UpdatePseudo(pseudoVoulu, UserPseudo, UserId):
            return "True"
        else:
            return "Echec pendant la mise à jour du pseudo"
    else:
        return "Le pseudo n'est pas disponible"
    return


# Fonction appelée en ajax
@app.route('/DemandeChangementPassword', methods=['POST'])
def DemandeChangementPassword():
    if 'utilisateur' not in session:
        return redirect(url_for('index'))

    UserId = session['utilisateur']["IdUtilisateur"]
    UserPseudo = session['utilisateur']["PseudoUtilisateur"]
    UserPasswordCurrent = getUserCurrentPasswd(UserPseudo, UserId)

    oldPasswordClair = request.form["AncienMotDePasse"]
    newPasswordClair = request.form["NewMotDePasse"]
    confirmPasswordClair = request.form["ConfirmationMotDePasse"]

    if isNullOrEmpty(oldPasswordClair, newPasswordClair, confirmPasswordClair):
        return messageErrorChampsVide()

    AncienMotDePasseSaisie = hashMdp(oldPasswordClair)
    NewMotDePasse = hashMdp(newPasswordClair)
    ConfirmationMotDePasse = hashMdp(confirmPasswordClair)

    if(NewMotDePasse != ConfirmationMotDePasse):
        return "Le nouveau mot de passe et la confirmation ne sont pas identique"

    if(UserPasswordCurrent != AncienMotDePasseSaisie):
        return "L'ancien mot de passe est incorrect"

    if UpdateMdp(NewMotDePasse, UserPseudo, UserId):
        return "True"
    else:
        return "Echec pendant la mise à jour du mot de passe"


@app.route('/updateTitrePoste', methods=['POST'])  # Fonction appelée en ajax
def updateTitrePoste():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        NewTitrePoste = request.form["NewTitrePoste"]
        MdpUserClair = request.form["MdpUser"]

        if isNullOrEmpty(idPoste, NewTitrePoste, MdpUserClair):
            return messageErrorChampsVide()

        MdpUserSaisie = hashMdp(MdpUserClair)
        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if UpdateTitrePoste(idPoste, NewTitrePoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/SuppressionPosteAccueil', methods=['POST'])
def SuppressionPosteAccueil():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        MdpUserClair = request.form["MdpUser"]

        if isNullOrEmpty(idPoste, MdpUserClair):
            return messageErrorChampsVide()

        MdpUserSaisie = hashMdp(MdpUserClair)

        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if deletePoste(idPoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" SECTION ADMINISTRATION  """


@app.route('/Administration')
def Administration():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        isModeModeractionActive = bool(getModeModeration())
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        ArrayUser = SelectAllUser()
        AllUser = MapArrayResultBddToArrayUtilisateur(ArrayUser)
        return render_template("Administration.html", user=session['utilisateur'], allUser=AllUser, messageInfo=messageInfo, isModeModeractionActive=isModeModeractionActive)
    else:
        return redirect(url_for('index'))


@app.route("/ChangementRole", methods=['POST'])  # Fonction appelée en ajax
def ChangementRole():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        pseudoUser = request.form["pseudoUser"]
        idUser = request.form["idUser"]
        AncienRoleUser = request.form["AncienRoleUser"]
        NouveauRoleUser = request.form["NouveauRoleUser"]
        mdpOfAdminSaisieClair = request.form["AdminPwd"]

        if isNullOrEmpty(pseudoUser, idUser, AncienRoleUser, NouveauRoleUser, mdpOfAdminSaisieClair):
            return messageErrorChampsVide()

        mdpOfAdminSaisie = hashMdp(mdpOfAdminSaisieClair)
        mdpOfAdmin = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdpOfAdminSaisie != mdpOfAdmin:
            return "Le mot de passe entré est incorrect"

        isUpdate = UpdateRole(idUser, pseudoUser, NouveauRoleUser)
        return str(isUpdate)
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route("/updateMsgInformation", methods=['POST'])
def updateMsgInformation():

    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        msg = request.form["Msg"]
        MdpUserSaisieClair = request.form["MdpUser"]

        if isNullOrEmpty(msg, MdpUserSaisieClair):
            return messageErrorChampsVide()

        MdpUserSaisie = hashMdp(MdpUserSaisieClair)
        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        userIdCurrent = session['utilisateur']["IdUtilisateur"]
        if updateMessageInformation(msg, userIdCurrent):
            return "True"
        else:
            return "Le message n'as pas pu être actualisé"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/changementModeModeration', methods=['POST'])
def changementModeModeration():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:

        MdpUserSaisieClair = request.form["MdpUser"]
        ModeModerationVoulu = request.form["ModeModerationVoulu"]

        if isNullOrEmpty(ModeModerationVoulu, MdpUserSaisieClair):
            return messageErrorChampsVide()

        user = MapSessionToUser(session['utilisateur'])
        MdpUserSaisie = hashMdp(MdpUserSaisieClair)
        modeModerationVoulut = 1 if ModeModerationVoulu == "true" else 0

        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if updateModeModeration(modeModerationVoulut, user.IdUtilisateur):
            return "True"
        else:
            return "Echec pendant la mise à jour du mode modération"
    else:
        return redirect(url_for('index'))


@app.route('/Moderation<idPage>')
def Moderation(idPage):

    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        isModeModeractionActive = bool(getModeModeration())
        numPage = int(idPage)
        postesAM = []
        nbPosteAttenteModerationTotal = getNbPosteAttenteModeration()
        resultArray = getPosteAttenteModerationByPage(idPage)
        NbPageMax = CalculNbPageMax(
            nbPosteAttenteModerationTotal, nbPosteByPage)

        for result in resultArray:
            postesAM.append(PosteAttenteModeration(
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

        return render_template("Moderation.html", user=session['utilisateur'], postesAM=postesAM, NbPageMax=NbPageMax, page=numPage, isModeModeractionActive=isModeModeractionActive)
    else:
        return redirect(url_for('index'))


@app.route('/Bannissement', methods=['POST'])  # Fonction appelée en ajax
def Bannissement():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        userBanId = request.form["userId"]
        MdpUserSaisieClair = request.form["MdpUser"]

        if isNullOrEmpty(userBanId, MdpUserSaisieClair):
            return messageErrorChampsVide()

        MdpUserSaisie = hashMdp(MdpUserSaisieClair)
        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if BanUser(userBanId):
            return "True"
        else:
            return "L'utilisateur n'as pas pu être banni"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/updatePosteAttenteModeration', methods=['POST'])
def updatePosteAttenteModeration():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPostePAM = request.form["IdPoste"]
        isPostAccept = request.form["IsPostAccept"]

        if isNullOrEmpty(idPostePAM, isPostAccept):
            return messageErrorChampsVide()

        if isPostAccept == "true":
            acceptPostePAM(idPostePAM)
            return "True"
        else:
            deletePostePAM(idPostePAM)
            return "True"
    else:
        return redirect(url_for('index'))


@app.route('/updateTitrePAM', methods=['POST'])  # Fonction appelée en ajax
def updateTitrePAM():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        NewTitrePoste = request.form["NewTitrePoste"]
        mdpClaire = request.form["MdpUser"]

        if isNullOrEmpty(idPoste, NewTitrePoste, mdpClaire):
            return messageErrorChampsVide()

        MdpUserSaisie = hashMdp(mdpClaire)

        mdpCurrentUser = getUserCurrentPasswd(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if UpdateTitrePostePAM(idPoste, NewTitrePoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" FIN SECTION ADMINISTRATION  """


@app.route('/A_Propos')
def A_Propos():
    if 'utilisateur' in session:
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        return render_template("A_Propos.html", messageInfo=messageInfo, user=session['utilisateur'])
    else:
        return render_template("A_Propos.html")


@app.route('/Cgu')
def Cgu():
    if 'utilisateur' in session:
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        return render_template("Cgu.html", messageInfo=messageInfo, user=session['utilisateur'])
    return render_template("Cgu.html")


@app.route('/Contact')
def Contact():
    if 'utilisateur' in session:
        msgTmp = getLastMessageInformation()
        if(msgTmp == False):
            messageInfo = MessageInformation("vide", "Aucun", datetime.now())
        else:
            messageInfo = MapResultToMessageInformation(msgTmp)
        return render_template("Contact.html", messageInfo=messageInfo, user=session['utilisateur'])
    return render_template("Contact.html")
