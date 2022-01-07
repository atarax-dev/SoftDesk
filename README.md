# SoftDesk
#  Projet OC n°10


Introduction: Il s'agit d'une application permettant de remonter et suivre des problèmes techniques (issue tracking system)

La documentation Postman (https://www.postman.com/downloads/) incluse dans ce dossier permet de comprendre les différents points de 
terminaisons et leur utilisation.
Importez le fichier export_postman_softdesk.json afin d'avoir accès à la documentation
Précisions concernant les choix disponibles dans certains champs de certains modèles:
-type de project: back-end, front-end, iOS ou Android
-priorité (priority) de issue: FAIBLE, MOYENNE ou ÉLEVÉE
-balise(tag) de issue: BUG, AMÉLIORATION ou TÂCHE
-statut (status) de issue: À faire, En cours ou Terminé

Lancez un terminal

Récupérez l'ensemble du projet :

`git clone https://github.com/atarax-dev/SoftDesk`

Placez-vous dans le répertoire qui contient le fichier manage.py

Pour pouvoir lancer le programme, créez un environnement virtuel:

`python -m venv venv`

Activez l'environnement :

`source venv/Scripts/activate` (sous windows)

`source venv/bin/activate` (sous Mac ou linux)

Installez les packages requis à l'aide de la commande suivante:

`pip install -r requirements.txt` 

# Utilisation 

Toujours depuis le répertoire qui contient manage.py dans le terminal, exécutez le programme:

`python manage.py migrate` puis `python manage.py runserver`

Puis ouvrez votre navigateur et allez sur la page suivante : http://127.0.0.1:8000/signup/ pour vous créer un compte
Si vous effectuez vos requêtes via Postman, vous devrez remplir l'Auth à l'aide du token JWT accessible 
à l'adresse suivante http://127.0.0.1:8000/login/ 