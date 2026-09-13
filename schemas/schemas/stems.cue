package stems

import l "pfmg.com/pkg/schemas:literals"

// Grammatical category, e.g. NOM, ADJ, V.
#category: =~"^[\(l.#upperCase)]+$"

// Stems are stored as an arbitrarily deep tree: intermediate keys are feature
// specifications, leaf keys are stem identifiers, and each leaf value is the
// (comma-separated, optionally annotated) surface form string.
#Inheritance: {
	[string]: string | #Inheritance
}

#Stems: {
	[#category]: #Inheritance
}

#Stems
