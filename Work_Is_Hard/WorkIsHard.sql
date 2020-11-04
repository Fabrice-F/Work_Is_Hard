--
-- Fichier généré par SQLiteStudio v3.2.1 sur mer. nov. 4 10:50:23 2020
--
-- Encodage texte utilisé : UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table : MessageInformation
CREATE TABLE MessageInformation (IdMessageInformation INTEGER PRIMARY KEY AUTOINCREMENT, ContenuMessageInformation TEXT NOT NULL, Fk_IdUtilisateurMessageInformation REFERENCES Utilisateur (IdUtilisateur), DateMessageInformation DATE NOT NULL);
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (1, 'Bienvenue! Le site est en cours de dévelopement, nous somme actuellement en train de travaillé sur la partie administration.', 3, '2020-11-02 13:08:19.120');
INSERT INTO MessageInformation (IdMessageInformation, ContenuMessageInformation, Fk_IdUtilisateurMessageInformation, DateMessageInformation) VALUES (2, 'Bienvenue les amigos !! ', 3, '2020-11-02 21:39:02.602388');

-- Table : Parametre
CREATE TABLE Parametre (IdParametre INTEGER PRIMARY KEY AUTOINCREMENT, ModeModeration BOOLEAN NOT NULL DEFAULT (0));
INSERT INTO Parametre (IdParametre, ModeModeration) VALUES (1, 0);

-- Table : Poste
CREATE TABLE Poste (IdPoste INTEGER PRIMARY KEY AUTOINCREMENT, Fk_IdUtilisateur INTEGER REFERENCES Utilisateur (IdUtilisateur), AdressePoste TEXT NOT NULL, TitrePoste VARCHAR (255) NOT NULL, DatePoste DATETIME NOT NULL, FOREIGN KEY (Fk_IdUtilisateur) REFERENCES Utilisateur (IdUtilisateur));
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (1, 3, 'https://f.hellowork.com/blogdumoderateur/2017/07/giphy-logo.gif', 'Quand tu joue trop au jeu video', '2020-10-24 22:33:06.565585');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (2, 3, 'http://www.reactiongifs.com/r/dreams.gif', 'Quand tu reçois un compliment de ton patron ', '2020-10-24 22:33:38.042682');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (3, 3, 'https://media.giphy.com/media/3oKIPeYIJSEUcbKdt6/giphy.gif', 'Quand tu passe plus de temps à chercher comment pas travailler cas travailler ', '2020-10-24 22:34:30.848004');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (4, 3, 'https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif', 'Ce que ton patron pense que tu fais', '2020-10-24 22:36:14.707664');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (5, 3, 'https://media.giphy.com/media/S1ZnyFKKJ9rwc/giphy.gif', 'Quand on me demande de venir travailler les week-end', '2020-10-24 22:36:28.896501');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (6, 3, 'https://media.giphy.com/media/60yTQLK9O7XlS/giphy.gif', 'Quand ton collègue à une prime alors que c''est toi as réalisé la tâche demandée', '2020-10-24 22:40:36.893312');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (7, 3, 'https://media.giphy.com/media/hOzfvZynn9AK4/giphy.gif', '1h avant mes vacances', '2020-10-25 01:58:27.809197');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (8, 3, 'https://media.giphy.com/media/8EmeieJAGjvUI/giphy.gif', 'A mon retour de vacance', '2020-10-25 01:58:55.105298');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (9, 3, 'https://media.giphy.com/media/v6W3LmqM7ktGg/giphy.gif', 'Quand ton chef te demande un service 2min avec la fin de journée', '2020-10-25 02:00:08.924234');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (10, 3, 'https://media.giphy.com/media/d2Z4i1TGqCunWBW0/giphy.gif', 'Ce que je pense quand je remarque que le rapport que j''ai mis 3 jours à écrire n''est même pas lu', '2020-10-25 02:02:18.547440');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (11, 3, 'https://media.giphy.com/media/5tsjxsQXLl4GcNsd5S/giphy.gif', 'Quand je m''en rends compte', '2020-10-25 02:06:32.305625');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (24, 3, 'https://media.giphy.com/media/Ssiutw5cCGvrG/giphy.gif', 'Quand je suis en réunion après mangé', '2020-10-25 02:38:04.764179');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (25, 3, 'https://media.giphy.com/media/bzSWoFLMKgo00/giphy.gif', 'Quand on te convoque sans savoir pourquoi', '2020-10-25 02:40:04.415874');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (26, 3, 'https://media.giphy.com/media/3vNa5YX2zG6mQ/giphy.gif', 'Quand c''est le week-end', '2020-10-25 02:43:31.245028');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (27, 3, 'https://i.pinimg.com/564x/e6/a5/b6/e6a5b6f6bee3e838f2afabb0ca62afd2.jpg', 'Minimum 2 fois par jour ..', '2020-10-25 02:50:40.745512');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (28, 3, 'https://media.giphy.com/media/Lk023zZqHJ3Zz4rxtV/giphy.gif', 'Quand tu trouve la solution pour le patron', '2020-11-01 01:13:10.563380');
INSERT INTO Poste (IdPoste, Fk_IdUtilisateur, AdressePoste, TitrePoste, DatePoste) VALUES (30, 3, 'https://media.giphy.com/media/qDxe3pb4myxggnPe9u/giphy.gif', 'Quand on te dit que ton job aurais pu être mieux', '2020-11-01 13:26:19.182885');

-- Table : Role
CREATE TABLE Role (IdRole INTEGER PRIMARY KEY AUTOINCREMENT, NomRole VARCHAR (128) NOT NULL);
INSERT INTO Role (IdRole, NomRole) VALUES (1, 'Posteur');
INSERT INTO Role (IdRole, NomRole) VALUES (2, 'Modérateur');
INSERT INTO Role (IdRole, NomRole) VALUES (3, 'Administrateur');

-- Table : Utilisateur
CREATE TABLE Utilisateur (IdUtilisateur INTEGER PRIMARY KEY AUTOINCREMENT, PseudoUtilisateur VARCHAR (255) NOT NULL UNIQUE, MotDePasseUtilisateur VARCHAR (2056) NOT NULL, NomUtilisateur VARCHAR (255) NOT NULL, Prenom VARCHAR (255) NOT NULL, AgeUtilisateur INTEGER (2) NOT NULL, Fk_IdRole INTEGER REFERENCES Role (IdRole) DEFAULT (1));
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, AgeUtilisateur, Fk_IdRole) VALUES (1, 'Professeur', 'e10adc3949ba59abbe56e057f20f883e', 'Ayoub', 'Guillaume ', 33, 2);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, AgeUtilisateur, Fk_IdRole) VALUES (2, 'Josue', 'ab4f63f9ac65152575886860dde480a1', 'Bayidikila', 'Josue', 28, 1);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, AgeUtilisateur, Fk_IdRole) VALUES (3, 'FabriceF', '4a95de5cb88611bcac58da121c7922be', 'FERRERE', 'Fabrice', 33, 3);
INSERT INTO Utilisateur (IdUtilisateur, PseudoUtilisateur, MotDePasseUtilisateur, NomUtilisateur, Prenom, AgeUtilisateur, Fk_IdRole) VALUES (4, 'Simple', 'e10adc3949ba59abbe56e057f20f883e', 'Simple', 'Posteur', 18, 1);

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
