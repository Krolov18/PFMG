// Development fixture: a minimal grammar unified with the MorphoSyntax schema.
import m "pfmg.com/pkg/schemas:morphosyntax"

#Francais: m.#MorphoSyntax & {
	Start: "NP"
	NP: {
		Source: {
			phrases: [["D", "NOM"]]
			agreements: ["Genre,Nombre"]
			percolations: ["Genre,Nombre"]
			translations: [[1, 0]]
		}
		Destination: {
			phrases: [["NOM", "D"]]
			agreements: ["Genre,Nombre"]
			percolations: ["Nombre"]
		}
	}
}

#Francais
