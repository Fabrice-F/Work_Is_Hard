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
    resultArray = get_last_poste()
    nbPosteTotal = get_nb_poste()

    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)
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


@app.route('/confirmation_inscription', methods=['POST'])
def confirmation_inscription():
    pattern_regex_nom_prenom = "^[a-zA-Z]*$"
    pattern_regex_info_pseudo = "^[a-zA-Z0-9]*$"
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,100}$"

    pattern_regex_password_user = re.compile(reg)

    nom = request.form["nom"].strip()
    prenom = request.form["prenom"].strip()
    pseudo = request.form["pseudo"].strip()
    mot_de_passe_clair = request.form["motdepasse"].strip()
    confirm_mdp = request.form["confirm_mdp"].strip()
    datenaissance = request.form["datenaissance"]

    if is_null_or_empty(nom) or not re.match(pattern_regex_nom_prenom, nom):
        error = "Le champs nom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    if not size_string_is_correct(nom, 2, 30):
        error = "Le champs nom ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    if is_null_or_empty(prenom) or not re.match(pattern_regex_nom_prenom, prenom):
        error = "Le champs prenom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    if not size_string_is_correct(prenom, 2, 30):
        error = "Le champs prenom ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    if is_null_or_empty(pseudo) or not re.match(pattern_regex_info_pseudo, pseudo):
        error = "Le champs pseudo est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    if not size_string_is_correct(pseudo, 3, 15):
        error = "Le champs pseudo ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    if is_null_or_empty(mot_de_passe_clair):
        error = "Le champs mot de passe est vide..."
        return render_template("inscription.html", error=error)

    if is_null_or_empty(confirm_mdp):
        error = "Le champs confirmation mots de passe est vide..."
        return render_template("inscription.html", error=error)

    if not re.search(pattern_regex_password_user, mot_de_passe_clair):
        error = "Le champs mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    if not re.search(pattern_regex_password_user, confirm_mdp):
        error = "Le champs confirmation mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    if not verif_date_de_naissance(datenaissance):
        error = "Vous n'avez pas l'age requis pour vous inscrire"
        return render_template("inscription.html", error=error)

    mdp = hash_password(mot_de_passe_clair)
    mdpConfirm = hash_password(confirm_mdp)

    if mdp != mdpConfirm:
        error = "Le mots de passe et sa confirmation ne sont pas identique."
        return render_template("inscription.html", error=error)

    if if_pseudo_disponible(pseudo) == True:

        if insert_user_inscription(pseudo, nom, prenom, mdp, datenaissance):
            imgPosteOk = image_confirm_poste()
            return render_template("Transition.html", redirect=True, imgPosteOk=imgPosteOk, message="Votre inscription c'est bien déroulé, vous aller être redirigé vers la page d'accueil !")
        else:
            return "problème d'inscription"
    else:  # si pseudo existe
        error = "Le pseudo est déja pris"
        return render_template("inscription.html", pseudo=pseudo, error=error)


@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdpClair = request.form["password"]

    if is_null_or_empty(pseudo, mdpClair):
        return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

    mdp = hash_password(mdpClair)
    result = connexion_utilisateur(pseudo, mdp)
    if result == False:
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    userDemandeConnexion = Utilisateur(
        result[0], result[1], result[2], result[3], result[4], result[5])
    mdpCurrentUser = get_current_user_password(
        userDemandeConnexion.PseudoUtilisateur, userDemandeConnexion.IdUtilisateur)

    if(mdpCurrentUser == False):
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    if userDemandeConnexion.PseudoUtilisateur == pseudo and mdpCurrentUser == mdp:
        session['utilisateur'] = userDemandeConnexion.__dict__
        return redirect(url_for('index'))
    else:
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/gestion_de_compte')
def gestion_de_compte():
    if 'utilisateur' in session:
        msgTmp = get_last_message_information()
        if(msgTmp == False):
            messageInfo = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            messageInfo = map_result_to_message_information(msgTmp)
        return render_template("GestionDeCompte.html", user=session['utilisateur'], messageInfo=messageInfo)
    else:
        return render_template("inscription.html")


@app.route('/creation_de_poste')
def creation_de_poste():
    if 'utilisateur' in session:
        msgTmp = get_last_message_information()
        if(msgTmp == False):
            messageInfo = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            messageInfo = map_result_to_message_information(msgTmp)
        return render_template("CreationDePoste.html", user=session['utilisateur'], messageInfo=messageInfo)
    else:
        return redirect(url_for('index'))


@app.route('/publie_post', methods=['POST'])
def publie_post():
    if 'utilisateur' in session:
        TitrePoste = request.form["TitrePoste"]
        LienImg = request.form["LienImg"]

        if is_null_or_empty(TitrePoste, LienImg):
            return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

        UserId = session['utilisateur']["IdUtilisateur"]

        imgPosteOk = image_confirm_poste()

        if get_mode_moderation() == 1:
            if insert_poste_attente_moderation(UserId, TitrePoste, LienImg):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, imgPosteOk=imgPosteOk, message="Votre poste a été pris en compte et est en attente de validation")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
        else:
            if insert_poste(UserId, TitrePoste, LienImg):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, imgPosteOk=imgPosteOk, message="Votre poste à été intégré !")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
    else:
        return redirect(url_for('index'))


@app.route('/page<idPage>')
def getPage(idPage):

    numPage = int(idPage)
    posteArray = []
    nbPosteTotal = get_nb_poste()
    resultArray = get_poste_by_page(idPage)
    NbPageMax = calcul_nb_page_max(nbPosteTotal, nbPosteByPage)

    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)

    for result in resultArray:
        posteArray.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if 'utilisateur' in session:
        return render_template("Accueil.html", posteArray=posteArray, page=numPage, nbPosteTotal=nbPosteTotal, NbPageMax=NbPageMax, messageInfo=messageInfo, user=session['utilisateur'])
    else:
        return render_template("Accueil.html", posteArray=posteArray, page=numPage, nbPosteTotal=nbPosteTotal, NbPageMax=NbPageMax, messageInfo=messageInfo)


# Fonction appelée en ajax
@app.route('/demande_si_pseudo_disponible', methods=['POST'])
def demande_si_pseudo_disponible():
    if 'utilisateur' not in session:  # test pour voir si poas d'utilisateur dans session
        return redirect(url_for('index'))

    pseudoVoulu = request.form["PseudoVoulu"]
    if is_null_or_empty(pseudoVoulu):
        return message_error_champs_vide()

    IsPseudoDisponible = if_pseudo_disponible(pseudoVoulu)
    if IsPseudoDisponible:
        UserId = session['utilisateur']["IdUtilisateur"]
        UserPseudo = session['utilisateur']["PseudoUtilisateur"]
        if update_pseudo(pseudoVoulu, UserPseudo, UserId):
            return "True"
        else:
            return "Echec pendant la mise à jour du pseudo"
    else:
        return "Le pseudo n'est pas disponible"
    return


# Fonction appelée en ajax
@app.route('/demande_changement_password', methods=['POST'])
def demande_changement_password():
    if 'utilisateur' not in session:
        return redirect(url_for('index'))

    UserId = session['utilisateur']["IdUtilisateur"]
    UserPseudo = session['utilisateur']["PseudoUtilisateur"]
    UserPasswordCurrent = get_current_user_password(UserPseudo, UserId)

    oldPasswordClair = request.form["AncienMotDePasse"]
    newPasswordClair = request.form["NewMotDePasse"]
    confirmPasswordClair = request.form["ConfirmationMotDePasse"]

    if is_null_or_empty(oldPasswordClair, newPasswordClair, confirmPasswordClair):
        return message_error_champs_vide()

    AncienMotDePasseSaisie = hash_password(oldPasswordClair)
    NewMotDePasse = hash_password(newPasswordClair)
    ConfirmationMotDePasse = hash_password(confirmPasswordClair)

    if(NewMotDePasse != ConfirmationMotDePasse):
        return "Le nouveau mot de passe et la confirmation ne sont pas identique"

    if(UserPasswordCurrent != AncienMotDePasseSaisie):
        return "L'ancien mot de passe est incorrect"

    if update_password(NewMotDePasse, UserPseudo, UserId):
        return "True"
    else:
        return "Echec pendant la mise à jour du mot de passe"


@app.route('/update_titre_poste', methods=['POST'])  # Fonction appelée en ajax
def update_titre_poste():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        NewTitrePoste = request.form["NewTitrePoste"]
        MdpUserClair = request.form["MdpUser"]

        if is_null_or_empty(idPoste, NewTitrePoste, MdpUserClair):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(MdpUserClair)
        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste(idPoste, NewTitrePoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/suppression_poste_accueil', methods=['POST'])
def suppression_poste_accueil():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        MdpUserClair = request.form["MdpUser"]

        if is_null_or_empty(idPoste, MdpUserClair):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(MdpUserClair)

        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if delete_poste(idPoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" SECTION ADMINISTRATION  """


@app.route('/administration')
def administration():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        isModeModeractionActive = bool(get_mode_moderation())
        msgTmp = get_last_message_information()
        if(msgTmp == False):
            messageInfo = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            messageInfo = map_result_to_message_information(msgTmp)
        ArrayUser = select_all_user()
        AllUser = map_array_result_bdd_to_array_utilisateur(ArrayUser)
        return render_template("Administration.html", user=session['utilisateur'], allUser=AllUser, messageInfo=messageInfo, isModeModeractionActive=isModeModeractionActive)
    else:
        return redirect(url_for('index'))


@app.route("/changement_role", methods=['POST'])  # Fonction appelée en ajax
def changement_role():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        pseudoUser = request.form["pseudoUser"]
        idUser = request.form["idUser"]
        AncienRoleUser = request.form["AncienRoleUser"]
        NouveauRoleUser = request.form["NouveauRoleUser"]
        mdpOfAdminSaisieClair = request.form["AdminPwd"]

        if is_null_or_empty(pseudoUser, idUser, AncienRoleUser, NouveauRoleUser, mdpOfAdminSaisieClair):
            return message_error_champs_vide()

        mdpOfAdminSaisie = hash_password(mdpOfAdminSaisieClair)
        mdpOfAdmin = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdpOfAdminSaisie != mdpOfAdmin:
            return "Le mot de passe entré est incorrect"

        isUpdate = update_role(idUser, pseudoUser, NouveauRoleUser)
        return str(isUpdate)
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route("/update_msg_information", methods=['POST'])
def update_msg_information():

    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        msg = request.form["Msg"]
        MdpUserSaisieClair = request.form["MdpUser"]

        if is_null_or_empty(msg, MdpUserSaisieClair):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(MdpUserSaisieClair)
        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        userIdCurrent = session['utilisateur']["IdUtilisateur"]
        if insert_message_information(msg, userIdCurrent):
            return "True"
        else:
            return "Le message n'as pas pu être actualisé"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/changement_mode_moderation', methods=['POST'])
def changement_mode_moderation():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:

        MdpUserSaisieClair = request.form["MdpUser"]
        ModeModerationVoulu = request.form["ModeModerationVoulu"]

        if is_null_or_empty(ModeModerationVoulu, MdpUserSaisieClair):
            return message_error_champs_vide()

        user = map_session_to_user(session['utilisateur'])
        MdpUserSaisie = hash_password(MdpUserSaisieClair)
        modeModerationVoulut = 1 if ModeModerationVoulu == "true" else 0

        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if update_mode_moderation(modeModerationVoulut, user.IdUtilisateur):
            return "True"
        else:
            return "Echec pendant la mise à jour du mode modération"
    else:
        return redirect(url_for('index'))


@app.route('/Moderation<idPage>')
def moderation(idPage):

    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        isModeModeractionActive = bool(get_mode_moderation())
        numPage = int(idPage)
        postesAM = []
        nbPosteAttenteModerationTotal = get_nb_poste_attente_moderation()
        resultArray = get_poste_attente_moderation_by_page(idPage)
        NbPageMax = calcul_nb_page_max(
            nbPosteAttenteModerationTotal, nbPosteByPage)

        for result in resultArray:
            postesAM.append(PosteAttenteModeration(
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

        return render_template("Moderation.html", user=session['utilisateur'], postesAM=postesAM, NbPageMax=NbPageMax, page=numPage, isModeModeractionActive=isModeModeractionActive)
    else:
        return redirect(url_for('index'))


@app.route('/banissement', methods=['POST'])  # Fonction appelée en ajax
def banissement():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        userBanId = request.form["userId"]
        MdpUserSaisieClair = request.form["MdpUser"]

        if is_null_or_empty(userBanId, MdpUserSaisieClair):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(MdpUserSaisieClair)
        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if ban_user(userBanId):
            return "True"
        else:
            return "L'utilisateur n'as pas pu être banni"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/update_poste_attente_moderation', methods=['POST'])
def update_poste_attente_moderation():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPostePAM = request.form["IdPoste"]
        isPostAccept = request.form["IsPostAccept"]

        if is_null_or_empty(idPostePAM, isPostAccept):
            return message_error_champs_vide()

        if isPostAccept == "true":
            accept_poste_pam(idPostePAM)
            return "True"
        else:
            delete_poste_pam(idPostePAM)
            return "True"
    else:
        return redirect(url_for('index'))


@app.route('/update_titre_pam', methods=['POST'])  # Fonction appelée en ajax
def update_titre_pam():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        NewTitrePoste = request.form["NewTitrePoste"]
        mdpClaire = request.form["MdpUser"]

        if is_null_or_empty(idPoste, NewTitrePoste, mdpClaire):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(mdpClaire)

        mdpCurrentUser = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdpCurrentUser:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste_pam(idPoste, NewTitrePoste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" FIN SECTION ADMINISTRATION  """


@app.route('/a_propos')
def a_propos():
    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)
    if 'utilisateur' in session:
        return render_template("A_Propos.html", messageInfo=messageInfo, user=session['utilisateur'])
    else:
        return render_template("A_Propos.html", messageInfo=messageInfo,)


@app.route('/cgu')
def cgu():
    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)
    if 'utilisateur' in session:
        return render_template("Cgu.html", messageInfo=messageInfo, user=session['utilisateur'])
    return render_template("Cgu.html", messageInfo=messageInfo)


@app.route('/contact')
def contact():
    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)
    if 'utilisateur' in session:
        return render_template("Contact.html", messageInfo=messageInfo, user=session['utilisateur'])
    return render_template("Contact.html", messageInfo=messageInfo)


@app.route('/aleatoire')
def aleatoire():
    result_array = get_random_poste()
    poste_array = []
    for result in result_array:
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    message_info = MessageInformation(
        "Sur la page aléatoire, le lien de partage redirige vers cette page et non pas vers les postes (vu qu'il change)", "Aucun", datetime.datetime.now())
    if 'utilisateur' in session:
        return render_template("Aleatoire.html", poste_array=poste_array, messageInfo=message_info, user=session['utilisateur'])
    else:
        return render_template("Aleatoire.html", poste_array=poste_array, messageInfo=message_info)


@app.route('/aide')
def aide():
    nbPosteTotal = get_nb_poste()
    msgTmp = get_last_message_information()
    if(msgTmp == False):
        messageInfo = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        messageInfo = map_result_to_message_information(msgTmp)
    if 'utilisateur' in session:
        return render_template("Aide.html", nbPosteTotal=nbPosteTotal, messageInfo=messageInfo, user=session['utilisateur'])
    return render_template("Aide.html", nbPosteTotal=nbPosteTotal, messageInfo=messageInfo)
