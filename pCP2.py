from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre): 

    def __init__(self, path_data, path_model, name_model):
        super().__init__(path_data, path_model, name_model)

    def creer_modele(self, capacite):
        """
        Implémente la version classique du problème.
        """
        # Modèle
        modele = pe.ConcreteModel(name = f'pCP2 Version classique {self.name_model}')

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
                modele.c1.add(1-modele.z[k] <= quicksum([modele.y[i] if self.data.d[i,j] < val_Dk 
                                                         else 0 for i in range(self.data.nb_clients)]))
        
        modele.c2 = pe.ConstraintList()
        modele.c2.add(quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)

        self.modele = modele

    def extraire_solution(self):
        """
        Extrait la solution du modèle résolu.
        """
        pass  # Extraction des valeurs optimales
