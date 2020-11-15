from markupsafe import escape
import hashlib
import sqlite3
import re
from flask import Flask, url_for, render_template, session, request, redirect
from BddFonctions import *
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
    """ Route appeler lorsqu'un utilisateur tente de se connecter
    """
    pseudo = request.form["pseudo"] # request permet de récupérer les valeurs envoyé via le POST
    mdp_clair = request.form["password"]

    if is_null_or_empty(pseudo, mdp_clair):
        return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide())

    mdp = hash_password(mdp_clair)
    result = connexion_utilisateur(pseudo)  # vérifie si l'utilisateur existe
    if result == False:                     # retourne faux si l'utilisateur n'existe pas
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())

    user_demande_connex = Utilisateur(
        result[0], result[1], result[2], result[3], result[4], result[5])
    mdp_current_user = get_current_user_password(   # Si l'utilisateur existe dans la bdd récupère son mdp
        user_demande_connex.PseudoUtilisateur, user_demande_connex.IdUtilisateur)

    if(mdp_current_user == False):  # Si une erreur pendant la récupération du mots de passe dans la bdd
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion())


    # on compare si le mot de passe entrer est identique au mot de passe dans la bdd
    if user_demande_connex.PseudoUtilisateur.lower() == pseudo.lower() and mdp_current_user == mdp: 
        session['utilisateur'] = user_demande_connex.__dict__   # Si c'est le cas on transforme l'utilisateur en session
        return redirect(url_for('index'))
    else:
        return render_template("Error/ErrorPage.html", messageError=message_error_connexion()) # sinon on renvoi une erreur


@app.route('/logout')
def logout():
    """ Route appelé quand on clique sur déconnecté
    """
    session.clear() # efface la session de l'utilisateur qui appel la route
    return redirect(url_for('index'))   # on renvoi vers la fonction index donc page accueil '/'


@app.route('/gestion_de_compte')
def gestion_de_compte():
    """ Page pour pouvoir les informations sur son compte
    """
    if 'utilisateur' in session:        # Si l'utilisateur est connecter ( donc a une session )
        msg_tmp = get_last_message_information()    # Recupere les msg infos
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        return render_template("GestionDeCompte.html", user=session['utilisateur'], message_info=message_info) # on l'envoi sur la page gestion de compte
    else:                               # Si l'utilisateur n'as pas de session c'est qu'il n'est pas connecter donc retour sur accueil
        return render_template("inscription.html")


@app.route('/creation_de_poste')
def creation_de_poste():
    """ La où on peut faire un poste
    """
    if 'utilisateur' in session:    # Si l'utilisateur est connecter ( donc a une session )
        msg_tmp = get_last_message_information() # Recupere les msg infos
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:                       # Si l'utilisateur n'as pas de session c'est qu'il n'est pas connecter donc retour sur accueil
            message_info = map_result_to_message_information(msg_tmp)
        return render_template("CreationDePoste.html", user=session['utilisateur'], message_info=message_info)
    else:
        return redirect(url_for('index'))


@app.route('/publie_post', methods=['POST'])
def publie_post():
    """ Une fois que le poste à été validé
    """
    if 'utilisateur' in session:
        titre_poste = request.form["TitrePoste"]    # On récupère les valeurs envoyées par la méthode POST
        lien_img = request.form["LienImg"]          

        if is_null_or_empty(titre_poste, lien_img): # on vérifie si ces valeurs sont vide
            return render_template("Error/ErrorPage.html", messageError=message_error_champs_vide()) # erreur si ces valeurs sont vides

        user_id = session['utilisateur']["IdUtilisateur"]   # Recupère l'id de l'utilisateur qui as soumis le poste

        image_confirm = image_confirmation()    # Recupère une image pour confirmer le poste

        if get_mode_moderation() == 1:          # Si le mode modération est activé 
            if insert_poste_attente_moderation(user_id, titre_poste, lien_img): # on insert le poste dans la table poste attente modération
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, image_confirm=image_confirm, message="Votre poste a été pris en compte et est en attente de validation")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
        else:                                   # Si le mode modération est désactivé
            if insert_poste(user_id, titre_poste, lien_img):                    # on insert le poste dans la table poste
                return render_template("Transition.html", user=session['utilisateur'], redirect=True, image_confirm=image_confirm, message="Votre poste à été intégré !")
            else:
                return render_template("Error/ErrorPage.html", messageError="Un problème à eut lieu lors de l'enregistrement du poste")
    else:
        return redirect(url_for('index'))


@app.route('/page<id_page>')
def getPage(id_page):
    """ permet de gérer la pagination de la page d'accueil
    """
    num_page = int(id_page)                                                 # récupère le numéro de la page
    poste_array = []                                                        
    nb_poste_totaux = get_nb_poste()                                        # récupère le nombre total de poste
    result_array = get_poste_by_page(id_page)                               # récupère les postes en fonction de la page ( grace au offset dans la requete)
    nb_page_max = calcul_nb_page_max(nb_poste_totaux, NB_POSTE_BY_PAGE)     # calcul le nombre maximum de page 

    msg_tmp = get_last_message_information()                                
    if(msg_tmp == False):
        message_info = MessageInformation(
            "vide", "Aucun", datetime.datetime.now())
    else:
        message_info = map_result_to_message_information(msg_tmp)

    for result in result_array:                                             # Ajoute les résultats de la bdd dans le tableau
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    # si utilisateur est connecter on envoi les postes, la page, le nb totaux de poste, le nombre de page max,le message info, et l'utilisateur dans la session
    if 'utilisateur' in session:    
        return render_template("Accueil.html", poste_array=poste_array, page=num_page, nb_poste_totaux=nb_poste_totaux, nb_page_max=nb_page_max, message_info=message_info, user=session['utilisateur'])
    # sinon on envoi tout sauf la session
    else:
        return render_template("Accueil.html", poste_array=poste_array, page=num_page, nb_poste_totaux=nb_poste_totaux, nb_page_max=nb_page_max, message_info=message_info)


# Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
@app.route('/demande_si_pseudo_disponible', methods=['POST'])
def demande_si_pseudo_disponible():
    """ Appelé en AJAX : Permet qu'un utilisateur puisse changer de pseudo
    """
    if 'utilisateur' not in session:  # si pas d'utilisateur dans session on renvoi vers la fonction index donc route '/'
        return redirect(url_for('index'))

    pseudo_voulu = request.form["PseudoVoulu"]  # récupère la valeur envoyé par la méthode POST en ajax
    if is_null_or_empty(pseudo_voulu):          
        return message_error_champs_vide()      # On retourne directement un message d'erreur qui sera affiché dans le html 

    is_pseudo_disponible = if_pseudo_disponible(pseudo_voulu)       # Vérifie si le pseudo existe dans la bdd
    if is_pseudo_disponible:                                        
        user_id = session['utilisateur']["IdUtilisateur"]           
        user_pseudo = session['utilisateur']["PseudoUtilisateur"]   
        if update_pseudo(pseudo_voulu, user_pseudo, user_id):       # On actualise le pseudo en bdd
            return "True"   # True est attendu coté ajax pour signifié que tout c'est bien passé .
                            # Une fois cette valeur receptionné on déconnect l'utilisateur ( avec msg de prevention de 2s)
                            # (clear de sa sesssion ) afin qu'il se reconnect avec une nouvelle session avec son nouveau pseudo  
        else:
            return "Echec pendant la mise à jour du pseudo"     # On retourne directement le message qui sera affiché dans le html 
    else:                                                       # si le pseudo existe dans la bdd
        return "Le pseudo n'est pas disponible"                 # On retourne directement le message qui sera affiché dans le html 
    return


# Fonction appelée en ajax 
@app.route('/demande_changement_password', methods=['POST'])
def demande_changement_password():
    """ Appelé en AJAX : Permet qu'un utilisateur puisse changer de mots de passe
    """
    if 'utilisateur' not in session:    
        return redirect(url_for('index'))

    user_id = session['utilisateur']["IdUtilisateur"]           # recupère l'id utilisateur de la session qui appel la route
    user_pseudo = session['utilisateur']["PseudoUtilisateur"]   # recupère le pseudo utilisateur de la session qui appel la route
    user_password_current = get_current_user_password(user_pseudo, user_id) 

    old_password_clair = request.form["AncienMotDePasse"]   
    new_password_clair = request.form["NewMotDePasse"]      
    confirm_password_clair = request.form["ConfirmationMotDePasse"]

    if is_null_or_empty(old_password_clair, new_password_clair, confirm_password_clair): # verifie si l'un est vide
        return message_error_champs_vide()  # renvoi un message d'erreur dans le html pour signaler qu'un champs est vide

    # hash des mots de passe reçu via le POST
    ancien_mot_de_passe = hash_password(old_password_clair) 
    new_mot_de_passe = hash_password(new_password_clair)
    confirmation_mot_de_passe = hash_password(confirm_password_clair)


    if(new_mot_de_passe != confirmation_mot_de_passe):
        return "Le nouveau mot de passe et la confirmation ne sont pas identique" # message affiché dans le html

    # Si le mot de passe de l'utilisateur de la session est différent de celui envoyé (ancien mdp)
    if(user_password_current != ancien_mot_de_passe):
        return "L'ancien mot de passe est incorrect" 

    # TODO: Il aurait fallut ajouter toutes les règles de conformités concernant le mdp (regex)
    # mais nous n'avons pas eut le temps

    if update_password(new_mot_de_passe, user_pseudo, user_id): # on actualise le mdp de passe de l'user
        return "True"  
    else:
        return "Echec pendant la mise à jour du mot de passe" # message affiché dans le html


# Fonction appelée en ajax 
@app.route('/update_titre_poste', methods=['POST']) 
def update_titre_poste():
    """ Appelé lorsqu'un membre du staff actualise le titre d'un psote via l'écran d'accueil aléatoire
    """
    # On vérifie si l'utilisateur est bien connecter et si il a le role admin ou modo 
    # On aurait pu aussi simplement vérifié si c'est pas un posteur 
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

        if update_title_poste(id_poste, new_titre_poste):   # si tout ok on actualise le titre du poste grace a son id
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
@app.route('/suppression_poste_accueil', methods=['POST'])
def suppression_poste_accueil():
    """ Appelé lorsqu'un membre du staff souhaite supprimer un poste de l'accueil ou de la page aléatoire
    """
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

        if delete_poste(id_poste):  # supprime le poste grace a son id
            return "True"
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))   # si l'utilsateur n'est pas conncter on redirige vers l'accueil


""" SECTION ADMINISTRATION  """


@app.route('/administration')
def administration():
    """ Partie accessible uniquement lorsqu'un utilisateur a le role adminsitrateur 
    """
    # si l'utilisateur est connecter et a le role admin
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        is_mode_moderation_actif = bool(get_mode_moderation())     # on récupere la valeur du mode modération pour l'affiche en html
        msg_tmp = get_last_message_information()
        if(msg_tmp == False):
            message_info = MessageInformation(
                "vide", "Aucun", datetime.datetime.now())
        else:
            message_info = map_result_to_message_information(msg_tmp)
        array_user = select_all_user()                                      # On recupere tous les utilisateurs ( pas les admins ) pour pouvoir changer leurs roles
        all_user = map_array_result_bdd_to_array_utilisateur(array_user)    # Mapping des resultat bdd en utlisateur
        # On envoi toutes les infos au template 
        return render_template("Administration.html", user=session['utilisateur'], all_user=all_user, message_info=message_info, is_mode_moderation_actif=is_mode_moderation_actif)
    else:
        return redirect(url_for('index'))


@app.route("/changement_role", methods=['POST'])  # Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
def changement_role():
    """ Lorqu'un admin change le role d'un utilisateur.
    """
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:
        # recupère toutes les infos pour pouvoir actualiser le role de l'utilisiateur
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

        is_role_update = update_role(id_user, pseudo_user, nouveau_role_user) # Actualise le role de l'utilisateur
        return str(is_role_update)
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
@app.route("/update_msg_information", methods=['POST'])
def update_msg_information():
    """ Actualise le message d'information présent un peu partout sur le site
    """
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3: # obligation d'être un admin
        msg = request.form["Msg"]                       #recupère le message écrit
        mdp_user_saisieClair = request.form["MdpUser"]

        if is_null_or_empty(msg, mdp_user_saisieClair):
            return message_error_champs_vide()

        mdp_user_saisie = hash_password(mdp_user_saisieClair)
        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        user_id_current = session['utilisateur']["IdUtilisateur"]

        if insert_message_information(msg, user_id_current):    # met a jour le message et l'utilisateur qui l'as posté 
            return "True"
        else:
            return "Le message n'as pas pu être actualisé"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax 
@app.route('/changement_mode_moderation', methods=['POST'])
def changement_mode_moderation():
    """ Désactive ou active le mode modération des postes
    """
    if 'utilisateur' in session and session['utilisateur']['IdRoleUtilisateur'] == 3:

        mdp_user_saisieClair = request.form["MdpUser"]
        mode_moderation_voulu = request.form["ModeModerationVoulu"] # la valeur du mode modération voulu

        if is_null_or_empty(mode_moderation_voulu, mdp_user_saisieClair):
            return message_error_champs_vide()

        user = map_session_to_user(session['utilisateur'])
        mdp_user_saisie = hash_password(mdp_user_saisieClair)
        mode_moderation_voulu_bit = 1 if mode_moderation_voulu == "true" else 0 # ternaire qui renvoi une valeur binaire (0 ou 1) selon la mode voulut

        mdp_current_user = get_current_user_password(
            session['utilisateur']["PseudoUtilisateur"], session['utilisateur']["IdUtilisateur"])

        if mdp_user_saisie != mdp_current_user:
            return " Le mot de passe saisie est incorrect"

        if update_mode_moderation(mode_moderation_voulu_bit, user.IdUtilisateur):   # actualise le mode modération et l'utilisateur
            return "True"
        else:
            return "Echec pendant la mise à jour du mode modération"
    else:
        return redirect(url_for('index'))


@app.route('/Moderation<id_page>')
def moderation(id_page):
    """ Gère la pagination dans la page modération
    """
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        is_mode_moderation_actif = bool(get_mode_moderation())  # récup le mode modération pour l'afficher dans la page modération
        num_page = int(id_page)
        postes_attente_moderation = []
        nb_pam_totaux = get_nb_poste_attente_moderation()
        result_array = get_poste_attente_moderation_by_page(id_page)    # recupere les poste en fontion de la page (de plus ancien au plus récent)
        nb_page_max = calcul_nb_page_max(
            nb_pam_totaux, NB_POSTE_BY_PAGE)

        for result in result_array:
            postes_attente_moderation.append(PosteAttenteModeration(
                result[0], result[1], result[2], result[3], result[4], result[5], result[6]))
        
        # renvoi toutes les infos pour compléter la page ainsi que les postes en fonction du numéro de la page
        return render_template("Moderation.html", user=session['utilisateur'], postes_attente_moderation=postes_attente_moderation, nb_page_max=nb_page_max, page=num_page, is_mode_moderation_actif=is_mode_moderation_actif)
    else:
        return redirect(url_for('index'))


@app.route('/banissement', methods=['POST'])  # Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
def banissement():
    """ Permet de gérer le banissement d'un utilisateur

        info: Un membre du staff ne peut bannir que des membres qui ont un role inférieur au sien
        Le banissement produit des suppressions en cascades notemment au niveau des postes et des poste attente modération.
    """
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

        if ban_user(user_ban_id):   # banni l'utilisateur grace a son id
            return "True"
        else:
            return "L'utilisateur n'as pas pu être banni"
    else:
        return redirect(url_for('index'))


# Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
@app.route('/update_poste_attente_moderation', methods=['POST'])
def update_poste_attente_moderation():
    """ Accepte ou refuse le poste en attente de modération
    """
    if 'utilisateur' in session and (session['utilisateur']['IdRoleUtilisateur'] == 3 or session['utilisateur']['IdRoleUtilisateur'] == 2):
        is_post_pam = request.form["IdPoste"]
        is_post_accept = request.form["IsPostAccept"]   # recoit la valeur 'true' pour accepter et 'false' pour refuser 

        if is_null_or_empty(is_post_pam, is_post_accept):
            return message_error_champs_vide()

        if is_post_accept == "true":                # si on accepte
            accept_poste_pam(is_post_pam)           # on transfert le poste de la table poste attente modération a la table poste
            return "True"
        else:                                       # si on refuse
            delete_poste_pam(is_post_pam)           # on le supprime de la table poste attente modération
            return "True"
    else:
        return redirect(url_for('index'))


@app.route('/update_titre_pam', methods=['POST'])  # Fonction appelée en ajax ( permet d'éviter le rechargement de la page au click d'envoi )
def update_titre_pam():
    """ Actualise le titre d'un poste en attente de modération
    """
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

        if update_title_poste_pam(id_poste, new_titre_poste): # actualise le titre d'un poste grace a son id  
            return "True"                                     # et on recharge la page en js
        else:
            return "Le titre n'as pas pu être mis à jour"
    else:
        return redirect(url_for('index'))


""" FIN SECTION ADMINISTRATION  """


@app.route('/a_propos')
def a_propos():
    """ Affiche la page qui parle du site
    """
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
    """ Page ennuyeuse sur les conditions d'utilisation du site (copié d'un site tiers)
    """
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
    """ page qui permet de fournir des informations sur comment contacter les admins du site
    """
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
    """ page qui propose des postes en aléatoires
    """
    result_array = get_random_poste()
    poste_array = []
    for result in result_array:
        poste_array.append(Poste(
            result[0], result[1], result[2], result[3], result[4], result[5], result[6]))

    message_info = MessageInformation(
        "Sur la page aléatoire, le lien de partage redirige vers cette page et non pas vers les postes (vu qu'ils changent)", "Aucun", datetime.datetime.now())
    if 'utilisateur' in session:
        return render_template("Aleatoire.html", poste_array=poste_array, message_info=message_info, user=session['utilisateur'])
    else:
        return render_template("Aleatoire.html", poste_array=poste_array, message_info=message_info)


@app.route('/aide')
def aide():
    """ page qui présente des petits tutos.
    """
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
