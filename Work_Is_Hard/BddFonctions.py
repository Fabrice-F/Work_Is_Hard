from flask import Flask, url_for, render_template
import hashlib
import sqlite3
import ConstanteAndTools

NB_POSTE_BY_PAGE = 3


def open_connexion():
    """ Permet de se connecter à la base de donnée"""
    conn = sqlite3.connect('WorkIsHard.db')
    return conn


def close_connexion(cursor, conn):
    """ Ferme la connexion """
    cursor.close()
    conn.close()


def connexion_utilisateur(pseudo):
    """ Recupère toutes les infos sur un utilisateur  

        Cette fonction est appelée lorqu'un l'utilisateur tente de se connecter
        et récupère les informations (hors mots de passe) si le pseudo existe
    """
    try:
        conn = open_connexion()  # appel la connexion a la bdd
        c = conn.cursor()   # creer le cursor qui va nous permettre de faire la requete
        request = f""" 
        SELECT IdUtilisateur,
            PseudoUtilisateur,
            NomUtilisateur,
            Prenom,
            DateNaissanceUtilisateur,
            Fk_IdRole
        FROM Utilisateur
        WHERE PseudoUtilisateur LIKE ?"""

        # Execute la requete et remplace le paramètre ? par la valeur pseudo
        # cela évite les failles xss
        result_array = c.execute(request, (pseudo,)).fetchall()
        if len(result_array) == 1:  # si un résultat c'est que l'utilisateur existe
            close_connexion(c, conn)  # fermeture de la connexion à la bdd
            return result_array[0]  # result le résultat obtenu
        else:                       # sinon c'est que l'utilisateur n'existe pas
            close_connexion(c, conn)
            return False
    except RuntimeError:  # si on a eut une erreur de connexion à la bdd alors on lève une erreur
        close_connexion(c, conn)
        return False


def insert_poste(user_id, titre_poste, lien_img):
    """ Fonction appelée lorque un poste doit être insérer un poste.

        Un poste est composé d'un utilisateur, un titre, et le lien de l'image.
        🛈 DateTime('now','localtime') renseigne la date au moment de l'insertion
        (inserer dans la table: poste)
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""INSERT INTO Poste (
                    Fk_IdUtilisateur,
                    TitrePoste,                    
                    AdressePoste,
                    DatePoste)
                VALUES (?,?,?,DateTime('now','localtime'))"""
        c.execute(request, (user_id, titre_poste, lien_img,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def insert_poste_attente_moderation(user_id, titre_poste, lien_img):
    """ Methode appelée pour l'insertion d'un poste  lorque le mode modération est activé. 

        Dans ce cas le poste est insérer dans une table différente que
        lorque le mode modération est désactivé (table: poste attente modération)
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""INSERT INTO PosteAttenteModération
                        (Fk_IdUtilisateur,
                        TitrePosteAttenteModeration,
                        AdressePosteAttenteModeration,
                        DatePosteAttenteModeration)
                    VALUES (?,?,?,DateTime('now','localtime'))"""
        c.execute(request, (user_id, titre_poste, lien_img,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_nb_poste():
    """ Recupere le nombre de poste total

        Cette fonction est utile pour la pagination et permet de savoir
        quand les boutons page suivante ou précèdente doivent être désactivés
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT COUNT(IdPoste)
                    FROM Poste ;"""
        result = c.execute(request).fetchone()[0]
        close_connexion(c, conn)
        return result
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_last_poste():
    """ Recupere les derniers postes en fonction de NB_POSTE_BY_PAGE
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT U.PseudoUtilisateur,
                        P.TitrePoste,
                        P.AdressePoste,
                        strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste),
                        P.IdPoste,
                        U.IdUtilisateur,
                        U.Fk_IdRole
                    FROM Poste AS P
                    INNER JOIN Utilisateur AS U ON
                        U.IdUtilisateur = P.Fk_IdUtilisateur 
                    ORDER BY IdPoste DESC
                    LIMIT {NB_POSTE_BY_PAGE}"""
        result_array = c.execute(request).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_poste_by_page(id_page):
    """ Récupère les postes en fonction de la page sur laquelle on se trouve

        grace au offset on peut récupérer des valeurs à partir de
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT U.PseudoUtilisateur,
                P.TitrePoste,
                P.AdressePoste,
                strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste),
                P.IdPoste,
                U.IdUtilisateur,
                U.Fk_IdRole
            FROM Poste AS P
            INNER JOIN Utilisateur AS U ON
            U.IdUtilisateur = P.Fk_IdUtilisateur
            ORDER BY P.DatePoste DESC
            LIMIT {NB_POSTE_BY_PAGE} OFFSET (?*{NB_POSTE_BY_PAGE})-{NB_POSTE_BY_PAGE};"""

        result_array = c.execute(request, (id_page,)).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_poste_attente_moderation_by_page(id_page):
    """ Récupère les postes en attente de modération 
        en fonction de la page sur laquelle on se trouve
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT IdPosteAttenteModération,
                        TitrePosteAttenteModeration,
                        AdressePosteAttenteModeration,
                        strftime('%d-%m-%Y à %H:%M:%S',DatePosteAttenteModeration),
                        U.IdUtilisateur,
                        U.PseudoUtilisateur,
                        U.Fk_IdRole
                    FROM PosteAttenteModération AS PAM
                    INNER JOIN Utilisateur AS U ON 
                        U.IdUtilisateur = PAM.Fk_IdUtilisateur
                    LIMIT 
                        {NB_POSTE_BY_PAGE} OFFSET (?*{NB_POSTE_BY_PAGE})-{NB_POSTE_BY_PAGE}"""
        result_array = c.execute(request, (id_page,)).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_nb_poste_attente_moderation():
    """ Recupere le nombre de poste total en attente de modération

        Cette fonction est utile pour la pagination et permet de savoir
        quand les boutons page suivante ou précèdente doivent être désactivés
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT 
                        count(IdPosteAttenteModération) 
                    FROM 
                        PosteAttenteModération"""
        result = c.execute(request).fetchone()[0]
        close_connexion(c, conn)
        return result
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_random_poste():
    """ Retourne grace a la fonction random sql un nombre de poste aléatoire

        Le nombre de psote aléatoire retourner dépends de NB_POSTE_BY_PAGE
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                    SELECT                 
                        U.PseudoUtilisateur,
                        P.TitrePoste,
                        P.AdressePoste,
                        strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste),
                        P.IdPoste,
                        U.IdUtilisateur,
                        U.Fk_IdRole
                    FROM Poste AS P
                    INNER JOIN Utilisateur AS U ON
                        U.IdUtilisateur = P.Fk_IdUtilisateur 
                    ORDER BY random() LIMIT {NB_POSTE_BY_PAGE}"""
        result_array = c.execute(request).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def if_pseudo_disponible(pseudo):
    """ Appelée lorque un utilisateur connecté souhaite changer de pseudo 
    vérifie si un pseudo existe

        Lorqu'un utilisateur tente de changer son pseudo
        si retourne un résultat c'est que le pseudo existe
    """
    conn = open_connexion()
    c = conn.cursor()
    request = f"""SELECT PseudoUtilisateur 
                FROM Utilisateur 
                WHERE PseudoUtilisateur LIKE ?"""
    result_array = c.execute(request, (pseudo,)).fetchall()
    if len(result_array) > 0:
        close_connexion(c, conn)
        return False
    else:
        close_connexion(c, conn)
        return True


def update_pseudo(pseudo_voulu, user_pseudo, user_id):
    """ Est appelée lorque le pseudo est disponble
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""Update Utilisateur 
            SET PseudoUtilisateur = ? 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ?;"""
        c.execute(request, (pseudo_voulu, user_pseudo, user_id,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def update_password(mdp, user_pseudo, user_id):
    """ Appelée lorque un utilisateur connecté souhaite changé de mots de passe
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""UPDATE Utilisateur
        SET MotDePasseUtilisateur = ?
        WHERE PseudoUtilisateur LIKE ? 
        AND IdUtilisateur = ?"""
        c.execute(request, (mdp, user_pseudo, user_id,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def select_all_user():
    """  Obtiens tous les utilisateurs sauf les administrateurs

        Sur la page administration => attribution rôle affiche tous les utilisateurs 
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
            SELECT IdUtilisateur,
                PseudoUtilisateur,
                NomUtilisateur,
                Prenom,
                DateNaissanceUtilisateur,
                Fk_IdRole
            FROM Utilisateur
            WHERE Fk_IdRole 
            IS NOT 3
            ORDER BY PseudoUtilisateur """
        result_array = c.execute(request).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_current_user_password(pseudo, Id):
    """ Récupère le mots de passe de l'utilisateur

        Evite que le password soit stocké dans la session, généralement utilisé pour 
        comparé le mot de passe envoyé du client  avec celui de la personne de la session
    """
    try:
        conn = open_connexion()
        c = conn.cursor()

        request = f"""
            SELECT MotDePasseUtilisateur 
            FROM Utilisateur 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ? """

        result = c.execute(request, (pseudo, Id,)).fetchone()

        if len(result) != 1:
            close_connexion(c, conn)
            return False
        else:
            close_connexion(c, conn)
            return result[0]
    except RuntimeError:
        close_connexion(c, conn)
        return False


def update_role(Id, pseudo, Role):
    """ Est appelée lorqu'un administrateur change le rôle d'un utilisateur

        role dispo : admin, modérateur , et posteur
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f""" 
            Update Utilisateur 
            SET Fk_IdRole = 
                (SELECT IdRole 
                FROM Role 
                WHERE NomRole Like ?)
            WHERE IdUtilisateur = ?
            AND PseudoUtilisateur LIKE ?
            """
        c.execute(request, (Role, Id, pseudo,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_last_message_information():
    """ Récupère le dernier message information dans la table du mëme nom

        Afin de l'afficher sur les pages.
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""SELECT 
                        MI.ContenuMessageInformation,
                        U.PseudoUtilisateur,
                        MI.DateMessageInformation      
                    FROM MessageInformation AS MI
                    INNER JOIN Utilisateur AS U ON
                        U.IdUtilisateur = MI.Fk_IdUtilisateurMessageInformation
                    ORDER BY IdMessageInformation 
                    DESC LIMIT 1"""
        result = c.execute(request).fetchone()
        if len(result) == 0:
            close_connexion(c, conn)
            return False
        else:
            close_connexion(c, conn)
            return result

    except RuntimeError:
        close_connexion(c, conn)
        return False


def insert_user_inscription(pseudo, nom, prenom, mot_de_passe_hash, date_naissance):
    """ Est appélée quand un utilisateur s'inscrit
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
            INSERT INTO Utilisateur 
                (PseudoUtilisateur, 
                NomUtilisateur, 
                Prenom, 
                MotDePasseUtilisateur, 
                DateNaissanceUtilisateur) 
            VALUES (?, ?, ?, ?, ?) 
        """
        c.execute(request, (pseudo, nom, prenom,
                            mot_de_passe_hash, date_naissance))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def insert_message_information(msg, id_user):
    """ Ajoute le message dans la base

        Le message s'écrit dans la partie administration
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
            INSERT INTO MessageInformation 
                (ContenuMessageInformation,
                Fk_IdUtilisateurMessageInformation,
                DateMessageInformation)
            VALUES(?,?,DateTime('now','localtime'))"""
        result = c.execute(request, (msg, id_user,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_mode_moderation():
    """ Retourne la valeur 0 si le mode est désactiver , 1 si activer

        Grace à cette valeur on peut savoir si on insert le poste 
        directement dans la table poste ou dans la table poste attente modération
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
            SELECT ModeModeration
            FROM Parametre"""
        result = c.execute(request).fetchone()[0]
        close_connexion(c, conn)
        return result
    except RuntimeError:
        close_connexion(c, conn)
        return False


def update_mode_moderation(isActive, user_id):
    """ Change la valeur du mode modération

    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
            UPDATE Parametre
            SET ModeModeration = ?,
                Fk_IdUtilisateurLastModification = ?,
                DateModification = DateTime('now','localtime')
            WHERE 3 =
            (SELECT U.Fk_IdRole 
            FROM Utilisateur AS U 
            WHERE U.IdUtilisateur = ?)"""
        c.execute(request, (isActive, user_id, user_id,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def ban_user(user_id):
    """ Active les contraintes et supprime les utilisateurs

        La suppression en cascade est activé lorsque l'on supprime 
        un utilisateur tous les postes et les postes attentes modérations sont 
        supprimés
    """
    try:
        conn = open_connexion()
        c = conn.cursor()

        request = f"""
        PRAGMA foreign_keys = ON;"""
        c.execute(request)
        conn.commit()

        request = f"""
        DELETE FROM Utilisateur
        WHERE IdUtilisateur = ?"""
        c.execute(request, (user_id,))

        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def accept_poste_pam(is_post_pam):
    """ Est appelée lorsqu'un poste en attente de modératrion est 
    accepté par un modérateur ou un administrateur
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                INSERT INTO Poste (Fk_IdUtilisateur,
                    TitrePoste,
                    AdressePoste,
                    DatePoste)
                SELECT Fk_IdUtilisateur,
                    TitrePosteAttenteModeration,
                    AdressePosteAttenteModeration,
                    DatePosteAttenteModeration
                    FROM PosteAttenteModération
                    WHERE IdPosteAttenteModération = ?"""
        c.execute(request, (is_post_pam,))
        conn.commit()
        close_connexion(c, conn)
        delete_poste_pam(is_post_pam) # Une fois le poste insérer dans poste on le supprime de poste attente modération
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def delete_poste(id_poste):
    """ Est appelée lorsqu'un modérateur ou administrateur supprime le poste
        via l'écran d'accueil ou aléatoire
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                DELETE FROM 
                    Poste 
                WHERE 
                    IdPoste = ? """
        c.execute(request, (id_poste,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def delete_poste_pam(is_post_pam):
    """ Est appelée lorsqu'un modérateur ou administrateur supprime le poste
        en attente de modération via l'écran modération
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                DELETE FROM 
                    PosteAttenteModération 
                WHERE 
                    IdPosteAttenteModération = ? """
        c.execute(request, (is_post_pam,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def update_title_poste(id_poste, new_titre):
    """ Actualise le titre d'un poste , uniquement accessible au modo et admin
        via la page l'accueil ou aléatoire
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                UPDATE 
                    Poste 
                SET 
                    TitrePoste = ? 
                WHERE 
                    IdPoste = ? """
        c.execute(request, (new_titre, id_poste,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def update_title_poste_pam(id_poste, new_titre):
    """ Actualise le titre d'un p.a.m , uniquement accessible au modo et admin
        via la page modération
    """
    try:
        conn = open_connexion()
        c = conn.cursor()
        request = f"""
                UPDATE 
                    PosteAttenteModération 
                SET 
                    TitrePosteAttenteModeration = ? 
                WHERE 
                    IdPosteAttenteModération = ? """
        c.execute(request, (new_titre, id_poste,))
        conn.commit()
        close_connexion(c, conn)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False
