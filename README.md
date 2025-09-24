# Problème de p-Centre

## Présentation

Un rapport complet est disponible dans le fichier rapport.pdf.

Le problème de p-centre (pCP) consiste à déterminer l’emplacement optimal d’installations (fournissant un service) afin de garantir un niveau de qualité de service tout en respectant une contrainte budgétaire. Ce problème est fondamental pour le positionnement géographique de services tels que les hôpitaux, ambulances, casernes de pompiers, postes de police, crèches, écoles, bibliothèques, etc. Dans certains cas, il est essentiel de prendre en compte la quantité de service demandée à chaque nœud client ainsi que la capacité de service que chaque installation peut fournir. Cela conduit à une extension du problème, connue sous le nom de problème de p-centre capacitaire (CpCP).

Trois programmes linéaires en nombres entiers ont été implémentés, et pour chacun d'eux une version avec et sans capacité. Chacun de ces programmes ont des solutions plus ou moins optimales et des temps d'exécution plus ou moins rapides en fonction des différentes instances. Cependant, les relaxations linéaires n'ont pas pu fournir de résultats satisfaisant, avec un gap de plus de 200%. Cependant, la rapidité de calcul a été améliorée de 3700%. Nous remarquons que le temps maximal de calcul a souvent été atteint, ce qui suggère qu'un temps maximal plus grand permettrait d'obtenir des résultats intéressant, d'autant que les instances ayant terminé avant ont fourni des bornes duales satisfaisantes.

## Utilisation

### Environnement pyomo
> source /net/ens/pythonPyomoEnv/pyomoEnv/bin/activate

### Appel à projetOptimExpe.sh
> ./projetOptimExpe.sh > LOG/{nom_fichier}.log

### Appel à solver.py
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

### Appel à checker.py
> python checker.py -v 1 -c 0 -d Instances -n 3 -p 1 -i 1 -s Solutions -m Modeles
- `v` **version** (1, 2, 3)
- `c` **avec ou sans capacités** (0: sans; 1: avec)
- `d` **chemin vers le dossier contenant les fichiers instances** (ne pas modifier)
- `n` **nombre de noeuds dans le graphe** (voir les noms d'instances dans le dossier Instances)
- `p` **nombre d'entrepôt à construire** (voir les noms d'instances dans le dossier Instances)
- `i` **indice de l'instance** (voir les noms d'instances dans le dossier Instances)
- `s` **chemin vers le dossier contenant les fichiers solutions** (ne pas modifier)
- `m` **chemin vers le dossier contenant les fichiers modèles** (ne pas modifier)
