#!/bin/bash

# Définir le chemin du fichier source
source_file="header_copyright.txt"

# Fonction pour vérifier si le contenu du fichier source est déjà présent au début du fichier cible
contains_source() {
    local source_content=$(cat "$source_file")
    local file_content=$(head -n $(wc -l < "$source_file") "$1")
    [ "$source_content" = "$file_content" ]
}

# Récupérer la liste des fichiers dans le répertoire
for file in `find . -name "*.py"`; do
    # Vérifier si le contenu du fichier source est déjà présent au début du fichier cible
    if ! contains_source "$file"; then
        # Copier le contenu du fichier source au début du fichier actuel
        cat "$source_file" "$file" > temp && mv temp "$file"
    fi
done

