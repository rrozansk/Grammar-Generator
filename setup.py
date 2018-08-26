"""
Create the PyPI package distribution(s) for use with python pip or install
directly.
"""
from setuptools import setup


with open('README.md', 'r') as fd:
    README = fd.read()

setup(
    name='scanner_parser_generator',
    version='0.0.18',
    license='MIT',
    author='Ryan Rozanski',
    author_email='',
    maintainer='Ryan Rozanski',
    maintainer_email='',
    description=(
        'A CLI program bundled with importable scanner, parser, and generator '
        'libraries which are used to generate scanners and/or parsers from '
        'regular expressions and LL(1) BNF grammar specifications respectively.'
    ),
    long_description=README,
    long_description_content_type='text/markdown',
    url='https://github.com/rrozansk/Scanner-Parser-Generator',
    download_url='https://github.com/rrozansk/Scanner-Parser-Generator',
    python_requires='>= 2.7.0',
    keywords=' '.join([
        'bnf',
        'BNF',
        'cli',
        'CLI',
        'code-generation',
        'context-free-grammar',
        'lexer',
        'lexer-generator',
        'lexical-analysis',
        'll1',
        'LL1',
        'LL(1)',
        'parser',
        'parser-generator',
        'regular-expression(s)',
        'regular-grammar',
        'scanner-generator',
        'scanner',
        'tokenizer',
        'tokens'
    ]),
    packages=[
        'scanner_parser_generator',
        'scanner_parser_generator.parser',
        'scanner_parser_generator.scanner',
        'scanner_parser_generator.generators'
    ],
    package_dir={
        'scanner_parser_generator': 'src',
        'scanner_parser_generator.parser': 'src/parser',
        'scanner_parser_generator.scanner': 'src/scanner',
        'scanner_parser_generator.generators': 'src/generators'
    },
    package_data={
        'scanner_parser_generator': [
            '../LICENSE.txt'
        ]
    },
    include_package_data=True,
    zip_safe=True,
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
        'Topic :: Software Development :: Compilers',
        'Topic :: Text Processing',
        'Topic :: Text Processing :: Linguistic'
    )
)
