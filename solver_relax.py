import argparse
from data import PCentreData
from pCP1_relax import VersionClassique
from pCP2_relax import VersionRayon_1
from pCP3_relax import VersionRayon_2
import time


def main():
    parser = argparse.ArgumentParser(description='Solver script')
    parser.add_argument('-v', '--version', required=True, type=int, choices=[1, 2, 3], help='Version of the solver')
    parser.add_argument('-c', '--avecCapacite', required=True, type=int, choices=[0, 1], help='Capacity constraint')
    parser.add_argument('-d', '--cheminVersInstance', required=True, help='Path to the instance')
    parser.add_argument('-t', '--tempsLimte', required=True, help='Limit time of the solver')
    parser.add_argument('-n', '--nbPoints', required=True, type=int, help='Number of nodes')
    parser.add_argument('-p', '--nbAouvrir', required=True, type=int, help='Number of facility to open')
    parser.add_argument('-i', '--indiceInstance', required=True, type=int, help='Index of the instance')
    parser.add_argument('-s', '--dossierSolution', required=True, help='Solution folder')
    parser.add_argument('-r', '--fichierResultat', required=True, help='Result file')

    args = parser.parse_args()

    print("************************** Infos for the Solver **************************")
    print(f"Version: {args.version}")
    print(f"With Capacity: {args.avecCapacite}")
    print(f"Path to Instance: {args.cheminVersInstance}")
    print(f"Time Limit: {args.tempsLimte}")
    print(f"Number of Nodes: {args.nbPoints}")
    print(f"Number to Open: {args.nbAouvrir}")
    print(f"Index of Instance: {args.indiceInstance}")
    print(f"Solution Folder: {args.dossierSolution}")
    print(f"Results file: {args.fichierResultat}")
    print("**************************************************************************")

    #___________________________Paths to files
    name_instance = f'n{args.nbPoints}p{args.nbAouvrir}i{args.indiceInstance}'
    name_solution = f'{name_instance}_v{args.version}c{args.avecCapacite}.sol'

    path_instance = f'{args.cheminVersInstance}/{name_instance}'
    path_solution = f'{args.dossierSolution}/{name_solution}'

    #___________________________Activation of the capacity constraint
    capacity = False
    if args.avecCapacite >= 1:
        capacity = True

    #__________________________ Load the data
    data = PCentreData()
    data.lireData(path_instance)
    #__________________________ Create the model
    if args.version == 1:
        model = VersionClassique(data)
    elif args.version == 2:
        model = VersionRayon_1(data)
    else:
        model = VersionRayon_2(data)

    start_time = time.time()
    model.creer_modele(capacity)
    end_time = time.time()
    model.temps_creation = round(end_time - start_time, 5)

    #__________________________ Solve the model
    model.lancer(args.tempsLimte)

    #__________________________ Save the solution
    model.extraire_solution()
    model.solution.ecrire_solution(path_solution)

    #__________________________ write results in dataBase file
    with open(args.fichierResultat, 'a') as f:
        f.write(f'{args.nbPoints} {args.nbAouvrir} {args.indiceInstance} {args.version} {args.avecCapacite} {model.erreur} {model.status} {model.etat} {model.temps_creation} {model.temps} {model.gap} {model.obj} {model.obj_upper} {model.obj_lower}\n')

if __name__ == "__main__":
    main()
