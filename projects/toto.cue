package truc

import p "example.com/pkg/schemas/primitive"

p.#Gloses & {
    NOM: {
        Genre: ["m", "f"]
        Nombre: ["sg", "pl"]
    }
    ADJ: {
        [
            {Mode: ["inf"]},
            {Nombre: ["sg", "pl"]
             Genre: ["m", "f"]}
        ]
    }
}
o: p.#Toto
