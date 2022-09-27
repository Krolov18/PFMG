import (
	r "regexp"
	l "list"
)

#Category:  =~"^(NOM|VER|ADJ|DET|PREP)$"
#Attribute: =~"^(Genre|Nombre|Temps|Pers)$"
#Value:     =~"^(3(Sg|Du|Pl)|P(RS|ST)|Sg|Du|Pl|[MFN])$"

#Genre:  =~"^[MFN]$"
#Nombre: =~"^(Sg|Du|Pl)$"
#Pers:   =~"^3(Sg|Pl|Du)$"
#Temps:  =~"^P(RS|ST)$"

#Sigma: {[#Attribute]: #Value}

#SigmaNOM: {#Sigma, Genre: #Genre, Nombre: #Nombre}
#SigmaMSg: {#SigmaNOM, Genre: "M", Nombre: "Sg"}
#SigmaMPl: {#SigmaNOM, Genre: "M", Nombre: "Pl"}
#SigmaFSg: {#SigmaNOM, Genre: "F", Nombre: "Sg"}
#SigmaFPl: {#SigmaNOM, Genre: "F", Nombre: "Pl"}

#SigmaVER: {#Sigma, Temps: #Temps, Pers: #Pers, Genre: #Genre}
#SigmaPRS3SgM: {#SigmaVER, Temps: "PRS", Pers: "3Sg", Genre: "M"}
#SigmaPRS3SgF: {#SigmaVER, Temps: "PRS", Pers: "3Sg", Genre: "F"}
#SigmaPRS3SgN: {#SigmaVER, Temps: "PRS", Pers: "3Sg", Genre: "N"}
#SigmaPRS3DuM: {#SigmaVER, Temps: "PRS", Pers: "3Du", Genre: "M"}
#SigmaPRS3DuF: {#SigmaVER, Temps: "PRS", Pers: "3Du", Genre: "F"}
#SigmaPRS3DuN: {#SigmaVER, Temps: "PRS", Pers: "3Du", Genre: "N"}
#SigmaPRS3PlM: {#SigmaVER, Temps: "PRS", Pers: "3Pl", Genre: "M"}
#SigmaPRS3PlF: {#SigmaVER, Temps: "PRS", Pers: "3Pl", Genre: "F"}
#SigmaPRS3PlN: {#SigmaVER, Temps: "PRS", Pers: "3Pl", Genre: "N"}
#SigmaPST3SgM: {#SigmaVER, Temps: "PST", Pers: "3Sg", Genre: "M"}
#SigmaPST3SgF: {#SigmaVER, Temps: "PST", Pers: "3Sg", Genre: "F"}
#SigmaPST3SgN: {#SigmaVER, Temps: "PST", Pers: "3Sg", Genre: "N"}
#SigmaPST3DuM: {#SigmaVER, Temps: "PST", Pers: "3Du", Genre: "M"}
#SigmaPST3DuF: {#SigmaVER, Temps: "PST", Pers: "3Du", Genre: "F"}
#SigmaPST3DuN: {#SigmaVER, Temps: "PST", Pers: "3Du", Genre: "N"}
#SigmaPST3PlM: {#SigmaVER, Temps: "PST", Pers: "3Pl", Genre: "M"}
#SigmaPST3PlF: {#SigmaVER, Temps: "PST", Pers: "3Pl", Genre: "F"}

#SigmaPST3PlN: {#SigmaVER, Temps: "PST", Pers: "3Pl", Genre: "N"}

//#SigmaADJ: {#Sigma, Genre: #Genre, Nombre: #Nombre}
//#SigmaDET: {#Sigma, Genre: #Genre, Nombre: #Nombre}

#SigmaPREP: #Sigma

#Forme: {
	_lexeme:     #Lexeme
	pos:         #Category
	sigma:       #Sigma & _lexeme.sigma
	realisation: string | *morphemes[len(morphemes)-1].realisation
	morphemes:   [...#Morpheme] & [_, ...#Morpheme]
}

#FormeNOM: {#Forme, pos: "NOM"}

#FormeNOMMSg: {#FormeNOM, sigma: #SigmaMSg}
#FormeNOMMPl: {#FormeNOM, sigma: #SigmaMPl}
#FormeNOMFSg: {#FormeNOM, sigma: #SigmaFSg}
#FormeNOMFPl: {#FormeNOM, sigma: #SigmaFPl}

#FormeVER: {#Forme, pos: "VER"}

#FormePRS3SgM: {#FormeVER, sigma: #SigmaPRS3SgM}
#FormePRS3SgF: {#FormeVER, sigma: #SigmaPRS3SgF}
#FormePRS3SgN: {#FormeVER, sigma: #SigmaPRS3SgN}
#FormePRS3DuM: {#FormeVER, sigma: #SigmaPRS3DuM}
#FormePRS3DuF: {#FormeVER, sigma: #SigmaPRS3DuF}
#FormePRS3DuN: {#FormeVER, sigma: #SigmaPRS3DuN}
#FormePRS3PlM: {#FormeVER, sigma: #SigmaPRS3PlM}
#FormePRS3PlF: {#FormeVER, sigma: #SigmaPRS3PlF}
#FormePRS3PlN: {#FormeVER, sigma: #SigmaPRS3PlN}
#FormePST3SgM: {#FormeVER, sigma: #SigmaPST3SgM}
#FormePST3SgF: {#FormeVER, sigma: #SigmaPST3SgF}
#FormePST3SgN: {#FormeVER, sigma: #SigmaPST3SgN}
#FormePST3DuM: {#FormeVER, sigma: #SigmaPST3DuM}
#FormePST3DuF: {#FormeVER, sigma: #SigmaPST3DuF}
#FormePST3DuN: {#FormeVER, sigma: #SigmaPST3DuN}
#FormePST3PlM: {#FormeVER, sigma: #SigmaPST3PlM}
#FormePST3PlF: {#FormeVER, sigma: #SigmaPST3PlF}
#FormePST3PlN: {#FormeVER, sigma: #SigmaPST3PlN}

//#FormeADJ: {#Forme, pos: "ADJ"}
//#FormeDET: {#Forme, pos: "DET"}
#FormePREP: {#Forme, pos: "PREP"}

#Morpheme: {
	stem:        string
	rule?:       string
	realisation: string
	sigma:       #Sigma
	position?:   int
}

#Prefix: {
	#Morpheme
	stem:        string
	rule:        string & =~"^[a-z]+\\+X$"
	realisation: r.FindSubmatch("([a-z]+)\\+X", rule)[1] + stem
}

#Suffix: {
	#Morpheme
	stem:        string
	rule:        string & =~"^X\\+[a-z]+$"
	realisation: stem + r.FindSubmatch("X\\+([a-z]+)", rule)[1]
}

#Circumfix: {
	#Morpheme
	stem:        string
	rule:        string & =~"^[a-z]+\\+X\\+[a-z]+$"
	_affixes:    [string, string] & l.Slice(r.FindSubmatch("([a-z]+)\\+X\\+([a-z]+)", rule), 1, 3)
	realisation: _affixes[0] + stem + _affixes[1]
}

#Identity: {
	#Morpheme
	stem:        string
	realisation: stem
}

#Lexeme: {
	pos:       #Category
	sigma:     #Sigma
	morphemes: [...#Morpheme] & [_, ...#Morpheme]
	stems:     string
}
#LexemeNOM: {
	#Lexeme
	pos: "NOM", morphemes: [
		{#Prefix, sigma: {Nombre: "Sg"}, rule: "so+X"} |
		{#Prefix, sigma: {Nombre: "Du"}, rule: "ti+X"} |
		{#Prefix, sigma: {Nombre: "Pl"}, rule: "Na+X"},
	]}
#LexemeVER: {
	#Lexeme
	pos: "VER"
	morphemes: [
		{#Suffix, sigma: {Temps: "PRS"}, rule: "X+z"} |
		{#Suffix, sigma: {Temps: "PST"}, rule: "X+j"},
		{#Suffix, sigma: {Pers:  "3Sg"}, rule: "X+ev"} |
		{#Suffix, sigma: {Pers: "3Du"}, rule: "X+ub"} |
		{#Suffix, sigma: {Pers:  "3Pl"}, rule: "X+ot"},
		{#Suffix, sigma: {Genre: "M"}, rule:   "X+a"} |
		{#Suffix, sigma: {Genre: "F"}, rule: "X+i"} |
		{#Suffix, sigma: {Genre: "N"}, rule: "X+e"},
	]}
#LexemeADJ: {#Lexeme, pos: "ADJ", morphemes: [
				{sigma: {Nombre: "Sg"}, rule: "X+b"} |
	{sigma: {Nombre: "Du"}, rule: "X+s"} |
	{sigma: {Nombre: "Pl"}, rule: "X+w"},
	{sigma: {Genre:  "M"}, rule:  "X+ek"} |
	{sigma: {Genre: "F"}, rule: "X+as"} |
	{sigma: {Genre: "N"}, rule: "X+u"},
]}

#LexemeDET: {
	#Lexeme
	pos: "DET"
	morphemes: [
		{#Suffix, sigma: {Genre: "M"}, rule: "X+o"} |
		{#Suffix, sigma: {Genre: "F"}, rule: "X+a"} |
		{#Suffix, sigma: {Genre:  "N"}, rule:  "X+e"},
		{#Suffix, sigma: {Nombre: "Sg"}, rule: "X+n"} |
		{#Suffix, sigma: {Nombre: "Du"}, rule: "X+ri"} |
		{#Suffix, sigma: {Nombre: "Pl"}, rule: "X+p"},
	]
}
#LexemePREP: {
	#Lexeme
	pos: "PREP"
}

#Forme: {
	#Forme
	_lexeme: #Lexeme
	morphemes: [#Morpheme & {stem: _lexeme.stems}, ...]
}

#FormeNOM: {
	#FormeNOM
	_lexeme: #LexemeNOM
	morphemes: [#Morpheme]
}

#FormePREP: {
	#FormePREP
	_lexeme: #LexemePREP
	morphemes: [#Identity]
}

#FormeADJ: {
	#FormeADJ
	_lexeme: #LexemeADJ
	morphemes: morphemes: [
		#Morpheme,
		#Morpheme & {stem: morphemes[0].realisation},
	]
}

#FormeVER: {
	#FormeVER
	_lexeme: #LexemeVER
	morphemes: [
		#Morpheme,
		#Morpheme & {stem: morphemes[0].realisation},
		#Morpheme & {stem: morphemes[1].realisation},
	]
}

//c: {
// #FormePRS3SgM
// _lexeme: stems: "dila", morphemes: [for m in _lexeme.morphemes {m&{sigma: c.sigma}}]
//}
//c: {
// #FormePREP
// _lexeme: {stems: "NiSaw"},
// morphemes: [for m in _lexeme.morphemes {m & {sigma: c.sigma}}]
//}

//#dila: {#LexemeVER, stems: "dila", morphemes: [for m in #dila._lexeme.morphemes {m&{sigma: #dila.sigma}}]}

FormePRS3SgM: {#FormePRS3SgM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3SgM.sigma}}]}
FormePRS3SgF: {#FormePRS3SgF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3SgF.sigma}}]}
FormePRS3SgN: {#FormePRS3SgN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3SgN.sigma}}]}
FormePRS3DuM: {#FormePRS3DuM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3DuM.sigma}}]}
FormePRS3DuF: {#FormePRS3DuF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3DuF.sigma}}]}
FormePRS3DuN: {#FormePRS3DuN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3DuN.sigma}}]}
FormePRS3PlM: {#FormePRS3PlM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3PlM.sigma}}]}
FormePRS3PlF: {#FormePRS3PlF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3PlF.sigma}}]}
FormePRS3PlN: {#FormePRS3PlN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePRS3PlN.sigma}}]}
FormePST3SgM: {#FormePST3SgM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3SgM.sigma}}]}
FormePST3SgF: {#FormePST3SgF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3SgF.sigma}}]}
FormePST3SgN: {#FormePST3SgN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3SgN.sigma}}]}
FormePST3DuM: {#FormePST3DuM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3DuM.sigma}}]}
FormePST3DuF: {#FormePST3DuF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3DuF.sigma}}]}
FormePST3DuN: {#FormePST3DuN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3DuN.sigma}}]}
FormePST3PlM: {#FormePST3PlM, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3PlM.sigma}}]}
FormePST3PlF: {#FormePST3PlF, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3PlF.sigma}}]}
FormePST3PlN: {#FormePST3PlN, _lexeme: morphemes: [ for m in _lexeme.morphemes {m & {sigma: FormePST3PlN.sigma}}]}
