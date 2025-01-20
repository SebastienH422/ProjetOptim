import pyomo.environ as pyo

class ModelesPCentre:
    def __init__(self, data):
        """
        Initialise le modèle avec les données.
        """
        self.data = data
        self.solution = None
        self.modele = None

    def creer_modele(self, capacite):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError

    def extraire_solution(self):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError

    def ecrire_modele(self, fichier_lp):
        """
        Sauvegarde le modèle dans un fichier LP.
        """
        self.modele.write(fichier_lp)

    def lancer(self, temps_limite):
        """
        Résout le modèle avec un solveur.
        """
        solver = pyo.SolverFactory("highs")  
        solver.options["time_limit"] = temps_limite  # Appliquer la limite de temps
        
        resultat = solver.solve(self.modele, tee=True)

        if (resultat.solver.status == pyo.SolverStatus.ok) and \
           (resultat.solver.termination_condition == pyo.TerminationCondition.optimal):
            print("Solution optimale trouvée.")
            self.extraire_solution()
        else:
            print(f"Problème lors de la résolution : {resultat.solver.termination_condition}")
