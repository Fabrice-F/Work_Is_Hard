from flask import Flask, url_for, render_template
import hashlib
import sqlite3
import ConstanteAndTools

nbPosteByPage = 3


def OpenConnexion():
    conn = sqlite3.connect('WorkIsHard.db')
    return conn


def closeConnexion(cursor, conn):
    cursor.close()
    conn.close()


def connexionUtilisateur(pseudo, mdp):
    try:
        conn = OpenConnexion()
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
        resultArray = c.execute(request, (pseudo,)).fetchall()
        if len(resultArray) == 1:
            closeConnexion(c, conn)
            return resultArray[0]
        else:
            closeConnexion(c, conn)
            return False
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def InsertPoste(UserId, TitrePoste, LienImg):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""INSERT INTO Poste (
                    Fk_IdUtilisateur,
                    TitrePoste,                    
                    AdressePoste,
                    DatePoste)
                VALUES (?,?,?,DateTime('now','localtime'))"""
        c.execute(request, (UserId, TitrePoste, LienImg,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def InsertPosteAttenteModeration(UserId, TitrePoste, LienImg):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""INSERT INTO PosteAttenteModération
                        (Fk_IdUtilisateur,
                        TitrePosteAttenteModeration,
                        AdressePosteAttenteModeration,
                        DatePosteAttenteModeration)
                    VALUES (?,?,?,DateTime('now','localtime'))"""
        c.execute(request, (UserId, TitrePoste, LienImg,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getNbPoste():
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""SELECT COUNT(IdPoste)
                    FROM Poste ;"""
        result = c.execute(request).fetchone()[0]
        closeConnexion(c, conn)
        return result
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getLastPoste():
    try:
        conn = OpenConnexion()
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
                    LIMIT {nbPosteByPage}"""
        resultArray = c.execute(request).fetchall()
        closeConnexion(c, conn)
        return resultArray
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getPosteByPage(idPage):
    try:
        conn = OpenConnexion()
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
            LIMIT {nbPosteByPage} OFFSET (?*{nbPosteByPage})-{nbPosteByPage};"""

        resultArray = c.execute(request, (idPage,)).fetchall()
        closeConnexion(c, conn)
        return resultArray
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getPosteAttenteModerationByPage(idPage):
    try:
        conn = OpenConnexion()
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
                        {nbPosteByPage} OFFSET (?*{nbPosteByPage})-{nbPosteByPage}"""
        resultArray = c.execute(request, (idPage,)).fetchall()
        closeConnexion(c, conn)
        return resultArray
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getNbPosteAttenteModeration():
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""SELECT 
                        count(IdPosteAttenteModération) 
                    FROM 
                        PosteAttenteModération"""
        result = c.execute(request).fetchone()[0]
        closeConnexion(c, conn)
        return result
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def get_random_poste():
    try:
        conn = OpenConnexion()
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
        closeConnexion(c, conn)
        return result_array
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def IfPseudoDisponible(pseudo):
    conn = OpenConnexion()
    c = conn.cursor()
    request = f"""SELECT PseudoUtilisateur 
                FROM Utilisateur 
                WHERE PseudoUtilisateur LIKE ?"""
    resultArray = c.execute(request, (pseudo,)).fetchall()
    if len(resultArray) > 0:
        closeConnexion(c, conn)
        return False
    else:
        closeConnexion(c, conn)
        return True


def UpdatePseudo(pseudoVoulu, UserPseudo, userId):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""Update Utilisateur 
            SET PseudoUtilisateur = ? 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ?;"""
        c.execute(request, (pseudoVoulu, UserPseudo, userId,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def UpdateMdp(mdp, userPseudo, userId):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""UPDATE Utilisateur
        SET MotDePasseUtilisateur = ?
        WHERE PseudoUtilisateur LIKE ? 
        AND IdUtilisateur = ?"""
        c.execute(request, (mdp, userPseudo, userId,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def SelectAllUser():
    try:
        conn = OpenConnexion()
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
        resultArray = c.execute(request).fetchall()
        return resultArray
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getUserCurrentPasswd(pseudo, Id):
    try:
        conn = OpenConnexion()
        c = conn.cursor()

        request = f"""
            SELECT MotDePasseUtilisateur 
            FROM Utilisateur 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ? """

        result = c.execute(request, (pseudo, Id,)).fetchone()

        if len(result) != 1:
            closeConnexion(c, conn)
            return False
        else:
            closeConnexion(c, conn)
            return result[0]
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def UpdateRole(Id, pseudo, Role):
    try:
        conn = OpenConnexion()
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
        return True
    except RuntimeError:
        return False


def getLastMessageInformation():
    try:
        conn = OpenConnexion()
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
            closeConnexion(c, conn)
            return False
        else:
            closeConnexion(c, conn)
            return result

    except RuntimeError:
        closeConnexion(c, conn)
        return False

# TODO : Close la connexion


def insert_user_inscription(pseudo, nom, prenom, motdepasse_hashe, datenaissance):
    try:
        conn = OpenConnexion()
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
                            motdepasse_hashe, datenaissance))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def updateMessageInformation(msg, idUser):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
            INSERT INTO MessageInformation 
                (ContenuMessageInformation,
                Fk_IdUtilisateurMessageInformation,
                DateMessageInformation)
            VALUES(?,?,DateTime('now','localtime'))"""
        result = c.execute(request, (msg, idUser,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def getModeModeration():
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
            SELECT ModeModeration
            FROM Parametre"""
        result = c.execute(request).fetchone()[0]
        closeConnexion(c, conn)
        return result
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def updateModeModeration(isActive, userId):
    try:
        conn = OpenConnexion()
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
        c.execute(request, (isActive, userId, userId,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def BanUser(userId):
    try:
        conn = OpenConnexion()
        c = conn.cursor()

        request = f"""
        PRAGMA foreign_keys = ON;"""
        c.execute(request)
        conn.commit()

        request = f"""
        DELETE FROM Utilisateur
        WHERE IdUtilisateur = ?"""
        c.execute(request, (userId,))

        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def acceptPostePAM(idPostePAM):
    try:
        conn = OpenConnexion()
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
        c.execute(request, (idPostePAM,))
        conn.commit()
        closeConnexion(c, conn)
        deletePostePAM(idPostePAM)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def deletePoste(idPoste):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
                DELETE FROM 
                    Poste 
                WHERE 
                    IdPoste = ? """
        c.execute(request, (idPoste,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def deletePostePAM(idPostePAM):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
                DELETE FROM 
                    PosteAttenteModération 
                WHERE 
                    IdPosteAttenteModération = ? """
        c.execute(request, (idPostePAM,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def update_title_poste(IdPoste, newTitre):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
                UPDATE 
                    Poste 
                SET 
                    TitrePoste = ? 
                WHERE 
                    IdPoste = ? """
        c.execute(request, (newTitre, IdPoste,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False


def UpdateTitrePostePAM(IdPoste, newTitre):
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request = f"""
                UPDATE 
                    PosteAttenteModération 
                SET 
                    TitrePosteAttenteModeration = ? 
                WHERE 
                    IdPosteAttenteModération = ? """
        c.execute(request, (newTitre, IdPoste,))
        conn.commit()
        closeConnexion(c, conn)
        return True
    except RuntimeError:
        closeConnexion(c, conn)
        return False
