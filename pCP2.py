from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

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
            modele.x = pe.Var(range(self.data.nb_points), range(self.data.nb_clients), name = 'x', domain=pe.Binary)
            modele.y = pe.Var(range(self.data.nb_points), name ='y', domain=pe.Binary)
            modele.z = pe.Var(range(len(self.data.Dk)), name ='z', domain=pe.Binary)

            # Objective function
            modele.obj = pe.Objective(expr = quicksum([(self.data.Dk[k] - self.data.Dk[k-1]) 
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])

            # Constraintes
            modele.c1 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_points)]) <= self.data.p)

            modele.c2 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                modele.c2.add(quicksum(modele.x[i, j] for i in range(self.data.nb_points)) == 1)
                
            modele.c3 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_points):
                    modele.c3.add(modele.x[i, j] * self.data.d[i, j] <= quicksum([(self.data.Dk[k] - self.data.Dk[k-1])
                                                    * modele.z[k] for k in range(1, len(self.data.Dk))]) + self.data.Dk[0])

            Q = self.data.capacites[i]
            q = self.data.demandes[j]
            
            modele.c4 = pe.ConstraintList()
            for i in range(self.data.nb_points):
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
            modele.c1 = pe.ConstraintList()
            for j in range(self.data.nb_clients):
                for k, val_Dk in enumerate(self.data.Dk):
                    modele.c1.add(1 - modele.z[k] <= quicksum([modele.y[i] if self.data.d[i,j] < val_Dk 
                                                            else 0 for i in range(self.data.nb_clients)]))
            
            modele.c2 = pe.Constraint(quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)
            

        self.modele = modele

    def extraire_solution(self):
        """
        Extrait la solution du modèle résolu.
        """
        pass  # Extraction des valeurs optimales
