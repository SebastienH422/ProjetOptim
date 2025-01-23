from models import ModelesPCentre
from solution import PCentreSolution
import pyomo.environ as pe
from pyomo.core import quicksum
import numpy as np

class VersionRayon_1(ModelesPCentre): 

    def __init__(self, path_data, path_model, name_model, capacity):
        super().__init__(path_data, path_model, name_model, capacity)
        self.creer_modele()

    def creer_modele(self):
        """
        Implémente la version classique du problème.
        """
        if self.capacity:
            print(self.data.Dk, '\n\n')
            # Modèle
            modele = pe.ConcreteModel(name = f'pCP2 avec capacité')

            # Variables
            modele.x = pe.Var(range(self.data.nb_clients), range(self.data.nb_clients), name = 'x', domain=pe.Binary)
            modele.y = pe.Var(range(self.data.nb_clients), name ='y', domain=pe.Binary)
            modele.z = pe.Var(range(len(self.data.Dk)), name = 'z', domain = pe.Binary)

            # Objective function
            modele.obj = pe.Objective(expr = quicksum([(self.data.Dk[k] - self.data.Dk[k - 1]) 
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])

            # Constraintes
            modele.c1 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)
                
            modele.c2 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                for k, val_Dk in enumerate(self.data.Dk):
                    modele.c2.add(expr = 1 - modele.z[k] <= quicksum([modele.y[i] if self.data.d[i,j] < val_Dk else 0 for i in range(self.data.nb_clients)]))

            modele.c3 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_clients):
                    modele.c3.add(modele.x[i, j] <= quicksum([modele.z[k] for k in range(len(self.data.Dk)) if self.data.d[i,j] <= self.data.Dk[k]]))
                    
            modele.c4 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                modele.c4.add(quicksum(modele.x[i, j] for i in range(self.data.nb_clients)) == 1)

            Q = self.data.Q
            q = self.data.q
            
            modele.c5 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                modele.c5.add(quicksum([q[j] * modele.x[i, j] for j in range(self.data.nb_clients)]) <= Q[i] * modele.y[i])
            
        else:
            # Modèle
            modele = pe.ConcreteModel(name = f'pCP2 sans capacité {self.name_model}')

            # Variables
            modele.z = pe.Var(range(len(self.data.Dk)), name = 'z', domain = pe.Binary)
            modele.y = pe.Var(range(self.data.nb_clients), name = 'y', domain = pe.Binary)

            # Fonction objectif 

            modele.obj = pe.Objective(expr = quicksum([(self.data.Dk[k] - self.data.Dk[k-1]) 
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])         

            # Contraintes
            modele.c1 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)

            modele.c2 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                for k, val_Dk in enumerate(self.data.Dk):
                    modele.c2.add(expr = 1 - modele.z[k] <= quicksum([modele.y[i] if self.data.d[i,j] < val_Dk else 0 for i in range(self.data.nb_clients)]))
            
            
        self.modele = modele

    def extraire_solution(self, nb_points, statut, results):
        
        solution = PCentreSolution()
        
        if statut:
            solution.distance_max = results.problem.lower_bound
            for i in range(nb_points):
                entrepot_built = results.solution.variable[self.modele.y[i].getname()]['Value']
                solution.entrepots.append(int(entrepot_built))

            if self.capacity: # Si on considère les contraintes de capacités 
                for j in range(nb_points):
                    for i in range(nb_points):
                        assigned_to_i = results.solution.variable[self.modele.x[i, j].getname()]['Value']
                        if assigned_to_i:
                            solution.assignations[j] = int(i)
            else: # Si on considère pas les contraintes de capacités 
                for j in range(nb_points):
                    for i in range(nb_points):
                        if self.data.d[i,j] <= solution.distance_max and solution.entrepots[i]:
                            solution.assignations[j] = int(i)
                            break

        else: # Si ça échoue, on met '-1' partout

            for i in range(nb_points):
                solution.entrepots.append(-1)
                for j in range(nb_points):
                    solution.assignations[j] = -1
        
        return solution
