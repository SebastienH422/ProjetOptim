from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum
from data import PCentreData

class VersionClassique(ModelesPCentre): 

    def __init__(self, data: PCentreData):
        super().__init__(data)

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacity):
        """
        Implémente la version classique du problème.
        """
        self.capacity = capacity

        # Modèle
        modele = pe.ConcreteModel(name = f'pCP1 Version classique')

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
        
        modele.c3 = pe.Constraint(expr = quicksum([modele.y[i] for i in range(self.data.nb_clients)]) <= self.data.p)

        if capacity:
            #modele.Q = pe.Param(range(self.data.nb_points), name = 'Q', initialize = self.data.capacites, domain = pe.NonNegativeReals)
            #modele.q = pe.Param(range(self.data.nb_clients), name = 'q', initialize = self.data.demandes, domain = pe.NonNegativeReals)
            Q = self.data.Q
            q = self.data.q
            
            modele.c4 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                modele.c4.add(quicksum(q[j] * modele.x[i, j] for j in range(self.data.nb_clients)) <= Q[i] * modele.y[i])
        else:
            modele.c4 = pe.ConstraintList()
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_clients):
                    modele.c4.add(modele.x[i,j] <= modele.y[i])

        self.modele = modele
        

    def extraire_solution(self):        
        if self.status:
            self.solution.distance_max = self.obj
            for i in range(self.data.nb_clients):
                entrepot_built = pe.value(self.modele.y[i]) # self.results.solution.variable[self.modele.y[i].getname()]['Value']
                self.solution.entrepots.append(int(entrepot_built))

            # if self.capacity: # Si on considère les contraintes de capacités 
            for i in range(self.data.nb_clients):
                for j in range(self.data.nb_clients):
                    assigned_to_i = pe.value(self.modele.x[i,j]) # self.results.solution.variable[self.modele.x[i, j].getname()]['Value']
                    if assigned_to_i:
                        self.solution.assignations[j] = int(i)
            # else: # Si on considère pas les contraintes de capacités 
            #     for i in range(self.data.nb_clients):
            #         for j in range(self.data.nb_clients):
            #             if self.data.d[i,j] <= self.solution.distance_max and self.solution.entrepots[i]:
            #                 self.solution.assignations[j] = int(i)
            #                 break

        else: # Si ça échoue, on met '-1' partout
            for i in range(self.data.nb_clients):
                self.solution.entrepots.append(-1)
                for j in range(self.data.nb_clients):
                    self.solution.assignations[j] = -1
