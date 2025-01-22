import argparse
import pyomo.opt as po
import pyomo.environ as pe
from pCP1 import VersionClassique
from pCP2 import VersionRayon_1
from pCP3 import VersionRayon_2
from solution import PCentreSolution


def choisir_version(version, path_data, path_model, name_instance, capacity):
    if version == 1:
        return VersionClassique(path_data, path_model, name_instance, capacity)
    elif version == 2:
        return VersionRayon_1(path_data, path_model, name_instance, capacity)
    elif version == 3:
        return VersionRayon_2(path_data, path_model, name_instance, capacity)
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

    name_instance = f'n{args.nbPoints}p{args.nbAouvrir}i{args.indiceInstance}'
    name_modele = f'{name_instance}_v{args.version}c{args.avecCapacite}.lp'
    name_solution = f'{name_instance}_v{args.version}c{args.avecCapacite}.sol'

    path_instance = f'{args.cheminVersInstance}/{name_instance}'
    path_modele = f'{args.cheminModelLp}/{name_modele}'
    path_solution = f'{args.cheminSolution}/{name_solution}'
    
    modele_inst = choisir_version(args.version, path_instance, path_modele, name_instance, args.avecCapacite)
    
    solver = po.SolverFactory('appsi_highs')
    solver.options['time_limit'] = args.tempsLimite

    results = solver.solve(modele_inst.modele, tee = False, load_solutions = False)

    name_solution = ''
    
    solution = PCentreSolution()
    if results.solver.status != po.SolverStatus.ok:
        for i in range(args.nbPoints):
            solution.entrepots.append(-1)
            for j in range(args.nbPoints):
                solution.assignations[j] = -1
    else:
        solution.distance_max = results.problem.lower_bound
        for i in range(args.nbPoints):
            entrepot_built = results.solution.variable[modele_inst.modele.y[i].getname()]['Value']
            solution.entrepots.append(1 if entrepot_built else 0)
            for j in range(args.nbPoints):
                assigned_to_i = results.solution.variable[modele_inst.modele.x[i, j].getname()]['Value']
                if assigned_to_i: solution.assignations[j] = i
        
    solution.ecrire_solution(path_solution = path_solution)    
