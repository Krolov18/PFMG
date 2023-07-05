package gloses

import (
    l "pfmg.com/pkg/schemas:literals"
    "list"
)

#CatAttVals : [=~ "^[\(l.#upperCase)]+$"]: #AttVals | #ListAttVals
#AttVals : [=~ "^[\(l.#upperCase)][\(l.#lowerCase)]+$"]: [...=~ "^[\(l.#lowerAlphaNumCase)]+$"]  & list.MinItems(1) & list.UniqueItems()
#ListAttVals: [...#AttVals] & [_, ...#AttVals]
