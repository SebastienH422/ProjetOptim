from data import PCentreData
from solution import PCentreSolution
import pyomo.opt as po
import pyomo.environ as pe
from pyomo.common.errors import PyomoException
import time

class ModelesPCentre:
     #_______________________ Attributs _______________________   
    def __init__(self, data):
        """
        Initialise le modèle avec les données.
        """
        self.data = data
        self.solution = PCentreSolution()
        self.modele = None
        self.gap = -1
        self.temps = -1
        self.obj = -1
        self.obj_upper = -1
        self.obj_lower = -1
        self.status = False
        self.etat = False
        self.temps_creation = -1
        self.erreur = 'ras'

        self.capacity = -1
        self.results = None

    #_______________________ Méthodes Création _______________________
    def creer_modele(self, capacite):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def extraire_solution(self):
        """
        Méthode virtuelle à implémenter dans les sous-classes.
        """
        raise NotImplementedError("This method should be overridden by subclasses")

    def ecrire_modele(self, file_name):
        """
        Sauvegarde le modèle dans un fichier LP.
        """
        if self.modele is None:
            raise ValueError("Model has not been built yet. Call build_model() first.")
        # Write the model to a .lp file
        self.modele.write(file_name, io_options = {"symbolic_solver_labels":True})

    def lancer(self, temps_limite):
        """
        Résout le modèle avec un solveur.
        """

        if self.modele is None:
            raise ValueError("Model has not been built yet. Call build_model() first.")
        
        solver_name = 'appsi_highs'
        # Creation of the solver with the desired parameters
        solver = po.SolverFactory(solver_name)
        # Set the options of the solver
        solver.options['time_limit'] = temps_limite
        solver.options['mip_rel_gap'] = 1e-6
        solver.options['mip_abs_gap'] = 0.99
        solver.options['threads'] = 2  # Utiliser 2 threads
        
        
        try:

            # Solve the model
            start_time = time.time()
            results = solver.solve(self.modele, tee = False) # Tee = True means that the solver log is print, set Tee = False to not display the log
            end_time = time.time()
            if results.solver.termination_condition == po.TerminationCondition.optimal:
                self.etat = True
                self.status = True
            if results.solver.termination_condition == po.TerminationCondition.maxTimeLimit:
                self.etat = False
                self.status = True

        except ValueError as ve:
            print("ValueError capturé :", ve)
            self.erreur = ve
        except RuntimeError as re:
            print("RuntimeError capturé :", re)
            self.erreur = re
        except PyomoException as ae:
            print("Erreur liée à l'exécution de Highs :", ae)
            self.erreur = ae
        except FileNotFoundError as fe:
            print("Solveur Highs introuvable :", fe)
            self.erreur = fe
        except Exception as e:
            print("Autre erreur :", e)
            self.erreur = e

        # Save the results
        if self.status:
            self.temps = round(end_time - start_time, 3)
            self.obj = round(pe.value(self.modele.obj), 3)
            self.obj_upper = round(results.problem.upper_bound, 3)
            self.obj_lower = round(results.problem.lower_bound, 3)
            self.gap = abs(self.obj_upper - self.obj_lower)
            if self.obj_upper != 0:
                self.gap = 100 * self.gap / abs(self.obj_upper)
            self.gap = round(self.gap, 2)
        
            self.results = results
