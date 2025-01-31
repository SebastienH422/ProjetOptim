from models import ModelesPCentre
import pyomo.environ as pe
from pyomo.core import quicksum
from data import PCentreData

class VersionRayon_2(ModelesPCentre): 

    def __init__(self, data: PCentreData):
        super().__init__(data)

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacity):
        """
        Implémente la version classique du problème.
        """
        self.capacity = capacity

        # Modèle
        modele = pe.ConcreteModel(name = f'pCP3')

        # Variables
        modele.y = pe.Var(range(self.data.nb_clients), name = 'y', domain = pe.NonNegativeReals, bound = (0, 1))
        modele.u = pe.Var(range(len(self.data.Dk)), name = 'u', domain = pe.NonNegativeReals, bound = (0, 1))

        # Fonction objectif 
        modele.obj = pe.Objective(expr = quicksum([self.data.Dk[k] * modele.u[k] for k in range(len(self.data.Dk))]))
                            
        # Contraintes
        modele.c1 = pe.Constraint(expr = quicksum(modele.y[i] for i in range(self.data.nb_clients)) <= self.data.p)

        if capacity:  
            # Variable supplémentaire
            modele.x = pe.Var(range(self.data.nb_clients), range(self.data.nb_clients), name = 'x', domain=pe.NonNegativeReals, bound = (0, 1))

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
                for k in range(len(self.data.Dk)):
                    modele.c2.add(modele.u[k] <= quicksum([modele.y[i] for i in range(self.data.nb_clients) if self.data.d[i,j] <= self.data.Dk[k]]))
                    
            modele.c3 = pe.Constraint(expr = quicksum([modele.u[k] for k in range(len(self.data.Dk))]) == 1)

        self.modele = modele
    
    
    def extraire_solution(self):        
        if self.status:
            self.solution.distance_max = self.obj
            for i in range(self.data.nb_clients):
                entrepot_built = pe.value(self.modele.y[i]) # self.results.solution.variable[self.modele.y[i].getname()]['Value']
                self.solution.entrepots.append(int(entrepot_built))

            if self.capacity: # Si on considère les contraintes de capacités 
                for j in range(self.data.nb_clients):
                    for i in range(self.data.nb_clients):
                        assigned_to_i = pe.value(self.modele.x[i,j]) # self.results.solution.variable[self.modele.x[i, j].getname()]['Value']
                        if assigned_to_i:
                            self.solution.assignations[j] = int(i)
            else: # Si on considère pas les contraintes de capacités 
                for j in range(self.data.nb_clients):
                    for i in range(self.data.nb_clients):
                        if self.data.d[i,j] <= self.solution.distance_max and self.solution.entrepots[i]:
                            self.solution.assignations[j] = int(i)
                            break

        else: # Si ça échoue, on met '-1' partout
            for i in range(self.data.nb_clients):
                self.solution.entrepots.append(-1)
                for j in range(self.data.nb_clients):
                    self.solution.assignations[j] = -1            
        
