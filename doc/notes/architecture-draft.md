# Kalabatiste construction (architecture draft)

_Draft converted from the original LaTeX notes (March 2022)._

## Introduction

This document traces the rewrite of the Kalaba project. The original code had become
too complex to extend. The rewrite applies design patterns such as abstract factory.

**Kalaba** is a lexical grammar that recognizes, generates, and translates a source
language into a target language. In practice the source is an invented language and
the target is French.

## Code (legacy)

### Architecture

Kalaba is a use case of Stump's Paradigm Function Morphology.

### Class usage

### Lack of unit tests

## Architecture and unit tests

The architecture was refactored to clarify the data structures. Unit tests were written
alongside the new design.

### Functional vision

Classes did not seem necessary. Functions were preferred, with overloads where needed.
Each module (file) exposes one function with declarations (`.pyi`) and implementation
(`.py`).

### Lexicon

The lexicon groups lexemes and their realizations (forms). It rests on two pillars:
language glosses and blocks.

- **Glosses** list all attribute–value pairs the language needs, organized by category.
- **Blocks** declare realization rules per category, linking a sigma (licensed
  feature values) to a lexical construction rule.

### Syntax

Syntax uses a Feature Context-Free Grammar (FCFG): syntactic categories as
non-terminals and feature sigmas. The designer declares non-lexical rules only; a
formalism reduces redundancy.

### Translation

Translation spans both lexicon and syntax and is the most complex stage.

### Toward LaTeX output

## HPSG via NLTK

### PLY: TDL interface with FeatStruct

### From typed to untyped

### Parsing and HPSG

_Content to be completed._
