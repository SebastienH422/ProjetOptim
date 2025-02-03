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

        with open(path_solution + 'br', 'w') as f:
            text_sol = '# Solutions brutes (valeurs des variables) \n'
            for name, val in self.variables.items():
                if name == 'x':
                    text_sol += 'x: '
                    for x_i in val:
                        for x_ij in x_i:
                            text_sol += f'{x_ij} '
                        text_sol += '// '
                    text_sol += '\n'
                else:
                    text_sol += f'{name}: '
                    for yz in val:
                        text_sol += f'{yz} '
                    text_sol += '\n'
            f.write(text_sol)
        with open(path_solution + 'brm', 'w') as f:
            text_sol = '# Solutions brutes (valeurs des variables) \n'
            
            for name, val in self.variables.items():
                if name == 'x':
                    max_x = 0
                    for xi in val:
                        max_x = max(max_x, max(xi))
                    text_sol += 'x: '
                    for x_i in val:
                        for x_ij in x_i:
                            text_sol += f'{round(x_ij / max_x)} '
                        text_sol += '// '
                    text_sol += '\n'
                else:
                    max_yzu = max(val) if max(val) else 1
                    text_sol += f'{name}: '
                    for yzu in val:
                        text_sol += f'{round(yzu / max_yzu)} '
                    text_sol += '\n'
            f.write(text_sol)


        
        


 
