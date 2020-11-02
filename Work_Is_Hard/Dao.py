from flask import Flask, url_for, render_template
import hashlib , sqlite3
from datetime import *
import ConstanteAndTools

nbPosteByPage=3


def OpenConnexion():
    conn = sqlite3.connect('WorkIsHard.db')
    return conn

def closeConnexion(cursor,conn):
    cursor.close()
    conn.close()

def connexionUtilisateur(pseudo,mdp):
    try :
        conn= OpenConnexion()
        c= conn.cursor()
        request = f"""
        SELECT IdUtilisateur,
            PseudoUtilisateur,
            NomUtilisateur,
            Prenom,
            AgeUtilisateur,
            Fk_IdRole
        FROM Utilisateur
        WHERE PseudoUtilisateur = ?"""
        resultArray = c.execute(request,(pseudo,)).fetchall()
        if len(resultArray)==1:
            closeConnexion(c,conn)
            return resultArray[0]
        else :
            closeConnexion(c,conn)
            return False
    except RuntimeError:
        closeConnexion(c,conn)
        return False
    
#TODO fermer les connexions !!
def InsertPoste(UserId,TitrePoste,LienImg):
    try:
        conn= OpenConnexion()
        c = conn.cursor()
        request =f"""INSERT INTO Poste (
                    Fk_IdUtilisateur,
                    TitrePoste,                    
                    AdressePoste,
                    DatePoste)
                VALUES (?,?,?,?);"""
        c.execute(request,(UserId,TitrePoste,LienImg,datetime.now()))
        conn.commit()
        closeConnexion(c,conn)
        return True
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def getNbPoste():
    try:
        conn = conn= OpenConnexion()
        c = conn.cursor()
        request =f"""SELECT COUNT(IdPoste)
                    FROM Poste ;"""
        result = c.execute(request).fetchone()[0]
        closeConnexion(c,conn)
        return result
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def getLastPoste():
    try:
        conn = conn= OpenConnexion()
        c = conn.cursor()
        request = f"""SELECT U.PseudoUtilisateur,
                        P.TitrePoste,
                        P.AdressePoste,
                        strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste)
                    FROM Poste AS P
                    INNER JOIN Utilisateur AS U ON
                        U.IdUtilisateur = P.Fk_IdUtilisateur 
                    ORDER BY IdPoste DESC
                    LIMIT {nbPosteByPage} ;"""
        resultArray = c.execute(request).fetchall()
        closeConnexion(c,conn)
        return resultArray
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def getPosteByPage(idPage):
    try:
        conn= OpenConnexion()
        c= conn.cursor()
        request =f"""SELECT U.PseudoUtilisateur,
                P.TitrePoste,
                P.AdressePoste,
                strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste)
            FROM Poste AS P
            INNER JOIN Utilisateur AS U ON
            U.IdUtilisateur = P.Fk_IdUtilisateur
            ORDER BY P.DatePoste DESC
            LIMIT {nbPosteByPage} OFFSET (?*{nbPosteByPage})-{nbPosteByPage};"""

        resultArray = c.execute(request,(idPage,)).fetchall()
        closeConnexion(c,conn)
        return resultArray
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def getRandomPoste():
    return ""

def IfPseudoDisponible(pseudo):
    conn= OpenConnexion()
    c= conn.cursor()
    request ="""SELECT PseudoUtilisateur 
                FROM Utilisateur 
                WHERE PseudoUtilisateur LIKE ?"""
    resultArray = c.execute(request,(pseudo,)).fetchall()
    if len(resultArray)>0 :
        closeConnexion(c,conn)
        return False
    else:
        closeConnexion(c,conn)
        return True

def UpdatePseudo(pseudoVoulu,UserPseudo,userId):
    try:
        conn = OpenConnexion()
        c= conn.cursor()
        request = f"""Update Utilisateur 
            SET PseudoUtilisateur = ? 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ?;"""
        c.execute(request,(pseudoVoulu,UserPseudo,userId,))
        conn.commit()
        closeConnexion(c,conn)
        return True
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def UpdateMdp(mdp,userPseudo,userId):
    try:
        conn = OpenConnexion()
        c= conn.cursor()
        request = f"""UPDATE Utilisateur
        SET MotDePasseUtilisateur = ?
        WHERE PseudoUtilisateur LIKE ? 
        AND IdUtilisateur = ?"""
        c.execute(request,(mdp,userPseudo,userId,))
        conn.commit()
        closeConnexion(c,conn)
        return True
    except RuntimeError:
        closeConnexion(c,conn)
        return False

def SelectAllUser():
    try:
        conn = OpenConnexion()
        c = conn.cursor()
        request  = f"""
            SELECT IdUtilisateur,
                PseudoUtilisateur,
                NomUtilisateur,
                Prenom,
                AgeUtilisateur,
                Fk_IdRole
            FROM Utilisateur
            WHERE Fk_IdRole 
            IS NOT 3
            ORDER BY PseudoUtilisateur """
        resultArray= c.execute(request).fetchall()
        return resultArray
    except RuntimeError:
        closeConnexion(c,conn)
        return False


def getUserCurrentPasswd(pseudo,Id):
    try:
        conn = OpenConnexion()
        c= conn.cursor()

        request=f"""
            SELECT MotDePasseUtilisateur 
            FROM Utilisateur 
            WHERE PseudoUtilisateur LIKE ? 
            AND IdUtilisateur = ? """

        result = c.execute(request,(pseudo,Id,)).fetchone()

        if len(result)!=1:
            closeConnexion(c,conn)
            return False
        else:
            closeConnexion(c,conn)
            return result[0]
    except RuntimeError:
        closeConnexion(c,conn)
        return False
    
def UpdateRole(Id,pseudo,Role):
    try :
        conn = OpenConnexion()
        c = conn.cursor()
        request =f""" 
        Update Utilisateur 
        SET Fk_IdRole = 
            (SELECT IdRole 
            FROM Role 
            WHERE NomRole Like ?)
        WHERE IdUtilisateur = ?
        AND PseudoUtilisateur LIKE ?
        """
        c.execute(request,(Role,Id,pseudo,))
        conn.commit()
        return True
    except RuntimeError:
        return False

