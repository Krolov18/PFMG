import l "list"
import s "strings"

#sign: {
	orth:  string
	pos:   string
	sigma: #sigma
}

//#valence: {
// subj:  [...#synsign] | *[]
// spr:   [...#synsign] | *[]
// comps: [...#synsign] | *[]
// mod:   [...#synsign] | *[]
//}

#sigma: {
	Genre?:  =~"^[mf]$"
	Nombre?: =~"^(?:sg|pl)$"
}

#synsign: {#sign}

#word: #synsign

#phrase: {
	#synsign
	orth: s.Join([ for arg in args {arg.orth}], " ")
	args: [...#synsign] & [_, ...#synsign]
}

#det:  #word & {pos: "det"}
#noun: #word & {pos: "noun"}
#prep: #word & {pos: "prep"}
#verb: #word & {pos: "verb"}

#le:  #det & {orth: "le", sigma: {Genre:   "m", Nombre: "sg"}}
#la:  #det & {orth: "la", sigma: {Genre:   "f", Nombre: "sg"}}
#les: #det & {orth: "les", sigma: {Nombre: "pl"}}

#chat:    #noun & {orth: "chat", sigma: {Genre:    "m", Nombre: "sg"}}
#chats:   #noun & {orth: "chats", sigma: {Genre:   "m", Nombre: "pl"}}
#chatte:  #noun & {orth: "chatte", sigma: {Genre:  "f", Nombre: "sg"}}
#chattes: #noun & {orth: "chattes", sigma: {Genre: "f", Nombre: "pl"}}

#dans: #prep & {orth: "dans"}
#de:   #prep & {orth: "de"}
#à:    #prep & {orth: "à"}

#dort:  #verb & {orth: "dort", sigma: {Nombre:  "sg"}}
#mange: #verb & {orth: "mange", sigma: {Nombre: "sg"}}
#boit:  #verb & {orth: "boit", sigma: {Nombre:  "sg"}}

#n1: #phrase & {
	pos: "noun"
	args: [
		(#le | #la | #les),
		(#chat | #chats | #chatte | #chattes),
	]
	sigma: and([ for arg in args {arg.sigma}])
}
#n2: #phrase & {
	pos:   "noun"
	args:  [(#le | #la | #les), (#chat | #chats | #chatte | #chattes)] + #p.args
	sigma: and([ for arg in args {arg.sigma}])
}
#n: #n1 | #n2

#p1: #phrase & {
	pos:  "prep"
	args: [(#dans | #de | #à)] + #n.args
	sigma: {}
}
#p: #p1

#se1: #phrase & {
	pos:  "verb"
	args: #n.args + [(#dort | #mange | #boit)]
	sigma: {}
}
#se2: #phrase & {
	pos:  "verb"
	args: #n.args + [(#dort | #mange | #boit)] + #p.args
	sigma: {}}
#se: #se1 | #se2

le_chat:                   #n & {args: [{orth:  "le"}, {orth: "chat"}]}
de_la_chatte:              #p & {args: [{orth:  "de"}, {orth: "le"}, {orth:   "chat"}]}
le_chat_de_la_chatte:      #n & {args: [{orth:  "le"}, {orth: "chat"}, {orth: "de"}, {orth: "le"}, {orth: "chat"}]}
le_chat_dort:              #se & {args: [{orth: "le"}, {orth: "chat"}, {orth: "dort"}]}
le_chat_dort_dans_le_chat: #se & {args: [{orth: "le"}, {orth: "chat"}, {orth: "dort"}, {orth: "dans"}, {orth: "le"}, {orth: "chat"}]}
