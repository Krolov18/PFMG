//contractions:
//  au: [ "à", "le" ]
//  aux: [ "à", "les" ]
//  du: [ "de", "le" ]
//  Des: [ "de", "les" ]
//  Katisha: ["", "Katisha"]
//  Katishas: ["", "Katishas"]
//start: "NP"
//syntagmes:
//  NP:
//    - [ "DET/?", "ADJ/?", "ADJ/?", "N", "ADJ/?" ]
//    - [ "DET2", "NNP" ]
//accords:
//  NP:
//    - [ { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dGenre: "*", dNombre: "*" } ]
//    - [ { sGenre: "*", sNombre: "*", dNombre: "*", dCas: "*" },
//        { sGenre: "*", sNombre: "*", dNombre: "*", dCas: "*" } ]
//percolations:
//  NP:
//    - { sGenre: "*", sNombre: "*",
//        dGenre: "*", dNombre: "*", dCas: "*" }
//    - { sGenre: "*", sNombre: "*",
//        dGenre: "*", dNombre: "*", dCas: "*" }
//traductions:
//  NP:
//    - [ 0, 3, 1, 2, 4 ]
//    - [ 0, 1 ]

import (
	""
)

contractions: {

	au: ["à", "le"]
	aux: ["à", "les"], du: ["de", "le"], Des: ["de", "les"], Katisha: ["", "Katisha"], Katishas: ["", "Katishas"]
}, start:
	"NP", source: {
	syntagmes: NP: [ ["DET/?", "ADJ/?", "N", "ADJ/?"], ["DET/?", "'deux'", "N/?"],
	], accords: {

		RTT: [ [{
			toto: "z"
		}]]
		NP: [ [{
			// Genre, Nombre
			Genre: "*", Nombre: "*"
		}, {
			Genre: "*", Nombre: "*"
		}, {
			Genre: "*", Nombre: "*"
		}, {
			Genre: "*", Nombre: "*"
		}], [{
			Genre: "*", Nombre: "Pl"
		}, {
			Genre: "*", Nombre: "Pl"
		}, {
			Genre: "", Nombre: "Pl"
		}],
		]
	}, percolations: {
		// Genre, Nombre
		NP: [ {
			Genre: "*", Nombre: "*"
		}]
	}, traductions: [ [0]]
}, destination: {
	syntagmes: NP: [ ["DET/?", "ADJ/?", "ADJ/?", "N"], ["DET/?", "N"],
	], accords: NP: [ [{
		Genre: "*", Nombre: "*", Cas: "*"
	}, {
		Genre: "*", Nombre: "*"
	}, {
		Genre: "*", Nombre: "*"
	}, {
		Genre: "*", Nombre: "*", Cas: "*"
	}], [{
		Genre: "*", Nombre: "Du", Cas: "*"
	}, {
		Genre: "*", Nombre: "Du", Cas: "*"
	}],
	], percolations: {
		// Genre, Nombre, Cas
		NP: [ {
			Genre: "*", Nombre: "*", Cas: "*"
		}]
	}
}
