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
            # Modèle
            modele = pe.ConcreteModel(name = f'pCP2 avec capacité')

            # Variables
            modele.x = pe.Var(range(self.data.nb_clients), range(self.data.nb_clients), name = 'x', domain=pe.Binary)
            modele.y = pe.Var(range(self.data.nb_clients), name ='y', domain=pe.Binary)
            modele.z = pe.Var(range(len(self.data.Dk)), name = 'z', domain = pe.Binary)

            # Objective function
            modele.obj = pe.Objective(expr = quicksum([(self.data.Dk[k] - self.data.Dk[k-1]) 
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])

            # Constraintes
            modele.c1 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)
                
            modele.c2 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_clients):
                    modele.c2.add(modele.x[i, j] * self.data.d[i, j] <= quicksum([(self.data.Dk[k] - self.data.Dk[k-1])
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])
                    
            modele.c3 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                modele.c3.add(quicksum(modele.x[i, j] for i in range(self.data.nb_clients)) == 1)

            Q = self.data.Q
            q = self.data.q
            
            modele.c4 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                modele.c4.add(quicksum([q[j] * modele.x[i, j] for j in range(self.data.nb_clients)]) <= Q[i] * modele.y[i])
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

    def extraire_solution(self, results):
        solution = PCentreSolution()
        if self.statut:
            if self.capacity:
                solution.variables['x'] = np.zeros((self.data.nb_clients, self.data.nb_clients), dtype = int)
                solution.variables['y'] = np.zeros(self.data.nb_clients, dtype = int)
                solution.variables['z'] = np.zeros(len(self.data.Dk), dtype = int)

                for i in range(self.data.nb_clients):
                    entrepot_built = results.solution.variable[self.modele.y[i].getname()]['Value']
                    solution.entrepots.append(int(entrepot_built))
                    solution.variables['y'][i] = entrepot_built

                    for j in range(self.data.nb_clients):
                        assigned_to_i = results.solution.variable[self.modele.x[i, j].getname()]['Value']
                        if assigned_to_i: solution.assignations[j] = i
                        solution.variables['x'][i,j] = assigned_to_i

                for k in range(1, len(self.data.Dk)):
                    solution.variables['z'][k] = results.solution.variable[self.modele.z[k].getname()]['Value']
                    if solution.variables['z'][k]: solution.distance_max = self.data.Dk[k]
                if solution.distance_max == -1: solution.distance_max = self.data.Dk[0]

            else:
                solution.variables['y'] = np.zeros(self.data.nb_clients, dtype = int)
                solution.variables['z'] = np.zeros(len(self.data.Dk), dtype = int)
                x = np.zeros((self.data.nb_clients, self.data.nb_clients), dtype = int)

                for k in range(len(self.data.Dk)):
                    solution.variables['z'][k] = results.solution.variable[self.modele.z[k].getname()]['Value']
                    if solution.variables['z'][k]: solution.distance_max = self.data.Dk[k]
                
                for i in range(self.data.nb_clients):
                    entrepot_built = results.solution.variable[self.modele.y[i].getname()]['Value']
                    solution.entrepots.append(int(entrepot_built))
                    solution.variables['y'][i] = results.solution.variable[self.modele.y[i].getname()]['Value']
                    for j in range(self.data.nb_clients):
                        if not x[i,j] and self.data.d[i,j] <= solution.distance_max:
                            x[i,j] = 1
                            solution.assignations[j] = i

                
        else:
            for i in range(self.data.nb_clients):
                solution.entrepots.append(-1)
                for j in range(self.data.nb_clients):
                    solution.assignations[j] = -1
        
        return solution
