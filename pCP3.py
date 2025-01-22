from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionRayon_2(ModelesPCentre): 

    def __init__(self, path_data, path_model, name_model, capacity):
        super().__init__(path_data, path_model, name_model, capacity)
        self.creer_modele()

    def creer_modele(self):
        """
        Implémente la version classique du problème.
        """
        # Modèle
        modele = pe.ConcreteModel(name = f'pCP3 {self.name_model}')

        # Variables
        modele.y = pe.Var(range(self.data.nb_clients), name = 'y', domain = pe.Binary)
        modele.u = pe.Var(range(len(self.data.Dk)), name = 'u', domain = pe.Binary)

        # Fonction objectif 
        modele.obj = pe.Objective(expr = quicksum([self.data.Dk * modele.u[k] for k in range(len(self.data.Dk))]))
                            
        # Contraintes
        modele.c1 = pe.Constraint(quicksum(modele.y[i] for i in range(self.data.nb_clients)) <= self.data.p)

        if self.capacity:  
            # Variable supplémentaire
            modele.x = pe.Var(range(self.data.nb_points), range(self.data.nb_clients), name='x', domain=pe.Binary)

            # Contraintes supplémentaires
            modele.c2 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_clients):
                    modele.c2.add(modele.x[i,j]* self.data.d[i,j] <= quicksum(self.data.Dk[k] * modele.u[k] for k in range(len(self.data.Dk))))

            modele.c3 = pe.ConstraintList()
            for j in range(self.data.nb_clients): 
                modele.c3.add(quicksum(modele.x[i,j] for i in range(self.data.nb_clients)) == 1)

            modele.c4 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                modele.c4.add(quicksum(self.data.q[j] * modele.x[i,j] for j in range(self.data.nb_clients)) <= self.data.Q[i] * modele.y[i])
        
        else :

            modele.c2 = pe.ConstraintList()
            for j in range(self.data.nb_clients): 
                for k in range(self.data.Dk):
                    modele.c2.add(modele.u[k] <= quicksum([modele.y[i] for i in range(self.data.nb_clients) if self.data.d[i,j] <= self.data.Dk[k]]))
                    
            modele.c3 = pe.Constraint(quicksum([modele.u[k] for k in range(self.data.Dk)]) == 1)

        self.modele = modele

    def extraire_solution(self):
        """
        Extrait la solution du modèle résolu.
        """
        pass  # Extraction des valeurs optimales

