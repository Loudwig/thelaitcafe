# THE'LAIT'CAFE

Description du projet : 
- Appli web utilisable sur mobile permettant aux étudiants de Télécom Paris d'acheter des capsules de café à prix coutant.(PARTIE 1)
- Lydia compatible (PARTIE 1)
- Une fois la capsule acheter un machine automatisé distribuera la capsule à l'étudiant (PARTIE 2)
- Le distributeur comportera une Rpi(récupère toutes les infos) et une arduino (commande les moteurs etc) (PARTIE 2)


État actuel du projet : 
 - La web app fonctionne en local. Un utilisateur peut créer un compte , acheter une capsule avec lydia où sa carte banquaire.(PARTIE 1)
 - L'app fonctionne pour l'instant avec l'environnement de test de Lydia, pour simuler une transaction utiliser la carte : 4970109000000007  CCV : 123 et date de péremenption dans le futur. (PARTIE 1)
 - Un script permet de détecter lorsque qu'un paiment à été fait (detectpayment.py)
 - La partie mécanique avec arduino du distributeur fonctionne(PARTIE 2)

Point à rajouter : 
  - Design la page d'acceuil.
  - J'aimerais que la connexion puisse se faire avec les identifiants Rezel des etudiants. Utilisation de OPEN ID CONNECT.
  - Problème de cyber-sécurité à fixer (voir Problème de cyber-sécurité ) 
  - Mettre en production le site web sur une machine virtuelle.
  - Rajouter un système qui permet aux étudiants d'avoir des capsules gratuites après un certain nombre d'achats.
  - Lié la partie arduino et le script detectpayment
  - Lors de la création d'un compte afficher ce qui ne va pas lorsque le mdp n'est pas bon
    
    

Problème de cyber-sécurité : 
  - Lorsque l'on fait une requête sur une transaction à lydia pour savoir son état actuel (si elle a été payé, en cours, canceller etcc), lydia signe ce qu'elle renvoie.
Cependant je n'arrive pas encore à vérifier la signature. Cela pose donc un problème de sécurité. En effet je penses que si quelqu'un arrive à écouter les requêtes que ma machine virtuelle fait, il pourra simuler un transaction payé.


POUR TESTER LE PROJET EN LOCAL:

Créer un environnement virtuel
Installer les dépendances du fichier requirements_dev.txt

VARIABLES D'ENVIRONNEMENT à CRÉER ET SOURCER : 
SECRET_KEY = "sakdfha;sdfjha;sldnf;askdfjalskjdf;aksjdf" # a long private string
PRODUCTION = 'false' # 

1 - Lancer l'app django : python manage.py runserver (src/)
2 - Aller sur la boutique de l'app
3 - Se mettre en mode téléphone
3 - Créer un utilisateur ou bien utiliser : utilisateur : usertest | password : testtest1234
4 - Tester les paiments etc
