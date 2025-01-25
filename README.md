# ProjetOptim

## Appel à projetOptimExpe.sh
> ./projetOptimExpe.sh > LOG/{nom_fichier}.log

## Appel à solver.py
> python solver.py -v 1 -c 0 -d Instances -t 100 -n 3 -p 1 -i 1 -s Solutions -m Modeles
- `v` **version** (1, 2, 3)
- `c` **avec ou sans capacités** (0: sans; 1: avec)
- `d` **chemin vers le dossier contenant les fichiers instances** (ne pas modifier)
- `t` **temps d'exécution max en secondes** (1 < `t`)
- `n` **nombre de noeuds dans le graphe** (voir les noms d'instances dans le dossier Instances)
- `p` **nombre d'entrepôt à construire** (voir les noms d'instances dans le dossier Instances)
- `i` **indice de l'instance** (voir les noms d'instances dans le dossier Instances)
- `s` **chemin vers le dossier contenant les fichiers solutions** (ne pas modifier)
- `m` **chemin vers le dossier contenant les fichiers modèles** (ne pas modifier)

## Appel à checker.py
> python checker.py -v 1 -c 0 -d Instances -n 3 -p 1 -i 1 -s Solutions -m Modeles
- `v` **version** (1, 2, 3)
- `c` **avec ou sans capacités** (0: sans; 1: avec)
- `d` **chemin vers le dossier contenant les fichiers instances** (ne pas modifier)
- `n` **nombre de noeuds dans le graphe** (voir les noms d'instances dans le dossier Instances)
- `p` **nombre d'entrepôt à construire** (voir les noms d'instances dans le dossier Instances)
- `i` **indice de l'instance** (voir les noms d'instances dans le dossier Instances)
- `s` **chemin vers le dossier contenant les fichiers solutions** (ne pas modifier)
- `m` **chemin vers le dossier contenant les fichiers modèles** (ne pas modifier)
