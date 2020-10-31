from flask import Flask, url_for, render_template
import hashlib , sqlite3
from datetime import *
import ConstanteAndTools

nbPosteByPage=3


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
    conn = sqlite3.connect('WorkIsHard.db')
    c = conn.cursor()
    resultArray = c.execute(request,(idPage,)).fetchall()
    return resultArray


def getRandomPoste():
    return ""
