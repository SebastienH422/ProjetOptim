from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum

class VersionClassique(ModelesPCentre): 

    def __init__(self, path_data, path_model, name_model):
        super.__init__(path_data, path_model, name_model)

    def creer_modele(self, capacite):
        """
        Implémente la version classique du problème.
        """
        # Modèle
        modele = pe.ConcreteModel(name = f'pCP1 Version classique {self.name_model}')

        # Fonction objectif
        modele.obj = pe.Objective(expr = modele.D)

        # Variables
        modele.x = pe.Var(range(self.data.nb_client), range(self.data.nb_client), name = 'x', domain = pe.Binary)
        modele.y = pe.Var(range(self.data.nb_client), name = 'y', domain = pe.Binary)
        modele.D = pe.Var(name = 'D', domain = pe.NonNegativeReals)

        # Contraintes
        modele.c1 = pe.ConstraintList()
        for i in range(self.data.nb_client):
            for j in range(self.data.nb_client):
                modele.c1.add(self.data.d[i,j] * modele.x[i,j] <= modele.D)
        
        modele.c2 = pe.ConstraintList()
        for j in range(self.data.nb_client):
            modele.c2.add(quicksum([modele.x[i,j] for j in range(self.data.nb_client)]) == 1)
        
        modele.c3 = pe.ConstraintList()
        for i in range(self.data.nb_client):
            for j in range(self.data.nb_client):
                modele.c3.add(modele.x[i,j] <= modele.y[i])
        
        modele.c4 = pe.Constraint(quicksum([modele.y[i] for i in range(self.data.nb_client)]) <= modele.data.p)

        self.modele = modele

    def extraire_solution(self):
        """
        Extrait la solution du modèle résolu.
        """
        pass  # Extraction des valeurs optimales
