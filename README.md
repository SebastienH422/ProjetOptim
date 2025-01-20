# ProjetOptim

## Vrac
### Début rapport
- On doit faire un min max des dij utilisés, donc créer une variable représentant le max des dij utilisé
- On a la formule du cours 3.C minimum entre deux valeurs. Il faut adapter la formule au cas max, et au cas avec beaucoup d'indices (la formule du cours utilise deux indices)
- On doit faire en sorte que les contraintes découlant du max entre les dij soient compatibles avec les autres contraintes du problème.

### Première reformulation du max des variables
On renumérote $E = {(i,j)}$ par $E = {1, ..., K}$. On définit les variables $B_i$ pour $i \in E$ par
$B_i = max(B_{i+1}, x_i)\\
B_k = x_k$

Ainsi, on cherche à minimiser 
$$
\begin{array}
  B_1 &= max(x_1, B_2)\\
      &= max(x_1, max(x_2, B_3))\\
      &= max(x_1, max(x_2, max(x_3, B_4)))\\
      &= ...\\
      &= max(x_1, ..., x_K)
\end{array}
$$
