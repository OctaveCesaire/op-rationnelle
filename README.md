# Recherche Opérationnelle destiné à la résolution de problème de transport
###  ![Logo Efrei](https://etudestech.com/wp-content/uploads/2022/01/logo_efrei_web_bleu-300x98.png)
*************************************************************************

### Auteur(s) & Rôle(s): 
Réalisateur(s) : 
 - ###### [Nom - prenom] : [Rôle]
 - ###### [Nom - prenom] : [Rôle]
 - ###### [Nom - prenom] : [Rôle]
 - ###### Date de réalisation : 29/04/2024
### Mise à jour potentielle:
**************************
+ - => Réorganisation du code (Functions dans un dossier globalFunction)
+ - => Dossier Main : Algorithme de Balas Hammer et Nord Ouest
+ - => Ecriture du code servant à effectuer une boucle jusqu'à épuisement de l'utilisateur
+ - => Ecriture des résultats du programme dans un fichier .txt
+ - => Etudes de la complexité du programme
+ - => Gestion du cas où le graphe n'est ni acyclique ni connexe

### Problèmatique du projet
****************************
###### Le projet de recherche opérationnelle de l'année 2023/2024 à l'Efrei Paris consiste à résoudre un problème de transport en minimisant lescoûts. Les étudiants doivent rédiger un programme informatique qui résout ce problème, en utilisant des algorithmes comme Nord-Ouest et Balas-Hammer. Le problème implique des fournisseurs ayant des provisions et des clients ayant des commandes, avec des coûts de transport entre eux. Les contraintes concernent les provisions des fournisseurs et les commandes des clients. Les étudiants doivent également étudier la complexité des algorithmes utilisés.

### Structure du projet
****************************
Dans ce projet, vous trouverez trois dossiers avec les contenus suivant:
- ###### => FunctionGlobal : functionsBalasHammer.py, functionsNordOuest.py, generalFunction.py
- ###### => Mains          : mainBalasHammer.py     , mainNordOuest.py
- ###### => Tracées        : ensemble des résultats sortant de l'exécution du programme
- ###### => Fichiers Test  : Ensemble des fichiers tests (.txt) pour l'exécution du programme
- ###### => Package Python : - numpy => pour les matrices
  ######                     - sympy => résolutions de systèmes équations pour le calcul des potentielle


### Fonctionalités
****************************
###### Nom et rôle des codes utiles selon leurs importances
###### Positions => Rôles
 - [0] => Lecture du cahier de charge sans prise en compte de la complexité.

 - [1] => Ecriture du code de lecture de fichier: readingFile( @param : fichierà lire )
    ###### return:tuple=>(data,order)| data:toutes les lignes sauf la dernier ligne,order:dernière ligne.

 - [2] => Ecriture du code pour la construction du problème de transport initial: graphInit( @param )

    ###### @param  : les données prises du fichier.

    ###### @retour : Ajout de 0 en fin de order pour faire la jonction entre data et order.

 - [3] => Ecriture de la fonction permettant d'afficher toutes matrices : printMatrice(@param)

    ###### @param  : [message : "string | texte à afficher", matrice : "numpy | matrice à afficher"].

 - [4] => Ecriture du sous programme permettant de trouver la nature du graphe (dégénéré ou non)

    ###### Nom prog: graphNature(@param).

    ###### @param  : [ext :"numpy | résultat de la proposition",init|"numpy"].

    ###### @retour : s * c * a * graphe | source*commande*nombre d'arrête*chemin composant la solution.

    ###### @info   : init est le graphe initiale pour NordOuest sinon la matrice des coûts initial.Source et commande sont les listes des sources et commandes composant graphe.Le retour est un tuple (graphe,[Boolean,a,s,c]) où Boolean est True si nombre de source et commande formant le graphe - 1 vaut a.
        
 - [5] => Ecriture du code permettant d'illustrer les chemin composant le graphe : TraceGraph(@param)
        
    ###### @param : [graph :"Graphe à afficher",message : "String| Pour indiquer le niveau du graphe"]
    
 - [6] => Ecriture du code permettant de vérifier la présence d'un cycle dans le graphe après avoir converti le graphe obtenu sous
        forme de dictionnaire grâce à la fonction adjacency_list(graph)
          
    ###### @param : graph | celui obtenu précédemment avec graphNature(@param) puis on appelle la fonction detectionCycle(dictionnaire,nombre de source,nombre de commande) avec dictionnaire la sortie de adjacency_list(graph).

    ###### @retour : [cycle : "Array | numpy de tuple (Commande,Source)"]

 - [7] => En cas de préence de cycle /circuit appliqué la méthode de marche pieds au cycle / circuit.
        
    ###### @But : Calcul de  δ grâce à marchePied(@param)

    ###### @param : [graphPhy : "numpy|chemin reliant source,commande",ext:"proposition de solution",n :"nombre de ligne", m :"nombre de colonne"]

    ###### @retour : "La nouvelle proposition de solutions"
    
 - [8] => Ecriture du code calcul des potentiels utilisant la fonction CalculPotentiel().
        
    ###### @param : graph, s,a, c représaant respectivement la matrice des données , la liste des sources,nombre d'arrêtes et la liste des commandes

    ###### @retour : liste des solutions qui servira à l'obtention de la matrice des coûts marginaux grâce à la fonction costMargi()
    
 - [9] => Ecriture de la fonction costMargi(res,solutionPotenti) permettant de construire la matrice des coûts marginaux.
          La matrice obtenu renvoie des floats converti en int avec à {{astype(int)}}

    ###### @param :  res * solutionPotenti = la solution de propositon obtenu * solution du système d'équation des potentielles
        
    ###### @retour : martice de cout marginaux
    
 - [10] => L'écriture de la fonction costInit() permet d'extrait de côté la matrice de coût intialement donnée

    ###### @param : data :: donnée fournie depuis le fiche test (.txt)
**********************************
### La fonction principale du projet : controle_globale(@param)


* #### La fonction controle_globale() est celle qui assure la mise à jour de la proposition initialement considéré comme optimale en vérifiant  que les valeurs de la matrice des coûts marginaux sont tous positives.
  #### @param : (coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti)
    - => coutMarginaux : Matrice des coût marginaux;
    - => sortie        : Solution obtenue;
    - => graph         : Graphe tracé;
    - => nbreCommande  : colonnes de toutes nos matrices issues des fichiers test (.txt);
    - => nbreSource    : lignes de toutes nos matrices issues des fichier test (.txt);
    - => graphinitial  : Graphe initiales la proposition que l'on estime optimale;
    - => nbrArret      : Nombre d'arrêtes formant notre graphe / ciruit de transport et non cycle;
    - => cout_inti     : Extrait de matrice constituée des cout de chaque transport.
  #### @ return : (coutMarginaux,sortie,graph,nbreCommande,nbreSource,graphinitial,nbrArret,cout_inti)
    - => coutMarginaux : Matrice des coût marginaux;
    - => sortie        : Solution obtenue;
    - => graph         : Graphe tracé;
    - => nbreCommande  : colonnes de toutes nos matrices issues des fichiers test (.txt);
    - => nbreSource    : lignes de toutes nos matrices issues des fichier test (.txt);
    - => graphinitial  : Graphe initiales la proposition que l'on estime optimale;
    - => nbrArret      : Nombre d'arrêtes formant notre graphe / ciruit de transport et non cycle;
    - => cout_inti     : Extrait de matrice constituée des cout de chaque transport.

### Mecanisme du projet
*************************
* #### Première réalisation
   ![Extraction des données](image-1.png)
* #### Secondaire réalisation
   ![Algorithme Nord-Ouest & Balas-Hammer](image-4.png)
* #### Troisème réalisation
   ![alt text](image-6.png)
### Outils & Usages 
****************************
- [X] GPT : Pour la recherche de certaine module afin de facilité les calcules dont la résolution du système d'équation 
- [X] Youtube : Pour la compréhension de certaines méthodes de calculs
- [X] Personne Ressource : Pour de la clarté
- [X] Cahier + Stylo : Pour la vérification du programme et structuration du projet à la papas

### Difficultés 
****************************
  #### listes des difficultés
   - Manipulations des matrices
   - Détection de cycle, calcul de pénalité
   - Extraite des sous graphe pour certaines études
   - Résolution du système d'équation pour le calcul des potentielle
   - Ecriture dans un fichier test (.txt)
   - Récupération du cycle et calcul de δ

### Modules à installer
***********************
### numpy, sympy
        pip install numpy
        pip install sympy 
