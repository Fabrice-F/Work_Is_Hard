# Bienvenue sur le projet Work is Hard
Bonjour et bienvenue !  
Le projet **Work Is Hard** a été réalisé dans le cadre du module Python lors l'année [C-Dev à l'IPI](https://www.ipi-ecoles.com/concepteur-developpeurfull-stack/) de lyon 2020-2021. 

Il a été mis en place par les étudiants **Josue Bayidikilla** et **Fabrice FERRERE**.  

La technologie utilisé est [**python**](https://www.python.org/) avec son framework [**Flask**](https://flask.palletsprojects.com/en/1.1.x/).

Nous avons tenté de respecter au maximum les règles communes au langage python et avons appliqué au maximum les règles De [**PEP8**](https://www.python.org/dev/peps/pep-0008/)

# Sommaire:

 **1. C'est quoi Work is Hard ?  
 2. Comment mettre en place le projet.  
  3. Ce qui a été réalisé.
  4. Ce que l'on aurait aimé faire   
  6. Divers informations**  

## C'est quoi Work is Hard ?

**Work Is Hard** est un site à caractère humoristique. 

Il a pour but de réunir les travailleurs de tout métier autour de ***poste*** contenant un ***titre*** plus ou moins comique avec ***une image ou un gif*** reflétant leur quotidien dans leurs métiers. 

L'ensemble reflète généralement une réalité légère de manière comique.

Pour pouvoir partager un poste utilisateur doit obligatoirement être inscrit.

##  Comment mettre en place le projet.

Il est important de signalé que nous n'avons mis en place le système d'initialisation de la bdd proposé comme sur le site de Flask.

**En effet, nous avons réussis à mettre l'initialisation de la base de donnée par le projet Flask qu'une journée avant la date butoir. 
Inquiet  de ne pouvoir vérifié l'intégralité du fonctionnement du site avec ce système d'initialisation et de pouvoir effectué une panoplie complète de test afin d'assurer le bon fonctionnement du site, nous avons choisit de ne pas poursuivre le système proposé par Flask.**

Nous avons pris alors la décision de maintenir notre système d'initialisation manuelle de la base de donnée.

Pour pouvoir mettre en place le projet :

 1. Télécharger le repository du projet.

## Ce qui a été réalisé ?

Actuellement sur le site nous avons mis en place :

 - L'inscription simple d'un utilisateur *(avec les sécurités d'usage)*.
 
 - La connexion d'un utilisateur.
 - La création et la publication de poste avec un système d'aperçu.
 - Une page d'accueil avec les postes.
 - La pagination de la page d'accueil.
 - Une page où des postes aléatoires apparaissent.
 -  La pagination de la page aléatoire.
 - Une page de gestion de compte avec possibilités de changer de mots de passe et de pseudo.
 - Le partage des postes avec redirection vers le site *(actif mais pointe vers  '127.0.0.1:5000' donc non pertinent)*
 - La partie modération (rôle nécessaire) avec : 
	 - La modification d'un titre de poste directement depuis la page l'accueil ou aléatoire.
	 - La suppression d'un poste directement depuis la page l'accueil ou aléatoire.
	 - Le bannissement d'un utilisateur ( de rôle inférieur) directement depuis la page l'accueil ou aléatoire.
	 - La page de modération où les **postes en attentes de modération** peuvent :  être acceptés , être refusés, avoir un changement de titre, avoir l'utilisateur bannis .
- La partie administration ( rôle nécessaire) avec :
	- L'attribution et le changement des rôles.
	- La possibilité d'activé où de désactivé le mode modération ( ce qui fait que les postes sont en attente de modération ou vont directement sur le site).
	- La possibilité d'écrire un message d'information.
- Les sécurités et l'expérience utilisateurs essentielles au bon fonctionnement du site (informations champs vides, demande mot quand changement important).
- Sécurité d'accès aux pages quand l'utilisateur n'as pas le rôle ou n'est pas connecté.

## Ce que l'on aurait aimé faire ?

> Malheureusement, par manque de temps, nous n'avons pas pu réalisé
> l'ensemble des taches que nous aurions voulu mettre en place à la
> remise du projet pour le module. 
> 
> *Fabrice et Josué*

Voici la liste *(non exhaustive)*  des fonctionnalités que nous aurions aimé mettre en place:

 - Implémenter les e-mail au projet afin d'envoyé de demande de  confirmation d'inscription et de réinitialisation de mot de passe   oublié (actuellement géré par contact aux admins) .  
 
  - Augmenter la sécurisation coté serveur notamment au niveau changement mot de passe.
  - Augmenter l'expérience utilisateur lors du changement de pseudo.
  - Augmenter la sécurité  en bannissant les i.p lors de tentative de connexion infructueuse et répété.
  - Ajouter l'impossibilité de multiple clique sur un bouton pendant un laps de temps une fois cliquer dessus.
  - Faire le système initialisation de la base de donnée.

## Divers informations

 1. Actuellement nous n'avons  **pas pu mettre en place le système d'initialisation de la base de donnée.** 
En effet, nous sommes partie sur la création du site en lançant l'application via les commande **flask_app=WorkIsHard.py**  et nous avons développé le site en nous servant de cette méthode.
 La base de donnée étant partagé a travers le repo pendant tout le développement *(pratique fortement déconseillé et ne sera plus refait à l'avenir)*.
 
 2. Nous souhaitons dans la mesure du possible continué à mettre en place le site en développant les fonctionnalités manquantes et primordial à une mise en production. Pour par la suite le mettre sur internet.
 
