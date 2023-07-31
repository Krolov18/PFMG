package stems

import (
	l "pfmg.com/pkg/schemas:literals"
)

#RecursiveInherence: [string]: =~"^[\(l.#alphaCase)]+(?:,[\(l.#alphaCase)]+)*(?:\\-[\(l.#lowerAlphaNumCase)]+(?:\\.[\(l.#lowerAlphaNumCase)]+)*)?$" | #RecursiveInherence
#Stems: [=~"^[\(l.#upperCase)]+$"]: #RecursiveInherence
