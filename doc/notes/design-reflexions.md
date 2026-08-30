# Reflections on building the Kalabatiste

## How to rewrite code to make it more flexible

Reading and debugging the initial code.

### Object-oriented

The base code was intended to be object-oriented. After digging into it, some classes
turned out to be functions and others were data structures. The approach shifted:
in Python 3.7, data structures were modeled as dataclasses (a rough equivalent of C
structs). Key elements and their relationships had to be identified before continuing.

### Functional

The design then moved toward a functional style. Structures (`Lexeme`, `Forme`,
`Morpheme`) could be "realized". A `realise` function dispatches on the type of its
argument to realize the data structure.

### Neither one nor the other?

## Rewrite focused on input files

Once the code was stable, functional, and tested as much as possible, the goal became:
users of this package should not need to touch the code except as a last resort. The
real entry point is the input files.

Users edit five files: `Gloses`, `Blocks`, `Stems`, `MorphoSyntax`, and `Phonology`.

- **Gloses** — paradigm cells (e.g. a noun varying in gender and number with two values
  each yields 2 × 2 = 4 cells).
- **Blocks** — realization rules ("morphemes"), e.g. `N -> [[nombre=pl: X+s]]` suffixes
  a noun with `s` only in the plural.
- **Stems** — lexemes: syntactic category, thematic set, inherent sigma, and translation.

## Discovery of JSON schemas

_Content to be completed._

## From JSON Schema to CUE

_Content to be completed._
