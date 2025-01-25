#!/bin/bash

dossier_Instances="Instances"
dossier_Solutions="Solutions"
dossier_Experimentation="Experimentations"


# Les valeurs de p pour chaque n
Noeuds=(300) # Ensemble des valeurs possibles de n: 300 500 1000 2000 3000
P_300=(30 42 75 100) 
P_500=(50 71 125 166)
P_1000=(100 142 250 333)
P_2000=(200 285 500 666)
P_3000=(300 428 750 1000)
index=(1 2 3 4 5) # Ensemble des valeurs possibles de i

# Petites instances
# Noeuds=(3 5)
# P_3=(1)
# P_5=(2)
# index=(1)

version=(1 2 3) # Les versions du problème
capacite=(0 1) # Les valeurs d'activation de la contrainte de capacité
TL=600  # Temps limite de résolution

for n in "${Noeuds[@]}"; do
    results_file="${dossier_Experimentation}/results_n${n}.txt"
    rm -f "$results_file" 
    echo "n p i v c erreur statut etat temps_creation temps gap obj obj_upper obj_lower" >> "${results_file}" # Entête du fichier de résultats
    mesP="P_${n}[@]"
    for p in "${!mesP}"; do
        for i in "${index[@]}"; do
            instance="${dossier_Instances}/n${n}p${p}i${i}"
            for v in "${version[@]}"; do
                for c in "${capacite[@]}"; do
                    echo "Résolution: Instance_n${n}p${p}i${i} Modèle_v${v}_c${c}"
                    python3 solver.py -v "${v}" -c "${c}" -d "${dossier_Instances}" -t "${TL}" -n "${n}" -p "${p}" -i "${i}" -s "${dossier_Solutions}" -r "${results_file}"
                done
            done
        done 
    done    
    echo "Fin de résolution du  groupe de ${n} noeuds"
done
