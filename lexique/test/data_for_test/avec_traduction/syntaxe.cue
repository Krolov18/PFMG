import (
	r "regexp"
	l "list"
	s "strings"
)

#Category:  =~"^(n|v|a|det|prep)$"
#Attribute: =~"^(Genre|Nombre|Temps|Pers)$"
#Value:     =~"^(3(Sg|Du|Pl)|P(RS|ST)|Sg|Du|Pl|[MFN])$"

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
//
//#Prefix: {
//	#Morpheme
//	stem:          string
//	rule:          string & =~"^[a-zA-Z]+\\+X$"
//	realisation:   r.FindSubmatch("([a-zA-Z]+)\\+X", rule)[1] + stem
//	//           decoupage: r.FindSubmatch("([a-z]+)\\+X", rule)[1] + "-" + stem
//}
//
//#Suffix: {
//	#Morpheme
//	stem:          string
//	rule:          string & =~"^X\\+[a-zA-Z]+$"
//	realisation:   stem + r.FindSubmatch("X\\+([a-zA-Z]+)", rule)[1]
//	//           decoupage: stem + "-" + r.FindSubmatch("([a-z]+)\\+X", rule)[1]
//}
//
//#Circumfix: {
//	#Morpheme
//	stem:         string
//	rule:         string & =~"^[a-zA-Z]+\\+X\\+[a-zA-Z]+$"
//	_affixes:     [string, string] & l.Slice(r.FindSubmatch("([a-zA-Z]+)\\+X\\+([a-zA-Z]+)", rule), 1, 3)
//	realisation:  _affixes[0] + stem + _affixes[1]
//	//           decoupage: _affixes[0] + "-" + stem + "-" + _affixes[1]
//}
//
//#Identity: {
//	#Morpheme
//	stem:         string
//	realisation:  stem
//}
//
//FormeDET: leDET | laDET
//
//laDET: {
//	orth: "la"
//	pos:  "det"
//	sigma: {
//		Genre:  "f"
//		Nombre: "sg"
//	}
//}
//
//leDET: {
//	orth: "le"
//	pos:  "det"
//	sigma: {
//		Genre:  "m"
//		Nombre: "sg"
//	}
//}
//
//dePREP: {
//	orth: "de"
//	pos:  "prep"
//}
//
//FormePREP: dePREP
//
//chatN: {
//	orth: "chat"
//	pos:  "n"
//	sigma: {
//		Genre:  "m"
//		Nombre: "sg"
//	}
//}
//
//chatteN: {
//	orth: "chatte"
//	pos:  "n"
//	sigma: {
//		Genre:  "f"
//		Nombre: "sg"
//	}
//}
//
//FormeN: chatN | chatteN
//
//mangerV: {
//	orth: "mange"
//	pos:  "v"
//	sigma: {
//		Personne: "3sg"
//		Temps:    "prs"
//		Type: "vt"
//	}
//}
//
//np_rule: {
//	orth:  l.FlattenN([ for a in args {a.orth}], 1)
//	pos:   "n"
//	sigma: and([ for s in args {s.sigma}])
//	args: [_, ...]
//}
//
//np_rule_1: np_rule & {
//	//    orth:    l.FlattenN([for a in args {a.orth}], 1)
//	pos: args[1].pos
//	//    sigma:   and([for s in args {s.sigma}])
//	args: [{pos: "det"}, {pos: "n"}]
//	args: [{sigma: sigma}, {sigma: sigma}]
//}
//
//np_rule_2: {
//	orth:  l.FlattenN([ for a in args {a.orth}], 1)
//	pos:   args[1].pos
//	sigma: and([ for s in args {s.sigma}])
//	args: [{pos: "n"}, {pos: "prep"}]
//	args: [{sigma: sigma}, {sigma: sigma}]
//}
//
//prep_rule_1: {
//	orth: l.FlattenN([ for a in args {a.orth}], 1)
//	pos:  args[0].pos
//	sigma: {}
//	args: [{pos: "prep"}, {pos: "n"}]
//}
//
////le_chat:    np_rule_1 & {args: [FormeDET & {orth: "le"}, FormeN & {orth: "chat"}]}
//la_chatte: np_rule_1 & {args: [FormeDET & {orth: "la"}, FormeN & {orth: "chatte"}]}
////la_chatte:  np_rule_1 & {args: [FormeDET, FormeN]}
//de_la_chatte: prep_rule_1 & {args: [FormePREP, la_chatte]}
//
//la_chatte_de_la_chatte: np_rule_2 & {args: [la_chatte, de_la_chatte]}
////le_chat: np_rule_1 & {args: [{orth: "le"}, {orth: "chat"}]}
//
//s_rule: {
//	orth: l.FlattenN([ for a in args {a.orth}], 1)
//	pos:  "s"
//	sigma: {}
//	args: [
//		{pos: "n", sigma: Cas: "erg"},
//		{pos: "v", sigma: Type: "vt"},
//		{pos: "n", sigma: Cas: "abs"},
//	]
//}

#Phrase: {
	realisation: string
	pos: string
	sigma: #Sigma
	args: [...] &[_, ...]
//	args: [...#Forme|#Phrase] & [_, ...#Forme|#Phrase]
	input: [...string] & [_, ...string]
}


#sign: {
	orth: string
	pos: #Category
	sigma: #Sigma
}

#lexsign: #sign & {}

#lexeme: {
	#lexsign,
	paradigm: [...{#Morpheme, ...}]
}

#synsign: {
	#sign,
	input?: [...string]
}

#word: {
	#lexsign,
	#synsign,
	morphemes: [...{#Morpheme, ...}]
}

#phrase: {
	#synsign,
	args: [...{#synsign, ...}] & [_, ...{#synsign, ...}]
	input: [_, ...]
}

#hfp: #phrase & {
	pos: args[0].pos
	args: [{pos: pos}, ...]
}

#phraseN: #hfp & {
	args: [{pos: "n"}, ...]
}

#phraseN1: #phraseN & {
	sigma: and([for s in args {s.sigma}])
	args: [
		{#word, orth: input[1]},
		{#word, pos: "det", orth: input[0]}
	]
	input: [args[1].orth, args[0].orth]
}

#phraseP: #hfp & {
	pos: "prep"
	args: [{#word, pos: "prep"}, ...]
}

#phraseP1: #phraseP & {
	args: [
		#word & {orth: #phraseP1.input[0]},
		#phraseN1 & {input: l.Slice(#phraseP1.input, 1, len(#phraseP1.input))}
	]
	input: [_, _, _]
}

g: #hfp & {pos: "n"}
