from flask import Flask, url_for, render_template
import hashlib , sqlite3
from datetime import *

conn = sqlite3.connect('WorkIsHard.db')
c = conn.cursor()


def InsertPoste(UserId,TitrePoste,LienImg):
    try:
        conn = sqlite3.connect('WorkIsHard.db')
        c = conn.cursor()
        request =f"""INSERT INTO Poste (
                    Fk_IdUtilisateur,
                    AdressePoste,
                    TitrePoste,
                    DatePoste)
                VALUES (?,?,?,?);"""
        c.execute(request,(UserId,TitrePoste,LienImg,datetime.now()))
        conn.commit()
        return True
    except RuntimeError:
        return False

