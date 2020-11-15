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

> En effet, nous avons réussis à mettre l'initialisation de la base de
> donnée par le projet Flask qu'une journée avant la date butoir. 
> Inquiet  de ne pouvoir vérifié l'intégralité du fonctionnement du site
> avec ce système d'initialisation et de pouvoir effectué une panoplie
> complète de test afin d'assurer le bon fonctionnement du site, nous
> avons choisit de ne pas poursuivre le système proposé par Flask.

Nous avons pris alors la décision de maintenir notre système d'initialisation manuelle de la base de donnée.

**Pour pouvoir mettre en place le projet :**

 - Télécharger le repository du projet.
 
 - Décompresser le dossier Work_Is_Hard.zip
 
 - *Sous Windows :* 

	 - Pour pouvoir mettre en place le projet, vous allez devoir installer  
   "**venv**". Ce dernier est un environnement virtuel qui permettra d’exécuter   votre serveur.
   
	 - Pour cela installer [python](https://www.python.org/downloads/) et   activer la variable d'environnement path.
	 
	 - Une fois python installé,  lancer un invite de commande et rendez-vous dans votre dossier **Work_Is_Hard** *(où se situe le fichier workishard .py, classe. py, static .. )* et tapez :
				
				python -m venv venv
				ou
				python3 -m venv venv

	   

	 - Une fois la commande terminé votre arborescence devrait ressemble a celle-ci  (dossier venv en +):
	 
			| static
			| templates
			| venv
			| BddFonctions. py
			| Classes. py
			| ConstanteAndTools. py
			| flask run development.cmd
			| Flask run host production.cmd
			| WorkIsHard. py
			| WorkIsHard.sql
	
	 - Une fois **venv** installé, vous devez maintenant vous connecter à **venv** pour cela dans l'invite de commande faite :
		 
			venv\Scripts\activate
	
	- Pour confimer que vous correctement connecté à venv vous devriez voir ***(venv)*** devant votre chemin  dans votre invite de commande, comme sur cette exemple :
	
			(venv) C:\Chemin\vers\votre\dossier\Work_Is_Hard>
	
	 - Toujours dans le même invité de commande, vous pouvez maintenant lancez cette commande pour installer le module **Flask** :
	 
			 pip install flask


> **Une fois tout cela fait,  vous voila prêt à lancer le serveur **

 - *Sous les autres OS :*
   	 - rendez vous [ici](https://flask.palletsprojects.com/en/1.1.x/installation/)
   	

**Pour pouvoir mettre en place la bdd:**

 - Dans le dossier Work_Is_Hard vous devriez avoir cette arborescence obtenir cette arboresence :

		| static
	    | templates
	    | venv
	    | BddFonctions. py
	    | Classes. py
	    | ConstanteAndTools. py
	    | flask run development.cmd
	    | Flask run host production.cmd
	    | WorkIsHard. py
	    | WorkIsHard.sql

 - Télécharger [**sqlite3.exe**](https://www.sqlite.org/download.html)  :

	 - si vous êtes sur Windows, vous pouvez récupérer le fichier 
	   ressemblant a ceci : *sqlite-tools-win32-x86-xxxxxxx.zip*

 - Une fois téléchargé , lancer sqlite3.exe.
 
 - Tapez ensuite la commande ***(sans la valider)*** dans l'invite de commande sqlite3 : `.read` 
 
 - **Glisser** ensuite le fichier **WorkIsHard.sql**.
 
 - Si des double quotes comme ceci: `"`  entour **le chemin** de votre fichier **WorkIsHard.sql** , remplacez par des simples  quotes comme ceci : `'`
		 
	 - exemple:


 
			✕ Chemin obtenu quand vous glisser le fichier WorkIsHard.sql:
				sqlite> .read "C:\chemin vers\votre\fichier\WorkIsHard.sql"

			✓ Chemin que vous devez avoir pour que le script fonctionne:
				sqlite> .read 'C:\chemin vers\votre\fichier\WorkIsHard.sql'

 - Une fois que votre chemin est correct valider avec la touche **entrer**.
 
 - Si une aucune erreur est signalé, une nouvelle ligne de ce type devrait apparaître :

		
		sqlite>
	


	> 	C'est que votre base à été correctement généré.


 - Dans le dossier contenant **sqlite3.exe** , un fichier nommé **WorkIsHard.db** a dû être généré. 
 
 - Glisser ce fichier **WorkIsHard.db** dans votre dossier **Work_Is_Hard** 
 
 - Après ceci vous devriez obtenir cette arborescence :

	 	| static
		| templates
		| venv
		| BddFonctions. py
		| Classes. py
		| ConstanteAndTools. py
		| flask run development.cmd
		| Flask run host production.cmd
		| WorkIsHard. py
		| WorkIsHard.sql	
		| WorkIsHard.db

 - Vous pouvez maintenant lancez ces 4 commandes les unes à la suite des autres :

		venv\Scripts\activate
		set flask_app=WorkIsHard.py
		set flask_env=development
		python -m flask run 

 - Un message comme ci dessous devrait apparaître :

		* Serving Flask app "WorkIsHard.py" (lazy loading)
		* Environment: development
		* Debug mode: on
		* Restarting with stat
		* Debugger is active!
		* Debugger PIN: 338-628-774
		* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

 - Cela signifie que le serveur est correctement allumé et que vous n'avez plus qu'as vous rendre sur l'adresse :http://127.0.0.1:5000/

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
 

