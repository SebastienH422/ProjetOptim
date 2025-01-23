class PCentreSolution:
    def __init__(self):
        """
        Initialise la solution du problème.
        """
        self.entrepots = []  # Liste des entrepôts ouverts
        self.assignations = {}  # Dictionnaire client -> entrepôt
        self.variables = {}
        self.distance_max = -1
 
    def ecrire_solution(self, path_solution: str):
        """
        Écrit la solution dans un fichier.
        """
        with open(path_solution, "w") as f:
            # Format d'écriture selon Appendix A
            text_sol = ''
            for entrepot_built in self.entrepots:
                text_sol += f'{entrepot_built} '
            text_sol += '\n'
            for j in range(len(self.assignations)):
                text_sol += f'{self.assignations[j]} '
    
            text_sol += f'\n{self.distance_max}'
            f.write(text_sol)

 
