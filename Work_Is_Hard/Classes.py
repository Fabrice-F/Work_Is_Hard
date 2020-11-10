class Utilisateur:
    def __init__(self, identifiant, pseudo, nom, prenom, age, role):
        self.IdUtilisateur = identifiant
        self.PseudoUtilisateur = pseudo
        self.NomUtilisateur = nom
        self.PrenomUtilisateur = prenom
        self.DateNaissanceUtilisateur = age
        self.IdRoleUtilisateur = role
        self.NomRole = self.getNomRole()

    def getNomRole(self):
        if self.IdRoleUtilisateur == 1:
            return "Posteur"
        elif self.IdRoleUtilisateur == 2:
            return "Modérateur"
        else:
            return "Administrateur"


class Poste:
    def __init__(self, pseudo, titre, adresse, date, idPoste, idUser, idRoleUser):
        self.PseudoUtilisateurPoste = pseudo
        self.TitrePoste = titre
        self.AdressePoste = adresse
        self.DatePoste = date
        self.IdPoste = idPoste
        self.IdUser = idUser
        self.IdRoleUserPoste = idRoleUser


class PosteAttenteModeration:
    def __init__(self, Id, titre, adresse, date, idUserPoste, userPseudo, userRole):
        self.IdPAM = Id
        self.TitrePAM = titre
        self.AdressePAM = adresse
        self.DatePAM = date
        self.UserIdPAM = idUserPoste
        self.UserPseudoPAM = userPseudo
        self.UserRolePAM = userRole
        self.UserNomRole = self.getNomRole()

    def getNomRole(self):
        if self.UserRolePAM == 1:
            return "Posteur"
        elif self.UserRolePAM == 2:
            return "Modérateur"
        else:
            return "Administrateur"


class MessageInformation:
    def __init__(self, contenu, pseudo, date):
        self.ContenuMessageInformation = contenu
        self.Pseudo = pseudo
        self.DateMessageInformation = date
