import numpy as np
import argparse
import pyomo.opt as po
import pyomo.environ as pe
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2
from solution import PCentreSolution

def verifier_solution(version, avec_capacite, chemin_instance, nb_points, nb_a_ouvrir, indice_instance, chemin_solution, chemin_modele):
    """
    Vérifie si la solution respecte les contraintes.
    """
    name_instance = f'n{nb_points}p{nb_a_ouvrir}i{indice_instance}'
    name_modele = f'{name_instance}_v{version}c{avec_capacite}.lp'
    name_solution = f'{name_instance}_v{version}c{avec_capacite}.sol'

    path_instance = chemin_instance + name_instance
    path_modele = chemin_modele + name_instance
    path_solution = chemin_solution + name_solution

    pass  # Implémentation à ajouter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int, choices=[1, 2, 3], required=True) # version du problème à résoudre
    parser.add_argument("-c", "--avecCapacite", type=int, choices=[0, 1], required=True) # 1 si les contraintes sont prises en compte
    parser.add_argument("-d", "--cheminVersInstance", type=str, required=True) # chemin relatif vers l’instance à résoudre
    parser.add_argument("-n", "--nbPoints", type=int, required=True) # nombre de sommets dans le graphe
    parser.add_argument("-p", "--nbAouvrir", type=int, required=True) # nombre d’installations à ouvrir
    parser.add_argument("-i", "--indiceInstance", type=int, required=True) # indice de l’instance
    parser.add_argument("-s", "--cheminSolution", type=str, required=True) # chemin relatif vers la solution à vérifier
    parser.add_argument("-m", "--cheminModelLp", type=str, required=True) #  chemin relatif vers le fichier .lp pour sauvegarder le modèle

    args = parser.parse_args()
    verifier_solution(args.version, args.avecCapacite, args.cheminVersInstance, args.nbPoints, args.nbAouvrir, args.indiceInstance, args.cheminSolution, args.cheminModelLp)







