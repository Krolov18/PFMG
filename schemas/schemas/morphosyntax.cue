package morphosyntax

//import (
//	"list"
//	"struct"
//)

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

#Syntagmes: [#identifier]: [...[...string] & [_, ...string]]

#Accords: [#identifier]: [...string] & [_, ...string]

#Percolations: [#identifier]: [...string] & [_, ...string]

#Traductions: [#identifier]: [...[...int]]

#Longueur: #SAPT & {
	syntagmes:    _
	accords:      _
	percolations: _
	_sameLength:  and([ for key, value in syntagmes {len(value), len(accords[key]), len(percolations[key])}])
	_sameKeys:    and([...])
}
