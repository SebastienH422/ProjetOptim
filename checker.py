import numpy as np
import argparse
import pyomo.opt as po
import pyomo.environ as pe
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2
from solution import PCentreSolution
from data import PCentreData

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int, choices=[1, 2, 3], required=True) # version du problème à résoudre
    parser.add_argument("-c", "--avecCapacite", type=int, choices=[0, 1], required=True) # 1 si les contraintes sont prises en compte
    parser.add_argument("-d", "--cheminVersInstance", type=str, required=True) # chemin relatif vers l’instance à résoudre
    parser.add_argument("-n", "--nbPoints", type=int, required=True) # nombre de sommets dans le graphe
    parser.add_argument("-p", "--nbAouvrir", type=int, required=True) # nombre d’installations à ouvrir
    parser.add_argument("-i", "--indiceInstance", type=int, required=True) # indice de l’instance
    parser.add_argument("-s", "--cheminVersSolution", type=str, required=True) # chemin relatif vers la solution à vérifier
    parser.add_argument("-m", "--cheminModelLp", type=str, required=True) #  chemin relatif vers le fichier .lp pour sauvegarder le modèle

    args = parser.parse_args()
    

name_instance = f'n{args.nbPoints}p{args.nbAouvrir}i{args.indiceInstance}'
name_modele = f'{name_instance}_v{args.version}c{args.avecCapacite}.lp'
name_solution = f'{name_instance}_v{args.version}c{args.avecCapacite}.sol'

path_instance = args.cheminVersInstance + '/' +  name_instance
path_modele = args.cheminModelLp + '/' +  name_instance
path_solution = args.cheminVersSolution + '/' + name_solution

def read_sol(path_solution):
    """ 
    Read solution file and extract datas into structures
    """

    with open(path_solution, "r") as f: 
        entrepot, liaisons, dist_max = f.read().split('\n')
        entrepot, liaisons, dist_max = entrepot.split(), liaisons.split(), dist_max.strip()

        # Conversions en int 
        entrepot = [int(i) for i in entrepot]
        liaisons = [int(i) for i in liaisons]
        dist_max = float(dist_max)
    
    return entrepot, liaisons, dist_max


def verif(entrepot, liaisons, dist_max, structs):
    """ 
    Make sure that the found solution respect every constraints and is valid
    """
   
    # Vérification que si une installation est assignée à un client est bien ouverte 
    # Vérification aussi que tout client a bien quelque chose assigné
    for liaison in liaisons:
            if liaison >= len(entrepot) or liaison < 0:
                raise TypeError("Non valid solution: All client must have associated installation") 
            if entrepot[liaison] == 0: # Pour chaque entrepot présent dans liaisons, vérifier qu'il est bien ouvert
                raise TypeError("Non valid solution: Client can't be associated to a closed installation")
        
    # Vérification des contraintes de capacités et demandes : 
    entrepots_ouverts = {num_entrepot : 0
                         for num_entrepot, val_entrepot in enumerate(entrepot)
                         if val_entrepot}
    for i, liaison in enumerate(liaisons):
        entrepots_ouverts[liaison] += structs.q[i] # ajt la quantité dmd par client 
    
    for key in entrepots_ouverts: 
        if entrepots_ouverts[key] > structs.Q[key]:
            raise TypeError("Non valid solutions: All capacities constraint must be satisfied")
    
    # Vérification que toutes les distances <= Dmax
    for i, j in enumerate(liaisons):
        if structs.d[i][j] > dist_max:
            raise TypeError("Non valid solution: The maximum distance dist_max is not satisfied")
    print("gucci")



entrepot, liaisons, dist_max = read_sol(path_solution)

structs = PCentreData(path_instance)

verif(entrepot, liaisons, dist_max, structs)

