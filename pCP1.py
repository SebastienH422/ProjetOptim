from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre): 

    def __init__(self, path_data, path_model, name_model):
        super().__init__(path_data, path_model, name_model)
        self.creer_modele(0)
        self.capacite = capcite

    def creer_modele(self):
        """
        Implémente la version classique du problème.
        """
        # Modèle
        modele = pe.ConcreteModel(name = f'pCP1 Version classique {self.name_model}')

        # Variables
        modele.x = pe.Var(range(self.data.nb_clients), range(self.data.nb_clients), name = 'x', domain = pe.Binary)
        modele.y = pe.Var(range(self.data.nb_clients), name = 'y', domain = pe.Binary)
        modele.D = pe.Var(name = 'D', domain = pe.NonNegativeReals)

        # Fonction objectif
        modele.obj = pe.Objective(expr = modele.D, sense = pe.minimize)

        # Contraintes
        modele.c1 = pe.ConstraintList()
        for i in range(self.data.nb_clients):
            for j in range(self.data.nb_clients):
                modele.c1.add(self.data.d[i,j] * modele.x[i,j] <= modele.D)
        
        modele.c2 = pe.ConstraintList()
        for j in range(self.data.nb_clients):
            modele.c2.add(quicksum([modele.x[i,j] for i in range(self.data.nb_clients)]) == 1)
        
        modele.c3 = pe.ConstraintList()
        for i in range(self.data.nb_clients):
            for j in range(self.data.nb_clients):
                modele.c3.add(modele.x[i,j] <= modele.y[i])
        
        modele.c4 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)

        if self.capacite == 1:
            #modele.Q = pe.Param(range(self.data.nb_points), name = 'Q', initialize = self.data.capacites, domain = pe.NonNegativeReals)
            #modele.q = pe.Param(range(self.data.nb_clients), name = 'q', initialize = self.data.demandes, domain = pe.NonNegativeReals)
            Q = {i: self.data.capacites[i] for i in range(self.data.nb_points)}
            q = {j: self.data.demandes[j] for j in range(self.data.nb_clients)}
            
            modele.c5 = pe.ConstraintList()
            for i in range(self.data.nb_points):
                modele.c5.add(sum(q[j] * modele.x[i, j] for j in range(self.data.nb_clients)) <= Q[i] * modele.y[i])

        self.modele = modele

    def extraire_solution(self):
        """
        Extrait la solution du modèle résolu.
        """
        pass  # Extraction des valeurs optimales
