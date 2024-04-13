import (
	"github.com/kalaba/declarations"
)

//NNP:
//  A:
//    katiSa: Katisha-1.F
//  B:
//    nikol: Nicole-1.F
//  D:
//    nabil: Nabil-1.M
//
//

katiSa: {pos: "NNP", sigma: Cf: "A", traduction: Katisha: sigma: {Cf: 1, Genre: "f"}}

katiSa: declarations.#Lexeme & {
	pos: "NNP"
	sigma: {
		Cf: "A"
	}
	traduction: {
		Katisha: {
			sigma: {
				Cf: "1"
				Genre: "f"
			}
		}
	}
}
nikol: declarations.#Lexeme & {
	pos: "NNP"
	sigma: {
		Cf: "B"
	}
	traduction: {
		Nicole: {
			sigma: {
				Cf: "1"
				Genre: "f"
			}
		}
	}
}
nabil: declarations.#Lexeme & {
	pos: "NNP"
	sigma: {
		Cf: "A"
	}
	traduction: {
		Nabil: {
			sigma: {
				Cf: "1"
				Genre: "m"
			}
		}
	}
}
