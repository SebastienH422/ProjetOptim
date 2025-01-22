import numpy as np

class PCentreData:
    def __init__(self, path_instance: str):
        """
        Initialise les données du problème à partir d'un fichier.
        """
        self.path_instance = path_instance
        self.nb_clients = None
        self.p = None
        self.coordonnees_clients = [] 
        self.coordonnees_installations = []
        self.Q = []
        self.q = [] 
        self.d = None # Matrice des distances
        self.Dk = []

        self.start(path_instance = path_instance)

    def start(self, path_instance : str):
        self.lire_donnees(path_instance = path_instance)

        self.calcul_dists()
        self.Deca()

    def lire_donnees(self, path_instance : str):
        """
        Lit les données depuis un fichier et les stocke dans les attributs de la classe.
        """
        with open(path_instance, "r") as f:
            ligne = f.readline().strip().split()
            self.nb_clients = int(ligne[0])
            self.p = int(ligne[1])
            for ligne in f:
                valeurs = list(map(int, ligne.strip().split()))
                x, y, qi, qj = valeurs
                
                self.coordonnees_clients.append((x, y))    #coordonées 
                self.coordonnees_installations.append((x, y))
                
                self.Q.append(qi)    #Calcul 
                self.q.append(qj)   

    def afficher_donnees(self):
        """ Affiche les données pour vérifier leur extraction. """
        print(f"Nombre de noeuds: {self.nb_clients}, Nombre d'installations à ouvrir: {self.p}")
        print("Coordonnées des clients:", self.coordonnees_clients, "\n", "Coordonées des installations: ", self.coordonnees_installations)
        print("Capacités des installations:", self.Q)
        print("Demandes des clients:", self.q)
        print("Matrice des distances :", self.d)
        


    def calcul_dists(self):
        """
        Calcule les distances entre les points clients.
        """
        
        # Conversion des deux listes en vecteurs numpy
        clients = np.array(self.coordonnees_clients)
        installations = np.array(self.coordonnees_installations)

        # Matrice numpy

        n = len(clients)
        self.d = np.zeros((n,n))

        for i in range(n):
            for j in range(n):
                diff = clients[i] - installations[j]
                self.d[i][j] = np.sqrt(np.sum(diff**2))


    def Deca(self):
        """
        Calcule les rayons D^k
        """
        for i in range(self.nb_clients):
            for j in range(self.nb_clients):
                if self.d[i][j] not in self.Dk: 
                    self.Dk.append(self.d[i][j])
