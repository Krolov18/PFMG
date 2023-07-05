package morphosyntax

import (
	"list"
	"struct"
)

#category: =~"^[A-Z]+$"

#MS: {
	source:      #SAPT
	destination: #SAP
}

#SAP: {
	syntagmes:    #Syntagmes
	accords:      #Accords
	percolations: #Percolations
}

#SAPT: {
	#SAP
	traductions: #Traductions
}

#identifier: =~"[A-Z]+P"

#Syntagmes: [#identifier]: [...[...string]]

#Accords: [#identifier]: [...[...string] | string]

#Percolations: [#identifier]: [...[...string] | string]

#Traductions: [#identifier]: [...[...int]]

#Longueur: #SAPT & {
	syntagmes:    _
	accords:      _
	percolations: _
	_sameLength:  and([ for key, value in syntagmes {len(value), len(accords[key]), len(percolations[key])}])
	_sameKeys:    and([...])
}

#Francais: #Longueur & {
	syntagmes: NP: [["D", "A*", "N", "A*"]]
	accords: NP: ["Genre,Nombre"]
	percolations: NP: ["Genre,Nombre"]
	traductions: NP: [[]]
}
