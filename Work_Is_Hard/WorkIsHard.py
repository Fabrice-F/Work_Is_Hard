from markupsafe import escape
import hashlib
import sqlite3
import re
from flask import Flask, url_for, render_template, session, request, redirect
from BddFonctions  import *
from datetime import *
from ConstanteAndTools import *
from Classes import *


""" Fichier qui contient toutes les routes.
"""
TEMPS_SESSION = 60                                                  # temps de session choisit de 1 heure
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'                            # clé permettant de gérer les sessions
app.permanent_session_lifetime = timedelta(minutes=TEMPS_SESSION)   # initialisation du temps de session 
                                                                    # l'utilisateur est déconnecter après ce lapse de temps 


@app.route('/')
def index():
    """ Route principal (page d'accueil)
    """
    result_array = get_last_poste() # recupère tous les postes
    nb_poste_totaux = get_nb_poste()    # recupère le nombre de postes

    msg_tmp = get_last_message_information()    # recupère dernier message
    if(msg_tmp == False):                       # si aucun ou si ça se passe mal retourne vide comme message
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)   # sinon le map en objet message
    poste_array = []                                                # créait un tableau 
    for result in result_array:                                     # Parse tous les postes et les ajoutes dans le tableau
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
    if 'utilisateur' in session:   # si l'utilisateur à sa session qui existe alors on lui envoi toutes les info + les infos sessions
        return render_template("Accueil.html", poste_array=poste_array,
                               nb_poste_totaux=nb_poste_totaux, message_info=message_info,
                               user=session['utilisateur'])

    return render_template("Accueil.html", poste_array=poste_array, # sinon on lui envoi toutes les info mais sans les infos sessions (provoque des différences sur le template)
                           nb_poste_totaux=nb_poste_totaux, message_info=message_info)


@app.route('/inscription')
def inscription():
    """ renvoi le template de la page inscription
    """
    return render_template("inscription.html")


@app.route('/confirmation_inscription', methods=['POST'])
def confirmation_inscription():
    """ Confirme ou non l'inscription d'un utilisateur

        En plus de la sécurité client
    """
    pattern_regex_nom_prenom = "^[a-zA-Z]*$"        # regex qui délimite le nom et prenom seulement au lettre
    pattern_regex_info_pseudo = "^[a-zA-Z0-9]*$"    # regex qui délimite le pseudo au lettre et au chiffre
    # regex qui oblige l'utilisateur a voir 1 majuscule, 1 minuscule, 1 chiffre , 1 caractère spécial et au moin 8 caractères
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,100}$" 
    pattern_regex_password_user = re.compile(reg)

    # La méthode strip() ici permet de supprimé les espaces blanc situé avant ou après 
    # les valeurs entrés par l'utilisateur
    nom = request.form["nom"].strip()   
    prenom = request.form["prenom"].strip()
    pseudo = request.form["pseudo"].strip()
    mot_de_passe_clair = request.form["motdepasse"].strip()
    confirm_mdp = request.form["confirm_mdp"].strip()
    date_naissance = request.form["datenaissance"]

    # Si le nom est vide,null ou encore ne réponds pas aux exigences de la regex (autre que lettre) alors incorrect
    if is_null_or_empty(nom) or not re.match(pattern_regex_nom_prenom, nom):
        error = "Le champs nom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    # Si la taille du nom n'est pas situé entre 2 caractères mini et 30 maxi alors incorrect.
    if not size_string_is_correct(nom, 2, 30):
        error = "Le champs nom ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    # Si le prenom est vide,null ou encore ne réponds pas aux exigences de la regex (autre que lettre) alors incorrect
    if is_null_or_empty(prenom) or not re.match(pattern_regex_nom_prenom, prenom):
        error = "Le champs prenom est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    # Si la taille du prenom n'est pas situé entre 2 caractères mini et 30 maxi alors incorrect.
    if not size_string_is_correct(prenom, 2, 30):
        error = "Le champs prenom ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    # Si le pseudo est vide,null ou encore ne réponds pas aux exigences de la regex (autre que chiffre et lettre) alors incorrect
    if is_null_or_empty(pseudo) or not re.match(pattern_regex_info_pseudo, pseudo):
        error = "Le champs pseudo est vide ou contient des caractères non appropriés."
        return render_template("inscription.html", error=error)

    # Si la taille du prenom n'est pas situé entre 3 caractères mini et 15 maxi alors incorrect.
    if not size_string_is_correct(pseudo, 3, 15):
        error = "Le champs pseudo ne contient pas le nombre de caractères appropriés."
        return render_template("inscription.html", error=error)

    # Si mot de passe non hashé est vide alors incorrect
    if is_null_or_empty(mot_de_passe_clair):
        error = "Le champs mot de passe est vide..."
        return render_template("inscription.html", error=error)

    # Si confirmation mot de passe non hashé est vide alors incorrect
    if is_null_or_empty(confirm_mdp):
        error = "Le champs confirmation mots de passe est vide..."
        return render_template("inscription.html", error=error)

    # Si le mot de passe non hashé ne réponds pas aux exigences de la regex (condition plus haut ^^) alors incorrect
    if not re.search(pattern_regex_password_user, mot_de_passe_clair):
        error = "Le champs mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    # Si la confirmation mot de passe non hashé ne réponds pas aux exigences de la regex (condition plus haut ^^) alors incorrect
    if not re.search(pattern_regex_password_user, confirm_mdp):
        error = "Le champs confirmation mot de passe ne contient pas 8 caractères dont 1 majuscule,1 mininuscule, 1 chiffre, 1 caractère spécial ..."
        return render_template("inscription.html", error=error)

    # Si la date de naissance utilisateur est plus jeune que la date du jour -18 ans alors incorrect
    if not verif_date_de_naissance(date_naissance):
        error = "Vous n'avez pas l'age requis pour vous inscrire"
        return render_template("inscription.html", error=error)

    mdp = hash_password(mot_de_passe_clair) # hash mdp
    mdp_confirm = hash_password(confirm_mdp) # hash confirm mdp

    if mdp != mdp_confirm:  # Si mots de passe différents alors incorrect
        error = "Le mots de passe et sa confirmation ne sont pas identique."
        return render_template("inscription.html", error=error)

    if if_pseudo_disponible(pseudo) == True:    # Si pseudo disponbile

        if insert_user_inscription(pseudo, nom, prenom, mdp, date_naissance):   # insertion de l'user dans la bdd
            image_confirm = image_confirmation()                                # recupère le lien d'une image de confirmation
            return render_template("Transition.html", redirect=True, image_confirm=image_confirm, 
                                    message="Votre inscription c'est bien déroulé, vous aller être redirigé vers la page d'accueil !") # on renvoi vers la page de transition
        else:                                                                   # sinon problème d'insertion dans la bdd
            return "problème d'inscription"
    else:                                       # Sinon c'est que le pseudo existe
        error = "Le pseudo est déja pris"
        return render_template("inscription.html", pseudo=pseudo, error=error)


@app.route('/login', methods=['POST'])
def login():
    pseudo = request.form["pseudo"]
    mdp_clair = request.form["password"]

    if is_null_or_empty(pseudo, mdp_clair):
        return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

    mdp = hash_password(mdp_clair)
    result = connexion_utilisateur(pseudo)
    if result == False:
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    user_demande_connex = Utilisateur(
        result[0], result[1], result[2], result[3], result[4], result[5])
    mdp_current_user = get_current_user_password(
        user_demande_connex.PseudoUtilisateur, user_demande_connex.IdUtilisateur)

    if(mdp_current_user == False):
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    if user_demande_connex.PseudoUtilisateur.lower() == pseudo.lower() and mdp_current_user == mdp:
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
    nb_page_max = calcul_nb_page_max(nb_poste_totaux, NB_POSTE_BY_PAGE)

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
    if 'utilisateur' not in session:  # test pour voir si pas d'utilisateur dans session
        return redirect(url_for('index'))

    pseudo_voulu = request.form["PseudoVoulu"]
    if is_null_or_empty(pseudo_voulu):
        return message_error_champs_vide()

    is_pseudo_disponible = if_pseudo_disponible(pseudo_voulu)
    if is_pseudo_disponible:
        user_id = session['utilisateur']["IdUtilisateur"]
        user_pseudo = session['utilisateur']["PseudoUtilisateur"]
        if update_pseudo(pseudo_voulu, user_pseudo, user_id):
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
    user_pseudo = session['utilisateur']["PseudoUtilisateur"]
    user_password_current = get_current_user_password(user_pseudo, user_id)

    old_password_clair = request.form["AncienMotDePasse"]
    new_password_clair = request.form["NewMotDePasse"]
    confirm_password_clair = request.form["ConfirmationMotDePasse"]

    if is_null_or_empty(old_password_clair, new_password_clair, confirm_password_clair):
        return message_error_champs_vide()

    ancien_mot_de_passe = hash_password(old_password_clair)
    new_mot_de_passe = hash_password(new_password_clair)
    confirmation_mot_de_passe = hash_password(confirm_password_clair)

    if(new_mot_de_passe != confirmation_mot_de_passe):
        return "Le nouveau mot de passe et la confirmation ne sont pas identique"

    if(user_password_current != ancien_mot_de_passe):
        return "L'ancien mot de passe est incorrect"

    if update_password(new_mot_de_passe, user_pseudo, user_id):
        return "True"
    else:
        return "Echec pendant la mise à jour du mot de passe"


@app.route('/update_titre_poste', methods=['POST'])  # Fonction appelée en ajax
def update_titre_poste():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        id_poste = request.form["IdPoste"]
        new_titre_poste = request.form["NewTitrePoste"]
        mdp_user_clair = request.form["MdpUser"]

        if is_null_or_empty(id_poste, new_titre_poste, mdp_user_clair):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_user_clair)
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste(id_poste, new_titre_poste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/suppression_poste_accueil', methods=['POST'])
def suppression_poste_accueil():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        id_poste = request.form["IdPoste"]
        mdp_user_clair = request.form["MdpUser"]

        if is_null_or_empty(id_poste, mdp_user_clair):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_user_clair)

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if delete_poste(id_poste):
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" SECTION ADMINISTRATION  """


@app.route('/administration')
def administration():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        is_mode_moderation_actif = bool(get_mode_moderation())
        msg_tmp = get_last_message_information()
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        array_user = select_all_user()
        all_user = map_array_result_bdd_to_array_utilisateur(array_user)
        return render_template("Administration.html", user=session['utilisateur'], all_user=all_user, message_info=message_info, is_mode_moderation_actif=is_mode_moderation_actif)
    else:
        return redirect(url_for('index'))


@app.route("/changement_role", methods=['POST'])  # Fonction appelée en ajax
def changement_role():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        pseudo_user = request.form["pseudoUser"]
        id_user = request.form["idUser"]
        ancien_role_user = request.form["AncienRoleUser"]
        nouveau_role_user = request.form["NouveauRoleUser"]
        mdp_admin_saisie_clair = request.form["AdminPwd"]

        if is_null_or_empty(pseudo_user, id_user, ancien_role_user, nouveau_role_user, mdp_admin_saisie_clair):
            return message_error_champs_vide()

        mdp_admin_saisie = hash_password(mdp_admin_saisie_clair)
        current_mdp_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_admin_saisie != current_mdp_user:
            return "Le mot de passe entré est incorrect"

        is_role_update = update_role(id_user, pseudo_user, nouveau_role_user)
        return str(is_role_update)
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route("/update_msg_information", methods=['POST'])
def update_msg_information():

    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        msg = request.form["Msg"]
        mdp_user_saisieClair = request.form["MdpUser"]

        if is_null_or_empty(msg, mdp_user_saisieClair):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_user_saisieClair)
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        user_id_current = session['utilisateur']["IdUtilisateur"]
        if insert_message_information(msg, user_id_current):
            return "True"
        else:
            return "Le message n'as pas pu être actualisé"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/changement_mode_moderation', methods=['POST'])
def changement_mode_moderation():
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:

        mdp_user_saisieClair = request.form["MdpUser"]
        mode_moderation_voulu = request.form["ModeModerationVoulu"]

        if is_null_or_empty(mode_moderation_voulu, mdp_user_saisieClair):
            return message_error_champs_vide()

        user = map_session_to_user(session['utilisateur'])
        mdp_user_saisie = hash_password(mdp_user_saisieClair)
        mode_moderation_voulu_bit = 1 if mode_moderation_voulu == "true" else 0

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_mode_moderation(mode_moderation_voulu_bit, user.IdUtilisateur):
            return "True"
        else:
            return "Echec pendant la mise à jour du mode modération"
    else:
        return redirect(url_for('index'))


@app.route('/Moderation<id_page>')
def moderation(id_page):

    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        is_mode_moderation_actif = bool(get_mode_moderation())
        num_page = int(id_page)
        postes_attente_moderation = []
        nb_pam_totaux = get_nb_poste_attente_moderation()
        result_array = get_poste_attente_moderation_by_page(id_page)
        nb_page_max = calcul_nb_page_max(
            nb_pam_totaux, NB_POSTE_BY_PAGE)

        for result in result_array:
            postes_attente_moderation.append(PosteAttenteModeration(
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

        return render_template("Moderation.html", user=session['utilisateur'], postes_attente_moderation=postes_attente_moderation, nb_page_max=nb_page_max, page=num_page, is_mode_moderation_actif=is_mode_moderation_actif)
    else:
        return redirect(url_for('index'))


@app.route('/banissement', methods=['POST'])  # Fonction appelée en ajax
def banissement():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        user_ban_id = request.form["userId"]
        mdp_user_saisieClair = request.form["MdpUser"]

        if is_null_or_empty(user_ban_id, mdp_user_saisieClair):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_user_saisieClair)
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if ban_user(user_ban_id):
            return "True"
        else:
            return "L'utilisateur n'as pas pu être banni"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax
@app.route('/update_poste_attente_moderation', methods=['POST'])
def update_poste_attente_moderation():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        is_post_pam = request.form["IdPoste"]
        is_post_accept = request.form["IsPostAccept"]

        if is_null_or_empty(is_post_pam, is_post_accept):
            return message_error_champs_vide()

        if is_post_accept == "true":
            accept_poste_pam(is_post_pam)
            return "True"
        else:
            delete_poste_pam(is_post_pam)
            return "True"
    else:
        return redirect(url_for('index'))


@app.route('/update_titre_pam', methods=['POST'])  # Fonction appelée en ajax
def update_titre_pam():
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        id_poste = request.form["IdPoste"]
        new_titre_poste = request.form["NewTitrePoste"]
        mdp_claire = request.form["MdpUser"]

        if is_null_or_empty(id_poste, new_titre_poste, mdp_claire):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_claire)

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_title_poste_pam(id_poste, new_titre_poste):
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
