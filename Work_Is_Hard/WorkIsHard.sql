
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table : MessageInformation
CREATE TABLE MessageInformation (IdMessageInformation INTEGER PRIMARY KEY AUTOINCREMENT, ContenuMessageInformation TEXT NOT NULL, Fk_IdUtilisateurMessageInformation REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, DateMessageInformation DATE NOT NULL);
INSERT INTO MessageInformation (ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES ('Bienvenue! Le site est en cours de développement, nous sommes actuellement en train de travailler sur la partie administration.', 3, '2020-11-02 13:08:19.120');
INSERT INTO MessageInformation (ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES ('Bienvenue les amigos !! ', 3, '2020-11-02 21:39:02.602388');
INSERT INTO MessageInformation (ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES ('Le mode modération en version 2 est en cours de développement... ce mode consiste a modérer les postes directement depuis la page d'' accueil ! ', 3, '2020-11-06 17:44:59');
INSERT INTO MessageInformation (ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES ('Le mode modération est à présent terminé, nous allons procéder à quelques changements sur la partie sécurité du site . ', 3, '2020-11-07 00:59:42');
INSERT INTO MessageInformation (ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES ('Le site est à présent terminé nous corrigeons les fautes.', 3, '2020-11-07 10:59:42');

-- Table : Parametre
CREATE TABLE Parametre (IdParametre INTEGER PRIMARY KEY AUTOINCREMENT, ModeModeration BOOLEAN NOT NULL DEFAULT (0), Fk_IdUtilisateurLastModification INTEGER REFERENCES Utilisateur (IdUtilisateur), DateModification DATE);
INSERT INTO Parametre ( ModeModeration, Fk_IdUtilisateurLastModification, DateModification) VALUES ( 1, 3, '2020-11-05 21:33:11');

-- Table : Poste
CREATE TABLE Poste (IdPoste INTEGER PRIMARY KEY AUTOINCREMENT, Fk_IdUtilisateur INTEGER REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, TitrePoste VARCHAR (255) NOT NULL, AdressePoste TEXT NOT NULL, DatePoste DATETIME NOT NULL);
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Quand tu reçois un compliment de ton patron', 'http://www.reactiongifs.com/r/dreams.gif', '2020-10-24 22:33:38.042682');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 2, 'Quand tu passes plus de temps à chercher comment ne pas travailler qu''a travailler', 'https://media.giphy.com/media/3oKIPeYIJSEUcbKdt6/giphy.gif', '2020-10-24 22:34:30.848004');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Quand on me demande de venir travailler les week-ends', 'https://media.giphy.com/media/S1ZnyFKKJ9rwc/giphy.gif', '2020-10-24 22:36:28.896501');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Quand ton collègue à une prime alors que c''est toi qui a réalisé la tâche demandée', 'https://media.giphy.com/media/60yTQLK9O7XlS/giphy.gif', '2020-10-24 22:40:36.893312');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 10, '1h avant mes vacances', 'https://media.giphy.com/media/hOzfvZynn9AK4/giphy.gif', '2020-10-25 01:58:27.809197');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 9, 'A mon retour de vacances', 'https://media.giphy.com/media/8EmeieJAGjvUI/giphy.gif', '2020-10-25 01:58:55.105298');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Quand ton chef te demande un service 2min avec la fin de journée', 'https://media.giphy.com/media/v6W3LmqM7ktGg/giphy.gif', '2020-10-25 02:00:08.924234');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Ce que je pense quand je remarque que le rapport que j''ai mis 3 jours à écrire n''est même pas lu', 'https://media.giphy.com/media/d2Z4i1TGqCunWBW0/giphy.gif', '2020-10-25 02:02:18.547440');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 8, 'Quand je m''en rends compte', 'https://media.giphy.com/media/5tsjxsQXLl4GcNsd5S/giphy.gif', '2020-10-25 02:06:32.305625');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 7, 'Quand je suis en réunion après manger', 'https://media.giphy.com/media/Ssiutw5cCGvrG/giphy.gif', '2020-10-25 02:38:04.764179');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 12, 'Quand on te convoque sans savoir pourquoi', 'https://media.giphy.com/media/bzSWoFLMKgo00/giphy.gif', '2020-10-25 02:40:04.415874');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 4, 'Quand c''est le week-end', 'https://media.giphy.com/media/3vNa5YX2zG6mQ/giphy.gif', '2020-10-25 02:43:31.245028');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 6, 'Minimum 2 fois par jour ..', 'https://i.pinimg.com/564x/e6/a5/b6/e6a5b6f6bee3e838f2afabb0ca62afd2.jpg', '2020-10-25 02:50:40.745512');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 5, 'Quand tu trouves la solution pour le patron', 'https://media.giphy.com/media/Lk023zZqHJ3Zz4rxtV/giphy.gif', '2020-11-01 01:13:10.563380');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 13, 'Qaund ton voisin réussit ce que tu n''as jamais voulu tenter', 'https://media.giphy.com/media/oB1fcWnkI9vHCcjww7/giphy.gif', '2020-11-05 02:14:17.175451');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 14, 'Quand tu chantes trop fort et que tout le monde te remarque', 'https://media.giphy.com/media/tovL6Ax2AjldOWMtxC/giphy.gif', '2020-11-05 11:32:42.459214');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 11, 'Quand on t''annonce qu''il y a une prime de fin d''année', 'https://media.giphy.com/media/yoJC2GnSClbPOkV0eA/giphy.gif', '2020-11-05 12:03:11.958577');
INSERT INTO Poste (Fk_IdUtilisateur, TitrePoste, AdressePoste, DatePoste) VALUES ( 3, 'Quand on te présente ton nouvel environnement de travail', 'https://media.giphy.com/media/13k4VSc3ngLPUY/giphy.gif', '2020-11-05 12:04:06.095498');

-- Table : PosteAttenteModération
CREATE TABLE PosteAttenteModération (IdPosteAttenteModération INTEGER PRIMARY KEY AUTOINCREMENT, Fk_IdUtilisateur INTEGER REFERENCES Utilisateur (IdUtilisateur) ON DELETE CASCADE, TitrePosteAttenteModeration VARCHAR (90) NOT NULL, AdressePosteAttenteModeration TEXT NOT NULL, DatePosteAttenteModeration DATE NOT NULL);
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 14, 'Quand ton projet est TERMINEEEEEEEEEEEEE', 'https://media.giphy.com/media/3o7abldj0b3rxrZUxW/giphy.gif', '2020-07-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 12, 'Quand les vacances d''été commencent dans 1 minute !', 'https://media.giphy.com/media/26tPplGWjN0xLybiU/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 9, 'Quand tu fais une blague à ton équipe et qui n''y''a que toi qui la comprend ! ', 'https://media.giphy.com/media/JsUoy8b2ZbgIw/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 14, 'Quand tu as pris la dernière dosette de café de la cuisine sans rien dire à personne... ', 'https://media.giphy.com/media/12PIT4DOj6Tgek/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 4, 'Quand ton augmentation est validée', 'https://media.giphy.com/media/10r2cSkQa2jPEY/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 1, 'Quand ton patron te fais un compliment sur ton job', 'https://media.giphy.com/media/wAxlCmeX1ri1y/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 14, 'Quand on t''annonce qu''il y aura une prime de fin d''année', 'https://media.giphy.com/media/26uf6o80xhd6MKGIw/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 14, 'Quand ton patron te dit de partir 1h avant', 'https://media.giphy.com/media/b5LTssxCLpvVe/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 6, 'Quand on parle de ton travail exemplaire devant tout le monde', 'https://media.giphy.com/media/LEdz8xl9uFxKw/giphy.gif', '2020-11-12 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 8, 'Quand un collègue que tu n''aimes pas te répond', 'https://media.giphy.com/media/xT0xewluEy8AMHXWWQ/giphy.gif', '2020-11-13 22:48:16');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 5, 'Quand t''as bouclé ta "to do list"', 'https://media.giphy.com/media/6oMKugqovQnjW/giphy.gif', '2020-02-21 18:54:42');
INSERT INTO PosteAttenteModération (Fk_IdUtilisateur,TitrePosteAttenteModeration,AdressePosteAttenteModeration,DatePosteAttenteModeration) VALUES( 2, 'Quand c''est le jour des frites au self', 'https://media.giphy.com/media/h8UyZ6FiT0ptC/giphy.gif', '2020-11-01 18:54:42');

-- Table : Role
CREATE TABLE Role (IdRole INTEGER PRIMARY KEY AUTOINCREMENT, NomRole VARCHAR (128) NOT NULL);
INSERT INTO Role (NomRole) VALUES ('Posteur');
INSERT INTO Role (NomRole) VALUES ('Modérateur');
INSERT INTO Role (NomRole) VALUES ('Administrateur');

-- Table : Utilisateur
CREATE TABLE Utilisateur (IdUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT, PseudoUtilisateur VARCHAR (255) NOT NULL UNIQUE, MotDePasseUtilisateur VARCHAR (2056) NOT NULL, NomUtilisateur VARCHAR (255) NOT NULL, Prenom VARCHAR (255) NOT NULL, DateNaissanceUtilisateur DATE (2) NOT NULL, Fk_IdRole INTEGER REFERENCES Role (IdRole) DEFAULT (1));
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Professeur', 'e10adc3949ba59abbe56e057f20f883e', 'Ayoub', 'Guillaume ', '1983-11-24', 2);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Josue', 'ab4f63f9ac65152575886860dde480a1', 'Bayidikila', 'Josue', '1992-11-12', 1);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('FabriceF', '4a95de5cb88611bcac58da121c7922be', 'FERRERE', 'Fabrice', '1987-08-30', 3);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Posteur', 'e10adc3949ba59abbe56e057f20f883e', 'Alan', 'Mathis', '1959-03-09', 1);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Moderateur', 'e10adc3949ba59abbe56e057f20f883e', 'Eric', 'Bower', '1948-04-28', 2);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Administrateur', 'e10adc3949ba59abbe56e057f20f883e', 'Megan', 'Cornish', '1970-01-01', 3);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Sue', 'e10adc3949ba59abbe56e057f20f883e', 'Sue', 'McGrath', '2000-03-24', 1);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Victor', 'e10adc3949ba59abbe56e057f20f883e', 'Victor', 'Simpson', '2000-01-01', 2);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Jennifer', 'e10adc3949ba59abbe56e057f20f883e', 'Jennifer', 'Lambert', '1993-12-21', 3);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Stewart', 'e10adc3949ba59abbe56e057f20f883e', 'Stewart', 'Bailey', '2001-12-14', 2);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Sally', 'e10adc3949ba59abbe56e057f20f883e', 'Sally', 'McDonald', '1998-07-17', 3);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Jack', 'e10adc3949ba59abbe56e057f20f883e', 'Jack', 'Paterson', '2002-11-13', 1);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Billy', 'e10adc3949ba59abbe56e057f20f883e', 'Joel', 'Billy', '2002-11-29', 2);
INSERT INTO Utilisateur (PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, DateNaissanceUtilisateur, Fk_IdRole) VALUES ('Fleur', 'e10adc3949ba59abbe56e057f20f883e', 'Jacinthe', 'Rose', '1990-11-12', 3);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
