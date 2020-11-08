--
-- Fichier généré par SQLiteStudio v3.2.1 sur dim. nov. 8 20:49:45 2020
--
-- Encodage texte utilisé : UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table : MessageInformation
CREATE TABLE MessageInformation (IdMessageInformation INTEGER PRIMARY KEY AUTOINCREMENT, ContenuMessageInformation TEXT NOT NULL, Fk_IdUtilisateurMessageInformation REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, DateMessageInformation DATE NOT NULL);
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (1, 'Bienvenue! Le site est en cours de dévelopement, nous somme actuellement en train de travaillé sur la partie administration.', 3, '2020-11-02 13:08:19.120');
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (2, 'Bienvenue les amigos !! ', 3, '2020-11-02 21:39:02.602388');
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (3, 'Le mod modération en version 2 est en cours de développement... ce mode consiste a pouvoir modérer les postes directements depuis la page d accueil ! ', 3, '2020-11-06 17:44:59');
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (4, 'Le mode modération est à présent terminé, nous allons procéder à quelques changements sur la partie sécurité du site . ', 3, '2020-11-07 10:59:42');

-- Table : Parametre
CREATE TABLE Parametre (IdParametre INTEGER PRIMARY KEY AUTOINCREMENT, ModeModeration BOOLEAN NOT NULL DEFAULT (0), Fk_IdUtilisateurLastModification INTEGER REFERENCES Utilisateur (IdUtilisateur), DateModification DATE);
INSERT INTO Parametre (IdParametre, ModeModeration, Fk_IdUtilisateurLastModification, DateModification) VALUES (1, 1, 3, '2020-11-05 21:33:11');

-- Table : Poste
CREATE TABLE Poste (IdPoste INTEGER PRIMARY KEY AUTOINCREMENT, Fk_IdUtilisateur INTEGER REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, TitrePoste VARCHAR (255) NOT NULL, AdressePoste TEXT NOT NULL, DatePoste DATETIME NOT NULL);
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (1, 1, 'Quand tu reçois un compliment de ton patron ', 'http://www.reactiongifs.com/r/dreams.gif', '2020-10-24 22:33:38.042682');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (2, 2, 'Quand tu passe plus de temps à chercher comment pas travailler cas travailler ', 'https://media.giphy.com/media/3oKIPeYIJSEUcbKdt6/giphy.gif', '2020-10-24 22:34:30.848004');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (3, 3, 'Quand on me demande de venir travailler les week-end', 'https://media.giphy.com/media/S1ZnyFKKJ9rwc/giphy.gif', '2020-10-24 22:36:28.896501');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (4, 3, 'Quand ton collègue à une prime alors que c''est toi as réalisé la tâche demandée', 'https://media.giphy.com/media/60yTQLK9O7XlS/giphy.gif', '2020-10-24 22:40:36.893312');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (5, 3, '1h avant mes vacances', 'https://media.giphy.com/media/hOzfvZynn9AK4/giphy.gif', '2020-10-25 01:58:27.809197');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (6, 3, 'A mon retour de vacance', 'https://media.giphy.com/media/8EmeieJAGjvUI/giphy.gif', '2020-10-25 01:58:55.105298');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (7, 3, 'Quand ton chef te demande un service 2min avec la fin de journée', 'https://media.giphy.com/media/v6W3LmqM7ktGg/giphy.gif', '2020-10-25 02:00:08.924234');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (8, 3, 'Ce que je pense quand je remarque que le rapport que j''ai mis 3 jours à écrire n''est même pas lu', 'https://media.giphy.com/media/d2Z4i1TGqCunWBW0/giphy.gif', '2020-10-25 02:02:18.547440');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (9, 3, 'Quand je m''en rends compte', 'https://media.giphy.com/media/5tsjxsQXLl4GcNsd5S/giphy.gif', '2020-10-25 02:06:32.305625');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (10, 3, 'Quand je suis en réunion après mangé', 'https://media.giphy.com/media/Ssiutw5cCGvrG/giphy.gif', '2020-10-25 02:38:04.764179');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (11, 3, 'Quand on te convoque sans savoir pourquoi', 'https://media.giphy.com/media/bzSWoFLMKgo00/giphy.gif', '2020-10-25 02:40:04.415874');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (12, 3, 'Quand c''est le week-end', 'https://media.giphy.com/media/3vNa5YX2zG6mQ/giphy.gif', '2020-10-25 02:43:31.245028');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (13, 3, 'Minimum 2 fois par jour ..', 'https://i.pinimg.com/564x/e6/a5/b6/e6a5b6f6bee3e838f2afabb0ca62afd2.jpg', '2020-10-25 02:50:40.745512');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (14, 3, 'Quand tu trouve la solution pour le patron', 'https://media.giphy.com/media/Lk023zZqHJ3Zz4rxtV/giphy.gif', '2020-11-01 01:13:10.563380');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (15, 3, 'Qaund ton voision réussit ce que tu n''as jamais voulut tenté', 'https://media.giphy.com/media/oB1fcWnkI9vHCcjww7/giphy.gif', '2020-11-05 02:14:17.175451');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (16, 3, 'Quand tu chante trop fort et que tout le monde te remarque', 'https://media.giphy.com/media/tovL6Ax2AjldOWMtxC/giphy.gif', '2020-11-05 11:32:42.459214');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (17, 3, 'Quand on t''annonce qu''il y a une prime de fin d''année', 'https://media.giphy.com/media/yoJC2GnSClbPOkV0eA/giphy.gif', '2020-11-05 12:03:11.958577');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (18, 3, 'Quand on te présente ton nouvelle environnement de travail', 'https://media.giphy.com/media/13k4VSc3ngLPUY/giphy.gif', '2020-11-05 12:04:06.095498');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES (19, 1, 'Quand on t''annonce que tes heures supp ne seront pas payées !', 'https://media.giphy.com/media/13AXYJh2jDt2IE/giphy.gif', '2020-11-05 21:20:40');

-- Table : PosteAttenteModération
CREATE TABLE PosteAttenteModération (IdPosteAttenteModération INTEGER PRIMARY KEY AUTOINCREMENT, Fk_IdUtilisateur INTEGER REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, TitrePosteAttenteModeration VARCHAR (90) NOT NULL, AdressePosteAttenteModeration TEXT NOT NULL, DatePosteAttenteModeration DATE NOT NULL);

-- Table : Role
CREATE TABLE Role (IdRole INTEGER PRIMARY KEY AUTOINCREMENT, NomRole VARCHAR (128) NOT NULL);
INSERT INTO Role (IdRole, NomRole) VALUES (1, 'Posteur');
INSERT INTO Role (IdRole, NomRole) VALUES (2, 'Modérateur');
INSERT INTO Role (IdRole, NomRole) VALUES (3, 'Administrateur');

-- Table : Utilisateur
CREATE TABLE Utilisateur (IdUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT, PseudoUtilisateur VARCHAR (255) NOT NULL UNIQUE, MotDePasseUtilisateur VARCHAR (2056) NOT NULL, NomUtilisateur VARCHAR (255) NOT NULL, Prenom VARCHAR (255) NOT NULL, DateNaissanceUtilisateur DATE (2) NOT NULL, Fk_IdRole INTEGER REFERENCES Role (IdRole) DEFAULT (1));
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (1, 'Professeur', 'e10adc3949ba59abbe56e057f20f883e', 'Ayoub', 'Guillaume ', '16/05/2020', 2);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (2, 'Josue', 'ab4f63f9ac65152575886860dde480a1', 'Bayidikila', 'Josue', '16/05/2020', 1);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (3, 'FabriceF', '4a95de5cb88611bcac58da121c7922be', 'FERRERE', 'Fabrice', '30/08/1987', 3);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (4, 'Posteur1', 'e10adc3949ba59abbe56e057f20f883e', 'Alan', 'Mathis', '16/05/2020', 1);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (5, 'Moderateur1', 'e10adc3949ba59abbe56e057f20f883e', 'Eric', 'Bower', '03/02/2020', 2);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES (6, 'Administrateur1', 'e10adc3949ba59abbe56e057f20f883e', 'Megan', 'Cornish', '08/02/2019', 3);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
