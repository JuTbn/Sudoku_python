##### 0 - Contenu du fichier parser #######################################################################################################
def read(filename):
    file = open(filename)

    dim = int(file.readline())
    grid = []

    for i in range(dim**2):
        line = file.readline().split('\n')[0].split(' ')
        for j in range(dim**2):
            if int(line[j]) != 0:
                grid.append((i, j, int(line[j])))

    file.close()

    return dim, grid


    
##### 2 - Représentation en mémoire d'une grille de sudoku ################################################################################

#   Question 1:
    #Entrée: L'ordre de la grille.
    #Sortie : Une grille vide d'ordre demandé en entrée.

def ordre_grille(ordre):
    grille = []
    
    for i in range(ordre**2):
        grille.append([])
        
        for j in range(ordre**2):
            grille[i].append(0)
            
    return grille

#   Question 2:
    #Entrée: Le nom d'un fichier texte contenant l'instance de sudoku.
    #Sortie : Une grille contenant la grille décrite dans le fichier.
def grille_base(nomFichier):
    ordre, valeurs = read(nomFichier)
    grille = ordre_grille(ordre)
    
    for i in range(len(valeurs)):
        ligne = valeurs[i][0]
        colonne = valeurs[i][1]
        grille[ligne] [colonne]  = valeurs[i][2]

    return grille


        
##### 3 - Représentation graphique d'une grille de sudoku  ######################################################################
import render
import math


    #Sortie : Affichage graphique d'une grille donnée en entrée.
def affiche_grille(grille):

    ordre = int(math.sqrt(len(grille[1])))

    render.draw_sudoku_grid(ordre)
    
    for ligne in range(ordre**2):
        for colonne in range(ordre**2):
            # Détermine les cases vides:
            if grille[ligne][colonne] == 0:
                render.write(ligne,colonne,"?","green")
            # Détermine les nombres fixés:
            else:
                render.write(ligne, colonne, grille[ligne][colonne], "red")
    
    #render.wait_quit()


##### 4 - jouer au sudoku  ######################################################################################################

    #Intention: Demande un entier, si c'est un entier supérieur a 20 ou si ce n'est pas un entier alors il recommence.
    #Sortie: un entier au format int
def demanderEntier(ordre, texte):
    resultat = "vide"
    liste = []
    for u in range(20):
        liste += [str(u),]
    while resultat not in liste:
        resultat = input("---> Entrez un numéro de " + texte + " ou appuyez sur entrée pour annuler le coup : ")
        if resultat == "":
            return -1
        
        if resultat not in liste:
            print("ERREUR! IL vous est demandé un entier compris entre 0 et ", ordre*ordre-1)
    
    return int(resultat)

    #Sortie : Le nombre de case vide d'une grille donnée en entrée.
def cptCaseVide(grille):
    cpt = 0

    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille[i][j] == 0:
                cpt += 1
    return cpt

    #Sortie : Liste contenant les coordonnées des cases non modifiables.
def caseNonModifiable(grille):
    liste = []
    cpt = 0
    for i in range(len(grille)):
        for j in range(len(grille)):
            if grille[i][j] != 0:
                liste += ((i, j),)
    
    return liste
    
    
    #Entrées : Liste contenant les coordonnées des cases non modifiables + liste contenant les coordonnées de la case qu'essai de modifier le joueur.
    #Sortie : True si la case qu'essai de modifier le joueur est une case non modifiable. Sinon False.
def estDans(casesFixes, essai):
    for k in range(len(casesFixes)):
        if casesFixes[k] == essai:
            return True
    return False

    
    #Intention: Vérifie si la ligne, la colonne et le carré de la case [ligne][colonne] contient valeur.
    #Sortie : False si la valeur est déjà présente sur la ligne, la colonne ou le bloc de cette case. Sinon True.
def valeurPossible(nOrdre, nGrille, nLigne, nColonne, nValeur):
    for m in range(nOrdre*nOrdre):
        if nGrille[nLigne][m] == nValeur:
            return False
        
        elif nGrille[m][nColonne] == nValeur:
            return False
        
    nLigne = (nLigne // nOrdre) * nOrdre
    nColonne = (nColonne // nOrdre) * nOrdre
    for n in range(nOrdre):
        for p in range(nOrdre):
            if nGrille[nLigne+n][nColonne+p] == nValeur:
                return False
    return True





##### 5 - Mis en place d'un historique  ######################################################################

    #Sortie : Affiche le contenu du liste
def lectureListe(liste):
    for i in range(len(liste)):
        print(liste[i], " ", end = '')

    #Intention: Demande au joueur s'il souhaite annuler son coup ou nom.
    #Sortie: "O" ou "N"
def demanderAnnulation():
    resultat = ""
    while resultat != "O" and resultat !="N":
        resultat = input("Voulez-vous l'annuler ? [O]ui / [N]on : ")
        if resultat != "O" and resultat != "N":
            print("ERREUR! Oui => O / Non => N")
    return resultat




def jouer(fichier):
    
    grille = grille_base(fichier)
    ordre = int(math.sqrt(len(grille)))
    affiche_grille(grille)
    
    historique = []
    
    caseFixe = caseNonModifiable(grille)
    
    caseVide = cptCaseVide(grille)
    

    while caseVide != 0:
        
        annuler = "N"
        if historique != []:
            print("Dernier coup joué : (", historique[ len(historique)-1 ] [ 0 ], ",", historique[ len(historique)-1 ] [ 1 ], ") ", historique[ len(historique)-1 ] [ 2 ],"--> ", historique[ len(historique)-1 ] [ 3 ] )
            annuler = demanderAnnulation()
            ligne = historique[ len(historique)-1 ] [0]
            colonne = historique[ len(historique)-1 ] [1]
            ancienneValeur = historique[len(historique)-1 ] [2]
            valeur = historique[ len(historique)-1 ] [3]
            
            
            if annuler == "O":
                if ancienneValeur == 0:
                    render.write(ligne,colonne,"?","green")
                    grille[ligne][colonne] = 0
                    caseVide = cptCaseVide(grille)
                    
                else:
                    render.write(ligne,colonne,ancienneValeur,"blue")
                    grille[ligne][colonne] = ancienneValeur
                    caseVide = cptCaseVide(grille)
                    
                historique.pop(len(historique)-1)
                
        if annuler == "N":
            print("Il reste ", caseVide, " cases à remplir")        
            #print("---> Entrez un numéro de ligne ou entrée pour annuler : ")
            ligne = demanderEntier(ordre, "ligne")
            
            if ligne == -1:
                print("Vous avez choisit d'annuler ce coup!")
                print()
            elif ligne < 0 or ligne >= ordre*ordre:
                print("ERREUR, ce numéro de ligne est incorrect, il doit être entre 0 et ",ordre*ordre-1)
                print()
                
            else:
                colonne = demanderEntier(ordre, "colonne")
                if colonne == -1:
                    print("Vous avez choisit d'annuler ce coup!")
                    print()
                elif colonne < 0 or colonne >= ordre*ordre :
                    print("ERREUR, ce numéro de colonne est incorrect, il doit être entre 0 et ",ordre*ordre-1)
                    print()
                elif estDans(caseFixe, (ligne, colonne)):
                    print("ERREUR, cette case est non modifiable ")
                    print()
                    
                else:
                    print("Les valeurs possibles sont : ", end = '',)
                    listeValeurPossible = [0,]
                    print(0, " ", end='')
                    for i in range(1, ordre*ordre+1):
                        if valeurPossible(ordre, grille, ligne, colonne, i):
                            listeValeurPossible += [i]
                            print(i, " ", end='')
                    print()
                    
                    valeur = demanderEntier(ordre, "valeur")
                    if valeur == -1:
                        print("Vous avez choisit d'annuler ce coup!")
                        print()
                    elif valeur < 0 or valeur > ordre*ordre:
                        print("ERREUR, ce numéro de valeur est incorrect, il doit être entre 0 et ",ordre*ordre )
                        print()
                        
                    elif not estDans(listeValeurPossible, valeur):
                        print("ERREUR, ce numéro de valeur est incorrect, il doit faire partie de la liste des valeurs possibles." )
                        print()
                        
                    elif valeur == 0:
                        ancienneValeur = grille[ligne][colonne]
                        grille[ligne][colonne] = valeur
                        render.write(ligne,colonne,"?","green")
                        caseVide = cptCaseVide(grille)
                        
                        historique += [ [ligne, colonne, ancienneValeur, valeur], ]
                    
                    else:
                        ancienneValeur = grille[ligne][colonne]
                        grille[ligne][colonne] = valeur
                        render.write(ligne,colonne,valeur,"blue")
                        caseVide = cptCaseVide(grille)
                        
                        historique += [ [ligne, colonne, ancienneValeur, valeur], ]
                    
    print()
    print("Félicitation, vous avez réussi à compléter le sudoku!")
    render.wait_quit()
    
    
##### 6 - Résolution automatique  ######################################################################

    #Sortie : Liste de liste contenant les coordonnées des cases modifiables
def listFreeCells(grid):
    liste = []

    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] == 0:
                liste += ((i, j),)
    return liste

    #Sortie : False si avec la valeur tester le sudoku ne peut être finit
def solve_recursive(grid, freecells):
    
    order = int(math.sqrt(len(grid)))
    countFreecells = len(freecells)
    
    while countFreecells != 0:
        
        for line in range(order*order):
            for column in range(order*order):
                
                if grid[line][column] == 0:
                    possibleValue = []
                    
                    for i in range(1, order*order+1):
                        if valeurPossible(order, grid, line, column, i):
                            possibleValue += [i]

                    
                    for j in range(len(possibleValue)):
                        
                        value = possibleValue[j]
                        
                        grid[line][column] = value
                        render.write(line,column,value,"blue")
                        
                        
                        solve_recursive(grid, freecells)
                        
                        grid[line][column] = 0
                        render.write(line,column,"?","green")
                    
                    if grid[line][column] == 0:
                        return False

    return True
    
    

    #Intention : Demande à l'utilisateur quel fichier utilisé avec quel mode de jeu.
def sudoku():
    grid = input("Entrez le nom du fichier (entrée pour prendre le fichier par défaut): ")
    
    if grid == "":
        grid = 'sudoku_9_9_1.txt'
    
    choice = ""
    
    while choice != "J" or choice != "R":
    
        choice = input('Voulez-vous [J]ouer ou [R]ésoudre ? ')
    
        if choice == "J":
            print(jouer(grid))
        
        elif choice == "R":
            grid = grille_base(grid)
            affiche_grille(grid)
            
            freecells = listFreeCells(grid)
            solve_recursive(grid, freecells)
            
    render.wait_quit()
            
    

sudoku()
    
                            
                
                
        
            



    
    
    


