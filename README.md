Scanner-Parser-Generator
========================

  - [Introduction](#introduction)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Methods](#methods)
      - [Source](#source)
        - [Prerequisites](#source-prerequisites)
        - [Install](#source-install)
      - [Pip](#pip)
        - [Prerequisites](#pip-prerequisites)
        - [Install](#pip-install)
    - [Test](#test)
  - [Usage](#usage)
    - [Library](#library)
    - [CLI](#cli)
  - [Scanner](#scanner)
    - [Input](#scanner-input)
  - [Parser](#parser)
    - [Input](#parser-input)
  - [Generate](#generators)
    - [Status](#status)
    - [Extension](#extension)
      - [Template](#template)
      - [Pylint](#pylint)
  - [License](#license)

# Introduction

An extensible purely Python framework (with no external dependencies!) capable
of producing scanners and/or parsers from regular expressions (regular grammars)
and LL(1) BNF languages (a subset of context free grammars), outputting the
results as valid programs in the choosen language. The framework is modular in
design being made up of only three components: scanner, parser, and program
generators. The scanner/parser tranformation processes are very formal,
well defined and understood and thorough table driven testing is also utilized
to ensure correctness. The program generator is the extensible portion,
allowing new targeted languages to be easily added (see below). Included is a
Python CLI program which accepts user file input(s) to help drive the
compilation/generation process. Below describes in detail what each component
sets out to do, how it accomplished those intended goals, and the accepted
input.

# Installation

Multiple installation methods are supported, all of which are listed below.
Each individual method lists the additional dependencies needed, if any,
along with all the steps required for a proper install.

## Prerequisites

These are the prerequisites required reguardless of choosen installation method.

  - python >= 2.7.0

## Methods
### Source

#### Source Prerequisites

  - git
  - setuptools

#### Source Install

```sh
# 1. Obtain the source code.
$ git clone https://github.com/rrozansk/Scanner-Parser-Generator.git

# 2. Install using the provided python setup script.
$ python setup.py install
```

### Pip

#### Pip Prerequisites

  - pip

#### Pip Install

```sh
# Only step required!
$ pip install scanner-parser-generator
```

## Test

Run the tests to ensure compatibility and verify installation went correctly.

NOTE: No output expected if all scanner and/or parser tests pass.

```sh
# 1. Run the scanner test suite.
$ python -m scanner_parser_generator.scanner

# 2. Run the parser test suite.
$ python -m scanner_parser_generator.parser

# 3. Check the generator CLI program installed correctly.
$ python -m scanner_parser_generator.generate --help
```

# Usage

This python module may be imported or invoked as a command line program.

NOTE: for the command line program to work properly the argparse package is
needed. It comes in most python versions but will need to be explicitly
installed if using python 3.0 or 3.1.

## Library

The individual components may be imported to produce custom python programs.
The RegularGrammar and ContextFreeGrammar are completely independent from one
another. For there respective documentation and interface see scanner.py and
parser.py. The individual generators may also be imported but they have a
dependency on both RegularGrammar and ContextFreeGrammar. For there respective
documentation and interface see the base generator in generators/\_\_init\_\_.py.
Below shows how the various components may be imported.

```sh
$ /usr/bin/python3
Python 3.5.2 (default, Nov 23 2017, 16:37:01)
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> from scanner_parser_generator.scanner import RegularGrammar
>>> from scanner_parser_generator.parser import ContextFreeGrammar
>>> from scanner_parser_generator.generators.c import C
>>> from scanner_parser_generator.generators.go import Go
>>> from scanner_parser_generator.generators.python import Python
```

## CLI

Different examples for the generator to produce scanner's and/or parser's for
different token sets and LL(1) languages may be found under examples/.
Shown below are some basic invocation's for help, scanner, and parser generation.

```sh
# Generate your scanner and/or parser! ...but first ask for help.
$ python -m scanner_parser_generator.generate --help

# Generate an ini scanner in c.
$ python -m scanner_parser_generator.generate -s examples/INI/scanner.txt -g c -o scan

# Generate an ini parser in c.
$ python -m scanner_parser_generator.generate -p examples/INI/parser.txt -g c -o parse
```

# Scanner

The scanner attempts to transform a collection of named patterns (regular
expression/token type pairs) into a unique minimal DFA accepting any input
specified while also containing an errors sink state for all invalid input.
The transformation begins by first checking the expression for validity while
internalizing it. Next, the use of an augmented version of Dijkstra's shunting
yard algorithm transforms the expression into prefix notation. From here
Thompson's algorithm is utilized to produce an NFA with epsilon productions. The
NFA is then directly converted into a minimal DFA with respect to reachable
states using e-closure conversions which are cached. Finally, the minimal DFA is
made total, if not already, so it can be further minimized with respect to
indistinguishable states using Hopcroft's algorithm.

## Scanner Input

Regular expressions must be specified following these guidelines:

```text
- only printable ascii characters (33-126) and spaces are supported
- supported operators:
    |                (union -> choice -> either or)
    ?                (question -> choice -> 0 or none)
    .                (concatenation -> combine)
    *                (kleene star -> repitition >= 0)
    +                (plus -> repitition >= 1)
    ()               (grouping -> disambiguation -> any expression)
    [ab]             (character class -> choice -> any specified char)
    [a-c] or [c-a]   (character range -> choice -> any char between the two)
    [^ab] or [^a-c]  (character negation -> choice -> all but the specified)
    NOTES: '^' is required to come first after the bracket for negation.
           If alone ([^]) it is translated as all alphabet characters.
           It is still legal for character ranges as well ([b-^] and
           negated as [^^-b]). Note that the reverse range was needed. If
           the first character is a '^' it will always mean negation! If a
           single '^' is wanted then there is no need to use a class/range.
           Classes and ranges can be combined between the same set of
           brackets ([abc-z]), even multiple times if wanted/needed. Due to
           this though the '-' char must come as the last character in the
           class if the literal is wanted. For literal right brackets an
           escape is needed if mentioned ([\]]). All other characters are
           treated as literals.
- concat can be either implicit or explicit
- supported escape sequences:
    operator literals   -> \?, \*, \., \+, \|
    grouping literals   -> \(, \), \[, \]
    whitespace literals -> \s, \t, \n, \r, \f, \v
    escape literal      -> \\\\
```

# Parser

The parser attempts to transform a collection of BNF production rules into a
parse table. While any BNF is accepted only LL(1) grammars will produce a valid
parse table containing no conflicts. Furthermore, the grammar must have no left
recursion or ambiguity while also being left factored. The first step in
constructing the resulting table is determining the terminal and nonterminal
sets, which is very trivial. From here, the sets are used to construct the first
and follow sets which identify what characters can be expected when parsing
corresponding production rules. Subsequently, the first and follow sets are used
to construct the predict sets which are in turn used in the table construction.
Finally, the table is verified by checking for conflicts.

## Parser Input

Context Free Grammars must be specified following these guidelines:

```text
- no left recursion (direct or indirect)
- must be left factored
- no ambiguity
- no syntax rules are enforced on nonterminals, but by conventions they should
  be delimited by a pair of angle brackets '< >'
- multiple productions per nonterminal may be specified, but each must be
  delimited by a '|'
- production symbols must be delimited by whitespace
- epsilon may be specified by declaring an empty production
```

# Generators

The generators are very light weight wrappers on top of the scanner/parser
objects and are responsible for compiling there output into a useable program in
the choosen language.

## Status

Below shows the current status of the generators:

  * [![C](https://img.shields.io/badge/C-Developing-yellow.svg)](https://github.com/rrozansk/Scanner-Parser-Generator/blob/master/scanner_parser_generator/generators/c.py)
  * [![Golang](https://img.shields.io/badge/Golang-Planned-red.svg)](https://github.com/rrozansk/Scanner-Parser-Generator/blob/master/scanner_parser_generator/generators/go.py)
  * [![Python](https://img.shields.io/badge/Python-Planned-red.svg)](https://github.com/rrozansk/Scanner-Parser-Generator/blob/master/scanner_parser_generator/generators/python.py)

## Extension

Adding a new generator is extremely simple as it only requires the addition of a
single file containing a single class definition and allows output to a new langauge.

### Template

Using the below as a template create a new file with the given contents under
scanner_parser_generator/generators, naming the file after the language being compiled to:

```python
"""
A scanner/parser generator targeting {filename}.
"""
from . import Generator


class {Filename}(Generator):
    """
    A simple object for compiling scanner's and/or parser's to {filename} programs.
    """

    def output(self, filename):
        """
        Attempt to generate the {filename} file(s) with the corresponding
        scanner and/or parser currently set in the object.

        Input Type:
          filename: String

        Output Type: List[Tuple[String, String]] | ValueError
        """
        pass
```

NOTE: the class name is a capitalized version of the filename.
This is important for the framework to automatically pick up and use the file/class.

### Pylint

There is also a .pylintrc file included in the repository so that your generator conforms
to the style guidlines of the rest of the project which provides a similiar look and feel.

```sh
# Lint your new generator and save the output in a file.
$ pylint scanner_parser_generator/generators/<new generator>.py > output.txt

# Update accordingly as per pylint's comments in output.txt.
$ vim output.txt scanner_parser_generator/generators/<new generator>.py
```

# License

[MIT](https://github.com/rrozansk/Scanner-Parser-Generator/blob/master/LICENSE.txt)
