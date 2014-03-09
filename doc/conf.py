# -*- coding: utf-8 -*-

extensions = ['sphinx.ext.autodoc']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'contents'

project = u'twyg'
copyright = u'2013, John Novak'
version = '0.1'
release = '0.1'

exclude_patterns = ['_build']

pygments_style = 'style.TwygStyle'
highlight_language = 'twyg'

html_theme = 'twyg'
html_theme_path = ['_themes']
html_static_path = ['_static']


html_additional_pages = {
  'index':      'index.html',
  'getit':      'getit.html',
  'quickstart': 'quickstart.html',
  'examples':   'examples.html'
}

htmlhelp_basename = 'twygdoc'


# -- twyg Pygments lexer -------------------------------------------------------

from pygments.lexer import Lexer, RegexLexer
from pygments.token import (Punctuation, Text, Comment, Keyword, Name, String,
                            Generic, Operator, Number, Whitespace,
                            Literal, Error)

class TwygLexer(RegexLexer):
    """
    Lexer for twyg configuration files.
    """

    name = 'Twyg'
    aliases = ['twyg']
    filenames = ['*.twg']
    mimetypes = []

    tokens = {
        'root': [
            (r'\s+', Text),
            (r'--.*', Comment),
            (r'\[[a-zA-Z]+\]', Keyword.Type),                    # Section
            (r'{[a-zA-Z][a-zA-Z0-9_]*}', Name.Label),            # Level
            (r'@[a-zA-Z]+', Keyword.Pseudo),                     # Directive
            (r'[+-]?[0-9]+\.[0-9]*|[0-9]*\.[0-9]+', Number.Float),    # Float
            (r'[0-9][0-9]*%', Number),                           # Percent
            (r'[0-9][0-9]*', Number.Integer),                    # Integer
            (r'\+|-|\*|/|\^|\(|\)|\[|\]|\.|,', Operator),        # Operator
            (r'[a-zA-Z][a-zA-Z0-9_]*', Name.Attribute),          # Name
            (r'#[a-zA-Z0-9]+', Number.Hex),                      # Hex Color
            (r'"[^"\\]*(?:\\.[^"\\]*)*"', String.Double)         # String
        ]
    }


# -- Extension interface -------------------------------------------------------

import sys, os

from docutils.parsers import rst
from docutils import nodes


# Needed for Pygments to find the custom style
sys.path.append(os.path.join('.'))


class PropertyParams(rst.Directive):
    required_arguments = 2
    final_argument_whitespace = True
    option_spec = {'values': rst.directives.unchanged}
    has_content = False

    def run(self):
        proptype = self.arguments[0]
        default = self.arguments[1]
        dl = nodes.definition_list()
        dl['classes'].append('propparams')

        term = nodes.term('', 'Type')
        defnode = nodes.definition('', nodes.paragraph('', proptype))
        dl += nodes.definition_list_item('', term, defnode)

        if 'values' in self.options:
            term = nodes.term('', 'Values')
            defnode = nodes.definition('',  nodes.paragraph('',
                                       self.options['values']))
            dl += nodes.definition_list_item('', term, defnode)

        term = nodes.term('', 'Default')
        defnode = nodes.definition('',  nodes.paragraph('', default))
        dl += nodes.definition_list_item('', term, defnode)

        return [dl]


def setup(app):
    app.add_object_type('property', 'property',
                        objname='configuration property',
                        indextemplate='pair: %s; configuration property')

    app.add_object_type('directive', 'directive',
                        objname='configuration directive',
                        indextemplate='pair: %s; configuration directive')

    app.add_directive('propparams', PropertyParams)

    app.add_lexer('twyg', TwygLexer())

