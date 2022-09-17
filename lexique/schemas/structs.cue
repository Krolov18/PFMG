package kalaba
//import "strings"
//import "list"

//consonnes: "zrtqsdfgbvcxwphjklmnç"
//voyelles: "aâäàeéèêëiîïoôöuûüùyŷÿ"
//lowerCase: consonnes + voyelles
//upperCase: "ZRTQSDFGBVCXWPHJKLMNÇ" + "AÂÄÀEÉÈÊËIÎÏOÔÖUÛÜÙYŶŸ"
//alphaCase: lowerCase + upperCase
//alphaNumCase: alphaCase + "0-9"
//upperAlphaNumCase: upperCase + "0-9"
//lowerAlphaNumCase: lowerCase + "0-9"
//
//#Gloses : {
//	source : #CatAttVals
//	destination : #CatAttVals
//	#CatAttVals : {
//		[=~ "^[\(upperCase)]+$"]: #AttVals | #ListAttVals
//	}
//	#AttVals : [=~ "^[\(upperCase)][\(lowerCase)]+$"]: [...=~ "^[\(lowerAlphaNumCase)]+$"]
//	#ListAttVals : [...#AttVals]
//}
//
//#Blocks: {
//	source: #CatBlocks
//	destination: #CatBlocks
//
//	#CatBlocks: [=~ "^[\(upperCase)]+$"]: #Blocks
//	#Blocks: list.minItems(1) & [...#Block]
//	#Block: [=~ "^[\(upperCase)][\(lowerCase)]+=[\(lowerAlphaNumCase)]+(,[\(upperCase)][\(lowerCase)]+=[\(lowerAlphaNumCase)]+)*$"]: #prefixation | #suffixation | #condition | #circonfixation | #gabarit | #selection
//	#prefixation: =~"^[\(lowerCase)]+\\+X$"
//	#suffixation: =~"^X\\+[\(lowerCase)]+$"
//	#condition: =~"^X[0-9]\\?X[0-9]\\:X[0-9]$"
//	#circonfixation: =~"^[\(lowerCase)]+\\+X\\+[\(lowerCase)]+$"
//	#gabarit: =~"^[1-9AUVaeiou]{4,9}$"
//	#selection: =~"^X[1-9][0-9]*$"
//}

//#Morphosyntax : {
//	start: =~ "^[\(upperCase)]+P$"
//	contractions: [=~"^[\(alphaCase)]+$"]: [...=~"^[\(alphaCase)]+$"]
//	source: #Structure
//	destination: #Structure
//
//	#Structure: {
//		syntagmes: [=~ "^[\(upperCase)]+P$"]: list.minItems(1) & [... list.minItems(1) & [...#Categorie]]
//		accords: string
//		percolations: string
//		traductions?: string
//	}
//	#Categorie: #Nonterminal | #Terminal | #Optional
//	#Nonterminal: =~ "^[\(upperCase)]+$"
//	#Terminal: =~ "^'[\(lowerCase)]+'$"
//	#Optional: =~ "^\(#Nonterminal)/\\?$"
//}

#Morphosyntax : {
	start: string
	contractions : string
	source: string
	destination: string
}

[string]: #Morphosyntax
