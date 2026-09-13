package gloses

import (
	l "pfmg.com/pkg/schemas:literals"
	"list"
)

// A single "Attribute=value" assignment (used in alignment keys and values).
#att: "[\(l.#upperCase)][\(l.#alphaCase)]*=[\(l.#lowerAlphaNumCase)]+"

// Grammatical category, e.g. NOM, ADJ, V.
#category: =~"^[\(l.#upperCase)]+$"

// Attribute name, e.g. Genre, Nombre, Cf.
#attribute: =~"^[\(l.#upperCase)][\(l.#alphaCase)]*$"

// Attribute value, e.g. m, sg, n1.
#value: =~"^[\(l.#lowerAlphaNumCase)]+$"

// One or more comma-separated assignments, e.g. "Nombre=sg,Det=def".
#featureset: =~"^\(#att)(,\(#att))*$"

// Attribute inventory: each attribute maps to its non-empty list of values.
#AttVals: {
	[#attribute]: [...#value] & list.MinItems(1) & list.UniqueItems()
}

// Every category declares a source and a destination inventory, plus an
// optional source->destination feature alignment table.
#Gloses: {
	[#category]: {
		source!:      #AttVals
		destination!: #AttVals
		alignments?: {
			[#featureset]: [...#featureset] & list.MinItems(1)
		}
	}
}

#Gloses
