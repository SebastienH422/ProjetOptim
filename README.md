# ProjetOptim

## Appel à solver.py
> python solver.py -v 1 -c 0 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles
- `v` version (1, 2, 3)
- `c` avec ou sans capacités (0: sans; 1: avec)
- `d` chemin vers le dossier contenant les fichiers instances (ne pas modifier)
- `t` temps d'exécution max en secondes (1 < `t`)
- `n` nombre de noeuds dans le graphe (voir les noms d'instances dans le dossier Instances)
- `p` nombre d'entrepôt à construire (voir les noms d'instances dans le dossier Instances)
- `i` indice de l'instance (voir les noms d'instances dans le dossier Instances)
- `s` chemin vers le dossier contenant les fichiers solutions (ne pas modifier)
- `m` chemin vers le dossier contenant les fichiers modèles (ne pas modifier)

#### Lancer toutes les instances et toutes les versions


## Appel à checker.py
python solver.py -v 1 -c 0 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 1 -c 1 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 2 -c 0 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 2 -c 1 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 3 -c 0 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 3 -c 1 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles;python solver.py -v 1 -c 0 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles;python solver.py -v 1 -c 1 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles;python solver.py -v 2 -c 0 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles;python solver.py -v 2 -c 1 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles;python solver.py -v 3 -c 0 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles;python solver.py -v 3 -c 1 -d Instances -t 100 -n 5 -p 2 -i 1 -s Solutions -m Modeles
