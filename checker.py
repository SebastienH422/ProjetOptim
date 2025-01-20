import argparse

def verifier_solution(avec_capacite, chemin_vers_instance, nb_points, nb_a_ouvrir, indice_instance, chemin_solution):
    """
    Vérifie si la solution respecte les contraintes.
    """
    pass  # Implémentation à ajouter

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--avecCapacite", type=int, choices=[0, 1], required=True) # 1 si les contraintes sont prises en compte
    parser.add_argument("-d", "--cheminVersInstance", type=str, required=True) # chemin relatif vers l’instance à résoudre
    parser.add_argument("-n", "--nbPoints", type=int, required=True) # nombre de sommets dans le graphe
    parser.add_argument("-p", "--nbAouvrir", type=int, required=True) # nombre d’installations à ouvrir
    parser.add_argument("-i", "--indiceInstance", type=int, required=True) # indice de l’instance
    parser.add_argument("-s", "--cheminSolution", type=str, required=True) # chemin relatif vers la solution à vérifier

    args = parser.parse_args()
    verifier_solution(args.avecCapacite, args.cheminVersInstance, args.nbPoints, args.nbAouvrir, args.indiceInstance, args.cheminSolution)
