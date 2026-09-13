package phonology

// A simple character/string rewrite table.
#Mapping: {
	[string]: string
}

// Phonological data. The five fields below are the ones the runtime loader
// (pfmg.lexique.phonology.Phonology) reads; the schema stays open so extended
// fields (translations, gabarits, nom_classe, syllabes, ...) are also allowed.
#Phonology: {
	consonnes!:  string
	voyelles!:   string
	apophonies!: #Mapping
	derives!:    #Mapping
	mutations!:  #Mapping
	...
}

#Phonology
