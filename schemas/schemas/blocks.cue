package blocks

import l "pfmg.com/pkg/schemas:literals"

// A single "Attribute=value" assignment.
#att: "[\(l.#upperCase)][\(l.#alphaCase)]*=[\(l.#lowerAlphaNumCase)]+"

// Grammatical category, e.g. NOM, ADJ, V.
#category: =~"^[\(l.#upperCase)]+$"

// One or more comma-separated assignments, e.g. "Genre=m,Nombre=sg".
#featureset: =~"^\(#att)(,\(#att))*$"

// A realization block: each feature specification maps to a non-empty
// realization pattern (prefix, suffix, template, condition, selection, ...).
#Block: {
	[#featureset]: string & !=""
}

// Every category declares an ordered list of source and destination blocks.
#Blocks: {
	[#category]: {
		source!:      [...#Block]
		destination!: [...#Block]
	}
}

#Blocks
