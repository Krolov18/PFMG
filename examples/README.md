# Examples

This directory contains sample Kalaba grammars and a notebook demonstrating parsing
with morphological and syntactic ambiguity.

## Prerequisites

Install project dependencies from the repository root:

```bash
uv sync --all-groups
```

Run commands from this directory (`examples/`) so that relative paths such as `./data`
resolve correctly.

## Grammar directories

Each subdirectory (`data/`, `data2/`, `data3/`, `data4/`) is a complete grammar: the five
required YAML files (`Gloses.yaml`, `Blocks.yaml`, `Stems.yaml`, `Phonology.yaml`,
`MorphoSyntax.yaml`).

| Directory | Purpose |
|-----------|---------|
| `data/` | Noun phrases with an optional adjective, prenominal or postnominal: `D NOM`, `D ADJ NOM`, `D NOM ADJ` (`"des petites autruches"` → Kalaba forms). |
| `data2/` | Variant with the quoted numeral literal `'deux'` and an explicit dual number. Differs in `Blocks.yaml`, `Stems.yaml`, and `MorphoSyntax.yaml`. |
| `data4/` | Templatic language: nouns are consonantal roots poured into a vocalic scheme, determiners are circumfixes, 4 genders, 5 numbers, 6 cases, case assigned by valence. See below. |
| `data3/` | Full sentences (`"les petits enfants mangent deux autruches jaunes"`). Adds verbs with a lexical valence (`V`, feature `Val`), prepositions (`P`) and numerals (`NUM`), and rules that call each other: `S` → `NP` … `PP` → `NP`. |

`Phonology.yaml` is identical in all four directories.

### What `data3/` demonstrates

* **Valence in the lexicon.** Each verb carries `Val=intr|tdir|tind|ditr`; a clause
  rule pins the value it accepts, so `"les enfants mangent"` (transitive verb, no
  object) has no parse.
* **Per-constituent agreement.** A rule's agreement string carries one `;`-separated
  segment per constituent: `"Nombre;Nombre,Val=tdir;"` makes the subject and the verb
  agree in number, requires a direct transitive verb, and leaves the object free.
* **Word order.** French is SVO, Kalaba is SOV; the French preposition becomes a
  Kalaba postposition.
* **Nested rules.** `S` refers to `NP` and `PP`, which refer to `NP` again. The
  `translation` feature of a rule collects those of its constituents, so the parser
  flattens it before joining the words.

## Jupyter notebook

[`execution_grammaire.ipynb`](execution_grammaire.ipynb) goes from noun phrases of
growing length (`des garçons`, then `des petites autruches`) to full sentences, and
shows how agreement keeps the remaining ambiguity down to the dual/plural
alternation. It calls `parsing_action` with the `data/` grammar:

```python
from pfmg.parsing.main.actions import parsing_action

parsing_action(
    {
        "data": "des garçons",
        "path": "./data",
        "keep": "all",
    }
)
```

then reuses a single `KParser` for the longer phrases:

```python
from pfmg.parsing.parser import KParser

parser = KParser.from_yaml("./data")
parser.parse(data="des petites autruches", keep="all")
# ['siprug kizin zij', 'sipru kizi zi']
```

and finally moves to `data3/` for full sentences:

```python
parser3 = KParser.from_yaml("./data3")
parser3.parse(data="les petits enfants mangent deux autruches jaunes", keep="all")
# ['telaazi kizerak rek sipruazi gelirak duz nagetak',
#  'telag kizen rej sipruazi gelirak duz nagetan']
```

Launch Jupyter from this directory:

```bash
cd examples
uv run jupyter notebook execution_grammaire.ipynb
```

(`jupyter` is not a project dependency; install it in your environment if needed.)

### What `data4/` demonstrates

A language built on the opposite principles from `data/`–`data3/`.

* **Templatic nouns.** A noun root is three consonants written `C C V C`
  (`ktub`, `gzem`); the `Gabarit` rules of `Blocks.yaml` pour it into a vocalic
  scheme that carries the inflection. First vowel = number (`a` sg, `o` dual,
  `i` plural, `u` trial, `e` quadral), second vowel = case (`i` nom, `u` acc,
  `e` dat, `o` erg, `a` abs, `ai` gen). So `ktub` gives `katib`, `kotab`,
  `kitob`, `ketaib`… — 30 schemes in all.
* **No determiner word.** The French determiner survives only as a circumfix on
  the noun: `ta-…-an` definite, `mu-…-un` indefinite, `si-…-in` demonstrative.
  The suffix consonant marks the noun's inherent gender (`-n` g1, `-l` g2,
  `-r` g3, `-s` g4), so `le livre` is `takataban`.
* **Case assigned by valence.** Intransitive: subject absolutive. Transitive:
  subject ergative, object accusative. Ditransitive: subject nominative, object
  absolutive, second object dative. The verb agrees on its subject's case, and
  the French `à` and `de` disappear — the dative and the genitive replace them.
* **Postpositions.** The French preposition moves to the right of the noun
  phrase, which it governs in the absolutive. It is invariable. Adpositions
  that come in opposing pairs (`pour`/`contre`, `sur`/`sous`) have a
  palindromic form: `talat`, `nusun`, `mirim`, `dolod`.
* **Peripheral circumstantials.** A circumstantial complement never sits inside
  the clause; with two of them, they frame it.
* **The numeral is a morpheme, not a word.** Number is inflectional:
  `takotaban` alone means "two books". The invented language therefore has no
  numeral at all. French does, and it uses them to say what its plural leaves
  open, so `deux`, `trois` and `quatre` exist only on the source side: they fix
  the source-only `Compte` feature, which the noun's alignments turn into a
  number (`deux` → dual, `trois` → trial, `quatre` → quadral). Like the
  determiner, the numeral leaves nothing behind — it narrows the French input,
  it does not add a word.

```
le livre dort                              → takataban fanzkot
la femme voit le chien                     → tagazomar tatasukas sepkket
la femme donne un livre à un enfant        → tagazimar mukatabun mumaredun mizdkat
le livre de la femme dort                  → takataban tagazaimar fanzkot
pour la femme le livre dort sous un arbre  → tagazamar talat takataban fanzkot mupanakul dolod
les deux femmes donnent
  les quatre livres à la rivière           → tagozimar taketaban tadaretar mizdkan
```

A bare French plural maps to four invented numbers, so `les livres dorment`
yields four translations — `takotaban fanzkon`, `takitaban fanzkol`,
`takutaban fanzkom`, `taketaban fanzkoz`. A numeral keeps exactly one of them,
without lengthening it: `les trois livres dorment` → `takutaban fanzkom`.

## Benchmark corpus

[`phrases_data3.txt`](phrases_data3.txt) holds 50 French sentences the `data3/`
grammar accepts, 3 to 11 words long, rotating through the four valences. Blank lines
and `#` lines are ignored.

`scripts/bench_parsing.py` parses it and reports how the cost scales:

```bash
uv run python scripts/bench_parsing.py examples/data3 examples/phrases_data3.txt
```

```
  keep  phrases      total   par phrase   phrases/s   sorties
 first       10    324.4 ms     32.44 ms          31        10
 first       50   1939.9 ms     38.80 ms          26        50
   all       10    371.2 ms     37.12 ms          27        14
   all       50   2242.1 ms     44.84 ms          22        81
```

Cost is linear in the number of sentences — each one is an independent chart parse —
and grows with sentence length (~26 ms at 3 words, ~70 ms at 11). `sorties` counts the
translations produced: with `keep="all"` a sentence may have several, one per
dual/plural reading.

The corpus is written for the `data3/` lexicon, which knows neither elision nor
contracted articles: it therefore avoids `la autruche`, `à le garçon` and `de les
maisons`. Some sentences are semantically odd (`deux cuisines mangent la banane`) —
the grammar constrains syntax and agreement, not meaning.

## CLI equivalents

From the repository root:

```bash
# Parse with the default grammar (data/)
uv run python -m pfmg.parsing.main parsing examples/data "des garçons" -k all

# List lexical forms from the grammar
uv run python -m pfmg.lexique.main.main lexicon examples/data
```

Swap `examples/data` for `examples/data2` or `examples/data3` to use the other
grammars:

```bash
uv run python -m pfmg.parsing.main parsing examples/data3 "la maman donne une banane à la fille"
```
