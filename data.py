class PCentreData:
    def __init__(self, fichier_donnees: str):
        """
        Initialise les données du problème à partir d'un fichier.
        """
        self.fichier_donnees = fichier_donnees
        self.nb_points = 0
        self.nb_ouvrir = 0
        self.arcs = []
        self.capacites = {}

        self.lire_donnees()

    def lire_donnees(self):
        """
        Lit les données depuis un fichier et les stocke dans les attributs de la classe.
        """
        with open(self.fichier_donnees, "r") as f:
            # Lire et parser les données ici
            # TODO
            pass  # Implémentation à ajouter
