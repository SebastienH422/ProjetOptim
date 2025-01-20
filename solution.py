class PCentreSolution:
    def __init__(self):
        """
        Initialise la solution du problème.
        """
        self.entrepots = []  # Liste des entrepôts ouverts
        self.assignations = {}  # Dictionnaire client -> entrepôt
        self.distance_max = None

    def ecrire_solution(self, fichier_sortie: str):
        """
        Écrit la solution dans un fichier.
        """
        with open(fichier_sortie, "w") as f:
            # Format d'écriture selon Appendix A
            # TODO
            pass  # Implémentation à ajouter
