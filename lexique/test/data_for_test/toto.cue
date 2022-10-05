import (
	r "regexp"
	l "list"
)

#Sigma: {...}
//#Sigma: {[#Attribute]: #Value}

#Lexeme: {
	pos:        #Category
	sigma:      #Sigma
	paradigm:   [...#Morpheme] | *[]
	stems:      string
}

#Forme: {
	_lexeme:      #Lexeme
	pos:          #Category & _lexeme.pos
	sigma:        _lexeme.sigma
	realisation:  string | *_lexeme.stems
	morphemes:    ([...#Morpheme] & [#Morpheme & {stem: _lexeme.stems}, ...#Morpheme]) | *[]
	morphemes:    [for x in _lexeme.paradigm {x & {_sigma: sigma}}]
}

#Morpheme: {
	stem:          string
	rule?:         string
	realisation:   string
	sigma:         #Sigma
	_sigma:        #Sigma
	position?:     int
	//           decoupage?: string
}

#Prefix: {
	#Morpheme
	stem:          string
	rule:          string & =~"^[a-zA-Z]+\\+X$"
	realisation:   r.FindSubmatch("([a-zA-Z]+)\\+X", rule)[1] + stem
	//           decoupage: r.FindSubmatch("([a-z]+)\\+X", rule)[1] + "-" + stem
}

#Suffix: {
	#Morpheme
	stem:          string
	rule:          string & =~"^X\\+[a-zA-Z]+$"
	realisation:   stem + r.FindSubmatch("X\\+([a-zA-Z]+)", rule)[1]
	//           decoupage: stem + "-" + r.FindSubmatch("([a-z]+)\\+X", rule)[1]
}

#Circumfix: {
	#Morpheme
	stem:         string
	rule:         string & =~"^[a-zA-Z]+\\+X\\+[a-zA-Z]+$"
	_affixes:     [string, string] & l.Slice(r.FindSubmatch("([a-zA-Z]+)\\+X\\+([a-zA-Z]+)", rule), 1, 3)
	realisation:  _affixes[0] + stem + _affixes[1]
	//           decoupage: _affixes[0] + "-" + stem + "-" + _affixes[1]
}

#Identity: {
	#Morpheme
	stem:         string
	realisation:  stem
}

#Category:  =~"^(NOM|VER|ADJ|DET|PREP)$"
#Attribute: =~"^(Genre|Nombre|Temps|Pers)$"
#Value:     =~"^(3(Sg|Du|Pl)|P(RS|ST)|Sg|Du|Pl|[MFN])$"

#Genre:  =~"^[MFN]$"
#Nombre: =~"^(Sg|Du|Pl)$"
#Pers:   =~"^3(Sg|Pl|Du)$"
#Temps:  =~"^P(RS|ST)$"

#SigmaNOM: {#Sigma, Genre: #Genre, Nombre: #Nombre}
#SigmaMSg: #SigmaNOM & {Genre: "M", Nombre: "Sg"}
#SigmaMPl: #SigmaNOM & {Genre: "M", Nombre: "Pl"}
#SigmaFSg: #SigmaNOM & {Genre: "F", Nombre: "Sg"}
#SigmaFPl: #SigmaNOM & {Genre: "F", Nombre: "Pl"}

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

#FormeNOM: #Forme & {forme: pos: "NOM"}

#FormeNOMMSg: #FormeNOM & {forme: sigma: #SigmaMSg}
#FormeNOMMPl: #FormeNOM & {forme: sigma: #SigmaMPl}
#FormeNOMFSg: #FormeNOM & {forme: sigma: #SigmaFSg}
#FormeNOMFPl: #FormeNOM & {forme: sigma: #SigmaFPl}

#FormeVER: {#Forme, pos: "VER"}

#FormePRS3SgM: {#FormeVER, forme: sigma: #SigmaPRS3SgM}
#FormePRS3SgF: {#FormeVER, forme: sigma: #SigmaPRS3SgF}
#FormePRS3SgN: {#FormeVER, forme: sigma: #SigmaPRS3SgN}
#FormePRS3DuM: {#FormeVER, forme: sigma: #SigmaPRS3DuM}
#FormePRS3DuF: {#FormeVER, forme: sigma: #SigmaPRS3DuF}
#FormePRS3DuN: {#FormeVER, forme: sigma: #SigmaPRS3DuN}
#FormePRS3PlM: {#FormeVER, forme: sigma: #SigmaPRS3PlM}
#FormePRS3PlF: {#FormeVER, forme: sigma: #SigmaPRS3PlF}
#FormePRS3PlN: {#FormeVER, forme: sigma: #SigmaPRS3PlN}
#FormePST3SgM: {#FormeVER, forme: sigma: #SigmaPST3SgM}
#FormePST3SgF: {#FormeVER, forme: sigma: #SigmaPST3SgF}
#FormePST3SgN: {#FormeVER, forme: sigma: #SigmaPST3SgN}
#FormePST3DuM: {#FormeVER, forme: sigma: #SigmaPST3DuM}
#FormePST3DuF: {#FormeVER, forme: sigma: #SigmaPST3DuF}
#FormePST3DuN: {#FormeVER, forme: sigma: #SigmaPST3DuN}
#FormePST3PlM: {#FormeVER, forme: sigma: #SigmaPST3PlM}
#FormePST3PlF: {#FormeVER, forme: sigma: #SigmaPST3PlF}
#FormePST3PlN: {#FormeVER, forme: sigma: #SigmaPST3PlN}

#FormeADJ: #Forme & {forme: pos: "ADJ"}

//#FormeDET: {#Forme, pos: "DET"}
#FormePREP: {#Forme, forme: pos: "PREP"}

#LexemeNOM: #Lexeme & {
	pos: "NOM"
	morphemes: [
		#Prefix & {sigma: {Nombre: "Sg"}, _sigma: {Nombre: "Sg"}, rule: "so+X"} |
		#Prefix & {sigma: {Nombre: "Du"}, _sigma: {Nombre: "Du"}, rule: "ti+X"} |
		#Prefix & {sigma: {Nombre: "Pl"}, _sigma: {Nombre: "Pl"}, rule: "Na+X"},
	]}
#LexemeVER: {
	#Lexeme
	pos: "VER"
	morphemes: [
		{#Suffix, _sigma: {Temps: "PRS"}, sigma: {Temps: "PRS"}, rule: "X+z"} |
		{#Suffix, _sigma: {Temps: "PST"}, sigma: {Temps: "PST"}, rule: "X+j"},
		{#Suffix, _sigma: {Pers:  "3Sg"}, sigma: {Pers:  "3Sg"}, rule: "X+ev"} |
		{#Suffix, _sigma: {Pers: "3Du"}, sigma: {Pers: "3Du"}, rule: "X+ub"} |
		{#Suffix, _sigma: {Pers:  "3Pl"}, sigma: {Pers: "3Pl"}, rule: "X+ot"},
		{#Suffix, _sigma: {Genre: "M"}, sigma: {Genre:  "M"}, rule:   "X+a"} |
		{#Suffix, _sigma: {Genre: "F"}, sigma: {Genre: "F"}, rule: "X+i"} |
		{#Suffix, _sigma: {Genre: "N"}, sigma: {Genre: "N"}, rule: "X+e"},
	]}
#LexemeADJ: {#Lexeme, pos: "ADJ",
	morphemes: [
		#Suffix & {sigma: {Nombre: "Sg"}, rule: "X+b"} |
		#Suffix & {_sigma: {Nombre: "Du"}, sigma: {Nombre: "Du"}, rule: "X+s"} |
		#Suffix & {_sigma: {Nombre: "Pl"}, sigma: {Nombre: "Pl"}, rule: "X+w"},
		#Suffix & {_sigma: {Genre:  "M"}, sigma: {Genre:   "M"}, rule:  "X+ek"} |
		#Suffix & {_sigma: {Genre: "F"}, sigma: {Genre: "F"}, rule: "X+as"} |
		#Suffix & {_sigma: {Genre: "N"}, sigma: {Genre: "N"}, rule: "X+u"},
	]
}

#LexemeDET: {
	#Lexeme
	pos: "DET"
	morphemes: [
		#Suffix & {sigma: {Genre: "M"}, _sigma: {Genre: "M"}, rule: "X+o"} |
		#Suffix & {sigma: {Genre: "F"}, _sigma: {Genre: "F"}, rule: "X+a"} |
		#Suffix & {sigma: {Genre:  "N"}, _sigma: {Genre:   "N"}, rule:  "X+e"},
		#Suffix & {sigma: {Nombre: "Sg"}, _sigma: {Nombre: "Sg"}, rule: "X+n"} |
		#Suffix & {sigma: {Nombre: "Du"}, _sigma: {Nombre: "Du"}, rule: "X+ri"} |
		#Suffix & {sigma: {Nombre: "Pl"}, _sigma: {Nombre: "Pl"}, rule: "X+p"}
	]
}

#LexemePREP: {
	#Lexeme
	pos: "PREP"
}

//#Forme: {
// #Forme
// _lexeme: #Lexeme
// morphemes: [#Morpheme & {stem: _lexeme.stems}, ...]
//}

#FormeNOM: {
	#FormeNOM
	forme: {
		_lexeme:   #LexemeNOM
		sigma: #Sigma
		morphemes: [#Morpheme] & [for m in #LexemeNOM.morphemes {m & {sigma: #FormeNOM.forme.sigma}}]
		realisation: morphemes[len(morphemes)-1].realisation
	}
}

#FormePREP: {
	#FormePREP
	forme: {
		_lexeme: #LexemePREP
		morphemes: [#Identity] & [for m in #LexemePREP.morphemes {m & {sigma: #FormePREP.forme.sigma}}]
		realisation: morphemes[len(morphemes)-1].realisation
	}
}

#FormeADJ: #FormeADJ & {
	forme: {
			_lexeme: #LexemeADJ
			morphemes: [ #Morpheme, #Morpheme & {stem: morphemes[0].realisation}, ]
	}
}

#FormeVER: #FormeVER & {
	forme: {
			_lexeme: #LexemeVER
			morphemes: [
				#Morpheme,
				#Morpheme & {stem: morphemes[0].realisation},
				#Morpheme & {stem: morphemes[1].realisation},
			] & [for m in #LexemeVER.morphemes {m & {sigma: #FormeVER.forme.sigma}}]
			realisation: morphemes[len(morphemes)-1].realisation
	}
}

//c: #FormePRS3SgM & {_lexeme: stems: "dila"}
//c: #FormePRS3SgM & {_lexeme: stems: "dila", morphemes: [for m in _lexeme.morphemes {m&{sigma: c.sigma}}]}
//c: {
// #FormePREP
// _lexeme: {stems: "NiSaw"},
// morphemes: [for m in _lexeme.morphemes {m & {sigma: c.sigma}}]
//}

//#dila: {#LexemeVER, stems: "dila", morphemes: [for m in #dila._lexeme.morphemes {m&{sigma: #dila.sigma}}]}

//_lexeme: #LexemeVER & {stems: "dila"}

//FormePRS3SgM: {#FormePRS3SgM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: #FormePRS3SgM.sigma}}]}
//FormePRS3SgF: {#FormePRS3SgF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3SgF.sigma}}]}
//FormePRS3SgN: {#FormePRS3SgN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3SgN.sigma}}]}
//FormePRS3DuM: {#FormePRS3DuM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3DuM.sigma}}]}
//FormePRS3DuF: {#FormePRS3DuF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3DuF.sigma}}]}
//FormePRS3DuN: {#FormePRS3DuN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3DuN.sigma}}]}
//FormePRS3PlM: {#FormePRS3PlM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3PlM.sigma}}]}
//FormePRS3PlF: {#FormePRS3PlF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3PlF.sigma}}]}
//FormePRS3PlN: {#FormePRS3PlN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePRS3PlN.sigma}}]}
//FormePST3SgM: {#FormePST3SgM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3SgM.sigma}}]}
//FormePST3SgF: {#FormePST3SgF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3SgF.sigma}}]}
//FormePST3SgN: {#FormePST3SgN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3SgN.sigma}}]}
//FormePST3DuM: {#FormePST3DuM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3DuM.sigma}}]}
//FormePST3DuF: {#FormePST3DuF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3DuF.sigma}}]}
//FormePST3DuN: {#FormePST3DuN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3DuN.sigma}}]}
//FormePST3PlM: {#FormePST3PlM, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3PlM.sigma}}]}
//FormePST3PlF: {#FormePST3PlF, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3PlF.sigma}}]}
//FormePST3PlN: {#FormePST3PlN, _lexeme: stems: "dila", morphemes: [ for m in _lexeme.morphemes {m & {_sigma: FormePST3PlN.sigma}}]}
//FormePST3PlN: #FormePST3PlN & {
// _lexeme: stems: "dila"
//}
//f: #Forme & {
// _lexeme: #LexemeNOM & {pos: "NOM", stems: "banane"},
// sigma: {Genre: "M", Nombre: "Sg"}
// morphemes: [ for m in _lexeme.morphemes {m & {sigma: f.sigma}}]
//}

//m: #FormeNOM & {
// _lexeme: {stems: "banane"},
// sigma: {Nombre: "Pl"},
// morphemes: [ for x in _lexeme.morphemes {x & {sigma: m.sigma}}]
//}
//
//mmm: #FormeNOMMSg & {
//	forme: _lexeme: stems: "toto"
//}

//#FormesNOM: {
//    FormeNOMMSg: (#FormeNOMMSg | #FormeNOMMPl | #FormeNOMFSg | #FormeNOMFPl) & {forme: _lexeme: {stems: "toto", sigma: Genre: "M"}}
//    FormeNOMMPl: (#FormeNOMMSg | #FormeNOMMPl | #FormeNOMFSg | #FormeNOMFPl) & {forme: _lexeme: {stems: "toto", sigma: Genre: "M"}}
//}


//f: (#FormeNOMMSg | #FormeNOMMPl) & {forme: _lexeme: {stems: "toto", sigma: Genre: "M"}}
//g: [
//	for forme in [#FormeNOMMSg, #FormeNOMMPl, #FormeNOMFSg, #FormeNOMFPl]
//	let yy=(forme & {forme: _lexeme: {stems: "toto", sigma: Genre: "M"}}) != _|_
//	if yy == true
//	{forme & {forme: _lexeme: {stems: "toto", sigma: Genre: "M"}}}
//]

//dila: or([
//	for forme in [ #FormePRS3SgM, #FormePRS3SgF, #FormePRS3SgN, #FormePRS3DuM, #FormePRS3DuF, #FormePRS3DuN, #FormePRS3PlM, #FormePRS3PlF, #FormePRS3PlN, #FormePST3SgM, #FormePST3SgF, #FormePST3SgN, #FormePST3DuM, #FormePST3DuF, #FormePST3DuN, #FormePST3PlM, #FormePST3PlF, #FormePST3PlN]
//	let toto=forme & {forme: _lexeme: {stems: "dila"}}
//	let tmp=toto != _|_
//	if tmp == true
//	{toto}
//])

m: #FormeADJ & {forme: {_lexeme: stems: "meN", sigma: {Genre: "N", Nombre: "Sg"}}}
n: #FormeNOM & {forme: {_lexeme: {stems: "minet", sigma: {Genre: "N"}}, sigma: {Nombre: "Sg"}}}

//j: [
//	for forme in []
//]
//#FormesNOM

o: #FormePREP & {forme: _lexeme: stems: "kal"}

//
//toto: {
//    #FormesNOM & {_lexeme: {stems: "toto", sigma: {Genre: "M"}}}
//}
