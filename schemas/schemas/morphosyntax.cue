package morphosyntax

import (
	l "pfmg.com/pkg/schemas:literals"
	"list"
)

// Syntactic category / rule name, e.g. S, NP, PP.
#category: =~"^[\(l.#upperCase)]+$"

// A non-empty list of phrase templates, each a non-empty list of symbols.
#Phrases: [...([...string] & list.MinItems(1))] & list.MinItems(1)

// One feature specification per phrase template (agreements, percolations).
// Kept as free strings: the runtime format packs constituents with ";" and
// features with ",".
#Features: [...string] & list.MinItems(1)

// One reordering per phrase template, each a list of source indices.
#Translations: [...[...int]]

// The two faces share phrases, agreements and percolations.
#Face: {
	phrases:      #Phrases
	agreements:   #Features
	percolations: #Features
}

// The source face additionally carries the translation reorderings.
#Source: {
	#Face
	translations?: #Translations
}

#Rule: {
	Source!:      #Source
	Destination!: #Face
}

// The file declares a Start symbol and one rule per category.
#MorphoSyntax: {
	Start!: string
	[#category]: #Rule
}

#MorphoSyntax
