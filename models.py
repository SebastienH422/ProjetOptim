import pyomo.environ as pe
from data import PCentreData

class ModelesPCentre:
    
    def __init__(self, path_instance, path_model, name_model, capacity):
        """
        Initialise le modèle avec les données.
        """
        self.data = PCentreData(path_instance)
        self.path_model = path_model
        self.name_model = name_model
        self.capacity = capacity

        self.solution = None
        self.modele = None
        self.statut = False

    def creer_modele(self, capacite):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError

    def extraire_solution(self, results):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError

    def ecrire_modele(self):
        """
        Sauvegarde le modèle dans un fichier LP.
        """
        self.modele.write(self.path_model)

    def lancer(self, temps_limite):
        """
        Résout le modèle avec un solveur.
        """
        solver = pe.SolverFactory("highs")  
        solver.options["time_limit"] = temps_limite  # Appliquer la limite de temps
        
        resultat = solver.solve(self.modele, tee=True)

        if (resultat.solver.status == pe.SolverStatus.ok) and \
           (resultat.solver.termination_condition == pe.TerminationCondition.optimal):
            print("Solution optimale trouvée.")
            self.extraire_solution()
        else:
            print(f"Problème lors de la résolution : {resultat.solver.termination_condition}")
