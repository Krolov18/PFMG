#Lexeme: {
	pos: #Category
	stems: [...string] & [_,...string]
	sigma: #Sigma
	traduction?: #Lexeme
	formes: [...#Forme] & [_,...#Forme]
}

#Forme: {
	pos: #Category
	stem: string
	sigma: #Sigma
	morphemes: [...#Morpheme] & [_, ...#Morpheme]
	traduction?: #Forme
	realisation: string
	glose?: string
	decoupage?: string
}

#FormeN: {
	#Forme,
	pos: "N"
	sigma: #sigmaN
	traduction?: #FormeN
}

// définition générée lors de la lecture de Gloses.yml
#Sigma: {}

// définition aussi géénrée lors de la lecture de Gloses.yml
#Category: string

#Morpheme: {
	sigma: #Sigma
	rule: #Rule
}





#LexemeN: {
	#Lexeme,
	pos: "N"
	stems: [...string] & [_,...string]
	sigma: #SigmaN
	traduction?: #LexemeN
	formes: [...#FormeN] & [_, ...#FormeN]
}

#LexemeNNP: {
    pos: "NNP"
    stems: [...string] & [_,...string]
    sigma: #SigmaNNP
    traduction?: #LexemeNNP
}

#Sigma: {
    genre?: string
    nombre?: string
    cf?: string
}

#SigmaNNP: {
	#Sigma,
	cf: "1"
}

nikol: {
    #LexemeNNP
    stems: ["nikol"]
    sigma: {genre: "b"}
    traduction: {
    		#LexemeNNP,
        stems: ["Nicole"]
        sigma: {
            #SigmaNNP
            genre: "F"
        }
    }
}

//claudio: {#LexemeNNP, traduction: pos: "RRR"}

// Gloses définit les formes
// Blocks définit la structure morphémique des formes
// Stems définit les lexèmes

// Comment sélectionner les bons morphèmes ?
// Comment sélectionner les bons stems ?
