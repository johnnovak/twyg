from pygments.style import Style
from pygments.token import (Punctuation, Text, Comment, Keyword, Name, String,
                            Generic, Operator, Number, Whitespace,
                            Literal, Error)



class TwygStyle(Style):
    default_style = ""

    styles = {
        Whitespace:                "#fff",

        Comment:                   "#999",
        Comment.Preproc:           "",
        Comment.Special:           "",

        Keyword:                   "",
        Keyword.Pseudo:            "bold #4aa",
        Keyword.Type:              "bold #56a3a5",

        Operator:                  "",
        Operator.Word:             "",

        Name.Builtin:              "",
        Name.Function:             "",
        Name.Class:                "",
        Name.Namespace:            "",
        Name.Exception:            "",
        Name.Variable:             "",
        Name.Variable.Instance:    "",
        Name.Variable.Class:       "",
        Name.Variable.Global:      "",
        Name.Constant:             "",
        Name.Label:                "bold #83b69c",
        Name.Entity:               "",
        Name.Attribute:            "",
        Name.Tag:                  "",
        Name.Decorator:            "",

        String:                    "#696",
        String.Char:               "",
        String.Doc:                "",
        String.Interpol:           "",
        String.Escape:             "",
        String.Regex:              "",
        String.Symbol:             "",
        String.Other:              "",

        Number:                    "bold #7a8",
        Number.Integer:            "",
        Number.Float:              "",
        Number.Hex:                "bold #f67",
        Number.Oct:                "",

        Generic.Heading:           "",
        Generic.Subheading:        "",
        Generic.Deleted:           "",
        Generic.Inserted:          "",
        Generic.Error:             "",
        Generic.Emph:              "",
        Generic.Strong:            "",
        Generic.Prompt:            "",
        Generic.Output:            "",
        Generic.Traceback:         "",

        Error:                     "#f00 bg:#faa"
    }

