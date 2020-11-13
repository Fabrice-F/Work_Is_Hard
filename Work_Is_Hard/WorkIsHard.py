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
    result_array = get_last_poste()
    nb_poste_totaux = get_nb_poste()

    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)
    poste_array = []
    for result in result_array:
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
    if 'utilisateur' in session:
        return render_template("Accueil.html", poste_array=poste_array,
                               nb_poste_totaux=nb_poste_totaux, message_info=message_info,
                               user=session['utilisateur'])

    return render_template("Accueil.html", poste_array=poste_array,
                           nb_poste_totaux=nb_poste_totaux, message_info=message_info)


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
    date_naissance = request.form["datenaissance"]

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

    if not verif_date_de_naissance(date_naissance):
        error = "Vous n'avez pas l'age requis pour vous inscrire"
        return render_template("inscription.html", error=error)

    mdp = hash_password(mot_de_passe_clair)
    mdp_confirm = hash_password(confirm_mdp)

    if mdp != mdp_confirm:
        error = "Le mots de passe et sa confirmation ne sont pas identique."
        return render_template("inscription.html", error=error)

    if if_pseudo_disponible(pseudo) == True:

        if insert_user_inscription(pseudo, nom, prenom, mdp, date_naissance):
            image_confirm = image_confirmation()
            return render_template("Transition.html", redirect=True, image_confirm=image_confirm, message="Votre inscription c'est bien déroulé, vous aller être redirigé vers la page d'accueil !")
        else:
            return "problème d'inscription"
    else:  # si pseudo existe
        error = "Le pseudo est déja pris"
        return render_template("inscription.html", pseudo=pseudo, error=error)


@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdp_clair = request.form["password"]

    if is_null_or_empty(pseudo, mdp_clair):
        return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

    mdp = hash_password(mdp_clair)
    result = connexion_utilisateur(pseudo, mdp)
    if result == False:
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    user_demande_connex = Utilisateur(
        result[0], result[1], result[2], result[3], result[4], result[5])
    mdp_current_user = get_current_user_password(
        user_demande_connex.PseudoUtilisateur, user_demande_connex.IdUtilisateur)

    if(mdp_current_user == False):
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    if user_demande_connex.PseudoUtilisateur == pseudo and mdp_current_user == mdp:
        session['utilisateur'] = user_demande_connex.__dict__
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
        msg_tmp = get_last_message_information()
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        return render_template("GestionDeCompte.html", user=session['utilisateur'], message_info=message_info)
    else:
        return render_template("inscription.html")


@app.route('/creation_de_poste')
def creation_de_poste():
    if 'utilisateur' in session:
        msg_tmp = get_last_message_information()
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        return render_template("CreationDePoste.html", user=session['utilisateur'], message_info=message_info)
    else:
        return redirect(url_for('index'))


@app.route('/publie_post', methods=['POST'])
def publie_post():
    if 'utilisateur' in session:
        titre_poste = request.form["TitrePoste"]
        lien_img = request.form["LienImg"]

        if is_null_or_empty(titre_poste, lien_img):
            return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

        user_id = session['utilisateur']["IdUtilisateur"]

        image_confirm = image_confirmation()

        if get_mode_moderation() == 1:
            if insert_poste_attente_moderation(user_id, titre_poste, lien_img):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, image_confirm=image_confirm, message="Votre poste a été pris en compte et est en attente de validation")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
        else:
            if insert_poste(user_id, titre_poste, lien_img):
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, image_confirm=image_confirm, message="Votre poste à été intégré !")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
    else:
        return redirect(url_for('index'))


@app.route('/page<id_page>')
def getPage(id_page):

    num_page = int(id_page)
    poste_array = []
    nb_poste_totaux = get_nb_poste()
    result_array = get_poste_by_page(id_page)
    nb_page_max = calcul_nb_page_max(nb_poste_totaux, nbPosteByPage)

    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)

    for result in result_array:
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    if 'utilisateur' in session:
        return render_template("Accueil.html", poste_array=poste_array, page=num_page, nb_poste_totaux=nb_poste_totaux, nb_page_max=nb_page_max, message_info=message_info, user=session['utilisateur'])
    else:
        return render_template("Accueil.html", poste_array=poste_array, page=num_page, nb_poste_totaux=nb_poste_totaux, nb_page_max=nb_page_max, message_info=message_info)


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
        user_id = session['utilisateur']["IdUtilisateur"]
        UserPseudo = session['utilisateur']["PseudoUtilisateur"]
        if update_pseudo(pseudoVoulu, UserPseudo, user_id):
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

    user_id = session['utilisateur']["IdUtilisateur"]
    UserPseudo = session['utilisateur']["PseudoUtilisateur"]
    UserPasswordCurrent = get_current_user_password(UserPseudo, user_id)

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

    if update_password(NewMotDePasse, UserPseudo, user_id):
        return "True"
    else:
        return "Echec pendant la mise à jour du mot de passe"


@app.route('/update_titre_poste', methods=['POST'])  # Fonction appelée en ajax
def update_titre_poste():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        idPoste = request.form["IdPoste"]
        Newtitre_poste = request.form["NewTitrePoste"]
        MdpUserClair = request.form["MdpUser"]

        if is_null_or_empty(idPoste, Newtitre_poste, MdpUserClair):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(MdpUserClair)
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste(idPoste, Newtitre_poste):
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

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
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
        msg_tmp = get_last_message_information()
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        ArrayUser = select_all_user()
        AllUser = map_array_result_bdd_to_array_utilisateur(ArrayUser)
        return render_template("Administration.html", user=session['utilisateur'], allUser=AllUser, message_info=message_info, isModeModeractionActive=isModeModeractionActive)
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
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
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

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_mode_moderation(modeModerationVoulut, user.IdUtilisateur):
            return "True"
        else:
            return "Echec pendant la mise à jour du mode modération"
    else:
        return redirect(url_for('index'))


@app.route('/Moderation<id_page>')
def moderation(id_page):

    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        isModeModeractionActive = bool(get_mode_moderation())
        num_page = int(id_page)
        postesAM = []
        nbPosteAttenteModerationTotal = get_nb_poste_attente_moderation()
        result_array = get_poste_attente_moderation_by_page(id_page)
        nb_page_max = calcul_nb_page_max(
            nbPosteAttenteModerationTotal, nbPosteByPage)

        for result in result_array:
            postesAM.append(PosteAttenteModeration(
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

        return render_template("Moderation.html", user=session['utilisateur'], postesAM=postesAM, nb_page_max=nb_page_max, page=num_page, isModeModeractionActive=isModeModeractionActive)
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
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
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
        Newtitre_poste = request.form["NewTitrePoste"]
        mdp_claire = request.form["MdpUser"]

        if is_null_or_empty(idPoste, Newtitre_poste, mdp_claire):
            return message_error_champs_vide()

        MdpUserSaisie = hash_password(mdp_claire)

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if MdpUserSaisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste_pam(idPoste, Newtitre_poste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" FIN SECTION ADMINISTRATION  """


@app.route('/a_propos')
def a_propos():
    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)
    if 'utilisateur' in session:
        return render_template("A_Propos.html", message_info=message_info, user=session['utilisateur'])
    else:
        return render_template("A_Propos.html", message_info=message_info,)


@app.route('/cgu')
def cgu():
    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)
    if 'utilisateur' in session:
        return render_template("Cgu.html", message_info=message_info, user=session['utilisateur'])
    return render_template("Cgu.html", message_info=message_info)


@app.route('/contact')
def contact():
    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)
    if 'utilisateur' in session:
        return render_template("Contact.html", message_info=message_info, user=session['utilisateur'])
    return render_template("Contact.html", message_info=message_info)


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
        return render_template("Aleatoire.html", poste_array=poste_array, message_info=message_info, user=session['utilisateur'])
    else:
        return render_template("Aleatoire.html", poste_array=poste_array, message_info=message_info)


@app.route('/aide')
def aide():
    nb_poste_totaux = get_nb_poste()
    msg_tmp = get_last_message_information()
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)
    if 'utilisateur' in session:
        return render_template("Aide.html", nb_poste_totaux=nb_poste_totaux, message_info=message_info, user=session['utilisateur'])
    return render_template("Aide.html", nb_poste_totaux=nb_poste_totaux, message_info=message_info)
