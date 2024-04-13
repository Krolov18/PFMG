package gloses

import (
    l "pfmg.com/pkg/schemas:literals"
    "list"
//    "struct"
)

#CatAttVals: [=~ "^[\(l.#upperCase)]+$"]: #AttVals | #ListAttVals
#AttVals: [=~ "^[\(l.#upperCase)][\(l.#lowerCase)]+$"]: [...=~ "^[\(l.#lowerAlphaNumCase)]+$"]  & list.MinItems(1) & list.UniqueItems()
#ListAttVals: [...#AttVals] & [_, ...#AttVals]

source!: #CatAttVals // & struct.MinFields(1)
destination!: #CatAttVals // & struct.MinFields(1)
