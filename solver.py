import argparse
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2

def choisir_version(version, data):
    if version == 1:
        return VersionClassique(data)
    elif version == 2:
        return VersionRayon_1(data)
    elif version == 3:
        return VersionRayon_2(data)
    else:
        raise ValueError("Version invalide")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", type=int, choices=[1, 2, 3], required=True) # version du problème à résoudre
    parser.add_argument("-c", "--avecCapacite", type=int, choices=[0, 1], required=True) # 1 si les contraintes de capacité sont prises en compte
    parser.add_argument("-d", "--cheminVersInstance", type=str, required=True) # chemin relatif vers l’instance à résoudre
    parser.add_argument("-t", "--tempsLimite", type=int, required=True) # temps limite d’exécution du solveur
    parser.add_argument("-n", "--nbPoints", type=int, required=True) # nombre de sommets dans le graphe
    parser.add_argument("-p", "--nbAouvrir", type=int, required=True) # nombre d’installations à ouvrir
    parser.add_argument("-i", "--indiceInstance", type=int, required=True) # indice de l’instance
    parser.add_argument("-s", "--cheminSolution", type=str, required=True) # chemin relatif vers le fichier dans lequel la solution sera écrite
    parser.add_argument("-m", "--cheminModelLp", type=str, required=True) #  chemin relatif vers le fichier .lp pour sauvegarder le modèle

    args = parser.parse_args()

    data = PCentreData(args.cheminVersInstance)
    modele = choisir_version(args.version, data)
    modele.creer_modele(capacite=args.avecCapacite)
    modele.lancer(args.tempsLimite)
    modele.ecrire_modele(args.cheminModelLp)
    modele.solution.ecrire_solution(args.cheminSolution)
