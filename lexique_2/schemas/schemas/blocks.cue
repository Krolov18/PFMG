package blocks

import l "pfmg.com/pkg/schemas:literals"


#CatBlocks: [=~ "^[\(l.#upperCase)]+$"]: #Blocks

#Blocks: [...#Block] & [_, ...#Block]

#Block: [=~ "^[\(l.#upperCase)][\(l.#lowerCase)]+=[\(l.#lowerAlphaNumCase)]+(,[\(l.#upperCase)][\(l.#lowerCase)]+=[\(l.#lowerAlphaNumCase)]+)*$"]: #prefixation | #suffixation | #condition | #circonfixation | #gabarit | #selection

#prefixation: =~"^[\(l.#lowerCase)]+\\+X$"
#suffixation: =~"^X\\+[\(l.#lowerCase)]+$"
#condition: =~"^X[0-9]\\?X[0-9]\\:X[0-9]$"
#circonfixation: =~"^[\(l.#lowerCase)]+\\+X\\+[\(l.#lowerCase)]+$"
#gabarit: =~"^[1-9AUVaeiou]{4,9}$"
#selection: =~"^X[1-9][0-9]*$"
