from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum
from data import PCentreData

class VersionRayon_1(ModelesPCentre): 

    def __init__(self, data: PCentreData):
        super().__init__(data)

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacity):
        """
        Implémente la version classique du problème.
        """
        self.capacity = capacity

        if capacity:
            # Modèle
            modele = pe.ConcreteModel(name = f'pCP2 avec capacité')

            # Variables
            modele.x = pe.Var(range(self.data.nb_clients), range(self.data.nb_clients), name = 'x', domain=pe.NonNegativeReals, bounds = (0, 1))
            modele.y = pe.Var(range(self.data.nb_clients), name ='y', domain=pe.NonNegativeReals, bounds = (0, 1))
            modele.z = pe.Var(range(len(self.data.Dk)), name = 'z', domain = pe.NonNegativeReals, bounds = (0, 1))

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
                    for k in range(len(self.data.Dk)):
                        if self.data.d[i,j] >= self.data.Dk[k]:
                            modele.c3.add(modele.x[i,j] <= modele.z[k])


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
            modele = pe.ConcreteModel(name = f'pCP2 sans capacité')

            # Variables
            modele.z = pe.Var(range(len(self.data.Dk)), name = 'z', domain = pe.NonNegativeReals, bound = (0, 1))
            modele.y = pe.Var(range(self.data.nb_clients), name = 'y', domain = pe.NonNegativeReals, bound = (0, 1))

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

    def extraire_solution(self):        
        if self.status:
            self.solution.distance_max = self.obj
            for i in range(self.data.nb_clients):
                entrepot_built = pe.value(self.modele.y[i])
                self.solution.entrepots.append(int(entrepot_built))

            if self.capacity: # Si on considère les contraintes de capacités 
                for i in range(self.data.nb_clients):
                    for j in range(self.data.nb_clients):
                        assigned_to_i = pe.value(self.modele.x[i, j])
                        if assigned_to_i:
                            self.solution.assignations[j] = int(i)
            else: # Si on considère pas les contraintes de capacités 
                for j in range(self.data.nb_clients):
                    for i in range(self.data.nb_clients):
                        print(f'{i}, {j}: {self.data.d[i,j]} <= {self.solution.distance_max} and {self.solution.entrepots[i]}')
                        if self.data.d[i,j] <= self.solution.distance_max and self.solution.entrepots[i]:
                            self.solution.assignations[j] = int(i)
                            break

        else: # Si ça échoue, on met '-1' partout
            for i in range(self.data.nb_clients):
                self.solution.entrepots.append(-1)
                for j in range(self.data.nb_clients):
                    self.solution.assignations[j] = -1
