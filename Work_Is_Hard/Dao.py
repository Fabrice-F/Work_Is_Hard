from flask import Flask, url_for, render_template
import hashlib
import sqlite3
import ConstanteAndTools

NB_POSTE_BY_PAGE = 3


def open_connexion():
    conn = sqlite3.connect('WorkIsHard.db')
    return conn


def close_connexion(cursor, conn):
    cursor.close()
    conn.close()


def connexion_utilisateur(pseudo, mdp):
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
        WHERE PseudoUtilisateur = ?"""
        result_array = c.execute(request, (pseudo,)).fetchall()
        if len(result_array) == 1:
            close_connexion(c, conn)
            return result_array[0]
        else:
            close_connexion(c, conn)
            return False
    except RuntimeError:
        close_connexion(c, conn)
        return False


def insert_poste(user_id, titre_poste, lien_img):
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
                    ORDER BY random() LIMIT 3"""
        result_array = c.execute(request).fetchall()
        close_connexion(c, conn)
        return result_array
    except RuntimeError:
        close_connexion(c, conn)
        return False


def if_pseudo_disponible(pseudo):
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
        close_connexion(c, conn)
        conn.commit()
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def get_last_message_information():
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

# TODO : Close la connexion


def insert_user_inscription(pseudo, nom, prenom, mot_de_passe_hash, date_naissance):
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
        delete_poste_pam(is_post_pam)
        return True
    except RuntimeError:
        close_connexion(c, conn)
        return False


def delete_poste(id_poste):
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
