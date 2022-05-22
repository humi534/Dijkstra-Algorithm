# -*- coding: utf-8 -*-
   
def read_file(adjacency_matrix):
    """ Extrait la matrice d'adjacence de départ et renvoie une liste de listes avec les éléments
    
    Parameters
    ----------
    adjacency_matrix: le fichier (.txt) avec la matrice d'adjacence de départ (file)
    
    Returns
    -------
    grid: la liste de listes avec les éléments de la matrice d'adjacence(list of list of int) """
    
    opened_file = open(adjacency_matrix,'r')  #ouvre le fichier avec la matrice
    lines = opened_file.readlines() 
    grid = list()
    
    try:
        lines[0] = lines[0].replace('ï»¿','')  #sert à effacer les 3 signes bizarres de la première ligne
    except:
        None
    
    for i in range(len(lines)):
        grid.append([int(s) for s in lines[i].split() if s.isdigit()])  # transforme le fichier texte en une liste de liste contenant les éléments   
        
    opened_file.close() #fermeture du fichier
    return grid
    
    
def get_nb_nodes(grid):
    """ Retourne le nombre de sommets présents dans la matrice
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    
    Returns
    -------
    nb_nodes: le nombre de sommets présents dans la matrice (int) """
    
    nb_nodes = 0
    for i in grid:
        nb_nodes += 1   #incrémente de 1 par élément dans grid
    
    return nb_nodes  #renvoie le nombre de sommets présent dans le graphe
    

def get_adjacency_matrix():
    """ Renvoie le lien vers le fichier contenant la matrice test
    
    Returns
    -------
    adjacency_matrix:  le fichier (.txt) avec la matrice d'adjacence de départ (file) """
    
    
    link_default_file = 'C:/Users/hugop/OneDrive/Documents/théorie des graphes/matrice_test.txt'  #lien par défaut
    
    user_input = str(input("indiquez le lien complet du fichier pour la matrice d'adjacence (exemple: C:/Users/hugop/OneDrive/Documents/théorie des graphes/matrice_test.txt)"))
    if user_input == "":  # si l'utilisateur n'encode pas de lien vers le fichier, prends le lien par défaut
        adjacency_matrix = link_default_file
    else: 
        adjacency_matrix = user_input
    
    return adjacency_matrix
        

def get_start_node(grid):
    """ Renvoie le choix de l'utilisateur pour le sommet de départ
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    
    Returns
    -------
    start_node: le sommet de départ depuis lequel on recherche le chemin le plus court vers les autres sommets (int) """
    
    while True:
        try:
            start_node = int(input("indiquez votre point de départ avec un numéro (commence à 0) "))  #si l'utilisateur encode un chiffre, c'est bon. Sinon on passe dans le except
            
        except ValueError:  #si l'utilisateur n'a pas encodé un chiffre, on relance la demande
            print("Vous devez écrire un nombre entier positif")
            continue
        
        if start_node not in range(get_nb_nodes(grid)):  #si l'utilisateur n'a pas encodé un chiffre correct, on relance la demande
            print("Ce nombre doit être inclu dans le nombre de sommets")
            continue
                
        else:  #si tout est bon, on passe à la suite
            break
    
    return start_node  #renvoie le sommet de départ
    
    
def dijkstra_algorithm(grid, start_node):
    """ Renvoie la distance la plus courte entre 2 sommets ainsi que la liste parent contenant pour chaque index le sommet précédent dans le chemin optimal 
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    start_node: le sommet de départ depuis lequel on recherche le chemin le plus court vers les autres sommets (int)
    
    Returns
    -------
    dist: la liste contenant la distance minimale entre le sommet de départ et chaque sommet (list)
    parent: liste contenant pour chaque index le sommet précedent dans chemin le plus court depuis le sommet de départ (list) """
    
    dist = list()  # représentera la distance minimale entre le sommet de départ et le sommet correspondant à l'index. Ex: dist[1] = 9 et le sommet de départ est 0 signifie que la distance entre 0 et 1 est de 9
    unvisited = list() # représentera la liste des sommets par lesquels l'algorithme n'est pas encore passé
    parent = list() #représente la liste qui pour chaque index, indique le sommet précedent dans l'algorithme pour le chemin le plus court depuis le sommet de départ
    
    
    for i in range(get_nb_nodes(grid)):  
        dist.append(float('inf'))   #initialisation: mettre une distance de infini entre le sommet de départ et l'ensemble des autres sommets
        unvisited.append(i)         #initialisation: tous les sommets sont au départ non visités
        parent.append(start_node)  
        
    dist[start_node] = 0            #initialisation: mettre la distance entre le sommet de départ et lui-même à 0
    
    node = start_node  #node représente le sommet de départ
    
    while unvisited != []:  # tant que unvisited n'est pas une liste vide
        
        node = get_smallest_dist(unvisited, dist)
        unvisited.remove(node)
        
        for neighbour in get_neighbours(grid, node):
            if dist[node] + grid[node][neighbour] < dist[neighbour]:
                dist[neighbour] = dist[node] + grid[node][neighbour]
                parent[neighbour] = node
                
    return dist, parent
    
    
def create_path(grid, parent, start_node):
    """ Renvoie un dictionnaire path contenant pour chaque sommet une liste correspondant aux sommet à parcourir pour aller du sommet de départ au sommet spécifié dans la clé
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    parent: liste contenant pour chaque index le sommet précedent dans chemin le plus court depuis le sommet de départ (list)
    start_node: le sommet de départ depuis lequel on recherche le chemin le plus court vers les autres sommets (int)
    
    Returns
    -------
    path: dictionnaire de liste correspondant au chemin de sommets entre le sommet de départ et la sommet spécifié dans la clé (dict) """
    
    path = dict() 
    for i in range(get_nb_nodes(grid)): #initialisation: path est un dictionnaire contenant pour chaque sommet une liste du chemin pour arriver à ce point. 
        path[i] = []                    # exemple au départ pour 5 sommets, path = {0: [], 1: [], 2: [], 3: [], 4: []}
        if i != start_node:
            path[i].append(i)  # on ajoute le point final dans le chemin
        
    for i in range(get_nb_nodes(grid)):
        a = parent[i]
        while a != start_node:
            path[i].append(a)  #ajout progressif des sommet dans l'ordre inverse du chemin
            a = parent[a] #on passe au sommet précédent
    
        path[i].append(start_node)  #ajout du point de départ
        path[i].reverse()   #inversion du chemin pour le mettre dans le bon ordre
        
    return path
    

def get_neighbours(grid, node):
    """Renvoie une liste contenant les sommets voisins à celui recherché (node) 
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    node: le sommet depuis lequel on recherche ses sommets voisins (int)
    
    Returns
    -------
    neighbours: la liste contenant les sommets voisins au sommet 'node' (list)   """
    
    neighbours = []
    for i in grid[node]:
        if i != 0:
            neighbours.append(grid[node].index(i))  #ajout du voisin dans la liste
            
    return neighbours
    
    
def get_smallest_dist(unvisited, dist):
    """Renvoie à partir d'un sommet le sommet le plus proche
    
    Parameters
    ----------
    unvisited: la liste des sommets par lequel l'algorithme n'est pas encore passé (list of int)
    dist: la liste contenant la distance minimale entre le sommet de départ et chaque sommet correspondant aux index de la liste (list)

    Returns
    -------
    index: un sommet qui n'a pas encore été visité et dont la distance est jusqu'à présent la plus petite dans la liste dist (int) """
    
    lowest_cost = float('inf')       # distance minimale est l'infini
    for i in unvisited:             # pour chaque sommet n'aillant pas encore été visité dans l'algorithme
        if dist[i] <= lowest_cost:   # si la distance entre le sommet non visitié et le sommet de départ est plus petite ou égale à l'infini
            lowest_cost = dist[i]    # la distance la plus petite devient la distance entre le sommet non visité et le sommet de départ
            index = i  
            
    return index


def final_message(grid, dist, start_node, path):
     
    """Print les messages avec les distances entre le sommet de départ et les autres sommets ainsi que le chemin pour y arriver
    
    Parameters
    ----------
    grid: la liste de liste de la matrice d'adjacence (list of list of int)
    dist: la liste contenant la distance minimale entre le sommet de départ et chaque sommet correspondant aux index de la liste (list)   
    start_node: le sommet de départ depuis lequel on recherche le chemin le plus court vers les autres sommets (int) 
    path: dictionnaire de liste correspondant au chemin de sommets entre le sommet de départ et la sommet spécifié dans la clé (dict) """
    
    for i in range(get_nb_nodes(grid)):
        print("la distance minimale pour aller du sommet {} au sommet {} est de {} avec comme chemin".format(start_node, i, dist[i]), path[i])
    
    
def run():
    """ Fonction principale comportant l'ensemble des fonctions """
    
    adjacency_matrix = get_adjacency_matrix()
    grid = read_file(adjacency_matrix)
    start_node = get_start_node(grid)
    dist, parent = dijkstra_algorithm(grid, start_node)
    path = create_path(grid, parent, start_node)
    final_message(grid, dist, start_node, path)    
    
    
run()  #appel de la fonction principale
    
    















