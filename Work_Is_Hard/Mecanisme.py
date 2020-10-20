from flask import Flask, url_for, render_template
import hashlib , sqlite3

conn = sqlite3.connect('WorkIsHard.db')
c = conn.cursor()


def GoToPage(page):
    return render_template(page)


def ExecuteRequest(requete):
    return c.execute(requete)