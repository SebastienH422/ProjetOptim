class PCentreData:
    def __init__(self, fichier_donnees: str):
        """
        Initialise les données du problème à partir d'un fichier.
        """
        self.fichier_donnees = fichier_donnees
        self.nb_points = 0
        self.nb_ouvrir = 0
        self.coordonnees = []
        self.capacites = []
        self.demandes = []

        self.lire_donnees()

    def lire_donnees(self):
        """
        Lit les données depuis un fichier et les stocke dans les attributs de la classe.
        """
        with open(self.fichier_donnees, "r") as f:
            ligne = f.readline().strip().split()
            self.nb_points = int(ligne[0])
            self.nb_ouvrir = int(ligne[1])
            for ligne in f:
                valeurs = list(map(int, ligne.strip().split()))
                x, y, qi, qj = valeurs
                
                self.coordonnees.append((x, y))
                self.capacites.append(qi)
                self.demandes.append(qj)

    def afficher_donnees(self):
        """ Affiche les données pour vérifier leur extraction. """
        print(f"Nombre de noeuds: {self.nb_points}, Nombre d'installations à ouvrir: {self.nb_ouvrir}")
        print("Coordonnées des noeuds:", self.coordonnees)
        print("Capacités des installations:", self.capacites)
        print("Demandes des clients:", self.demandes)


data = PCentreData("data/n3p1i1")
data.afficher_donnees()
