import math
import hashlib 
""" Comme les constantes n'existe pas en python:
en dehors de creer une classe avec getter setter
Nous avons créer ce fichier Constante&Tools où des méthodes
servent de constante ainsi que quelques méthodes outils"""

def CalculNbPageMax(numberPoste,nbPosteByPage):
    NbPageFloat = numberPoste / nbPosteByPage
    NbPage = math.ceil(NbPageFloat)
    return NbPage
    
def hashMdp(motdePassCLaire):
    h = hashlib.md5(motdePassCLaire.encode())
    return h.hexdigest()