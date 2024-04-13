package morphosyntax

//import (
//	"list"
//	"struct"
//)

#category: =~"^[A-Z]+$"

#File: {
	start?: string
	#Rules
}

#Rule: {
	Source: #SAPT
	Destination: #SAP
}

#Rules: [#identifier]: #Rule

#SAP: {
	Syntagmes:    #Syntagmes
	Accords:      #Accords
	Percolations: #Percolations
}

#SAPT: {
	#SAP
	Traduction: #Traductions
}

#identifier: =~"[A-Z]+P?"

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

#File
