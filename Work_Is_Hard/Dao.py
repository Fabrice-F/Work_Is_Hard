from flask import Flask, url_for, render_template
import hashlib , sqlite3
from datetime import *
import ConstanteAndTools

nbPosteByPage=3


def OpenConnexion():
    conn = sqlite3.connect('WorkIsHard.db')
    return conn


def closeConnexion(conn):
    conn.close()


#TODO fermer les connexions !!
def InsertPoste(UserId,TitrePoste,LienImg):
    try:
        conn = sqlite3.connect('WorkIsHard.db')
        c = conn.cursor()
        request =f"""INSERT INTO Poste (
                    Fk_IdUtilisateur,
                    TitrePoste,                    
                    AdressePoste,
                    DatePoste)
                VALUES (?,?,?,?);"""
        c.execute(request,(UserId,TitrePoste,LienImg,datetime.now()))
        conn.commit()
        return True
    except RuntimeError:
        return False

def getNbPoste():
    conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()
    request =f"""SELECT COUNT(IdPoste)
                FROM Poste ;"""
    result = c.execute(request).fetchone()[0]
    return result

def getLastPoste():
    conn = sqlite3.connect('WorkIsHard.db')
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
    return resultArray

def getPosteByPage(idPage):
    request =f"""SELECT U.PseudoUtilisateur,
                    P.TitrePoste,
                    P.AdressePoste,
                    strftime('%d-%m-%Y à %H:%M:%S', P.DatePoste)
                FROM Poste AS P
                INNER JOIN Utilisateur AS U ON
                U.IdUtilisateur = P.Fk_IdUtilisateur
                ORDER BY P.DatePoste DESC
                LIMIT {nbPosteByPage} OFFSET (?*{nbPosteByPage})-{nbPosteByPage};"""
    c = OpenConnexion().cursor()
    resultArray = c.execute(request,(idPage,)).fetchall()
    return resultArray

def getRandomPoste():
    return ""

def IfPseudoDisponible(pseudo):
    c = OpenConnexion().cursor()
    request ="""SELECT PseudoUtilisateur 
                FROM Utilisateur 
                WHERE PseudoUtilisateur LIKE ?"""
    resultArray = c.execute(request,(pseudo,)).fetchall()
    if len(resultArray)>0 :
        closeConnexion(c)
        return False
    else:
        closeConnexion(c)
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
        return True
    except RuntimeError:
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
        return True
    except RuntimeError:
        return False
