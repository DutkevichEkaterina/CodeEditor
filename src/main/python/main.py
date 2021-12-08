# Importing Required libraries & Modules
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import tree_sitter
from tree_sitter import Language, Parser
import random
import json
import re
from highlighter.HighlighterTreeSitterImpl import HighlighterTreeSitterImpl

from editor.CodeEditor import CodeEditor

Language.build_library('build/my-languages.so', ['../../../tree-sitter-ruby'])
t_ruby = Language('build/my-languages.so', 'ruby')
highlightsQuery = t_ruby.query(open("../../../tree-sitter-ruby/queries/highlights.scm").read())
localsQuery = t_ruby.query(open("../../../tree-sitter-ruby/queries/locals.scm").read())
t_parser = Parser()
t_parser.set_language(t_ruby)
 
highlighter = HighlighterTreeSitterImpl(t_parser, highlightsQuery, localsQuery)
styles_dict = json.loads(open("theme.json").read())
root = Tk()

CodeEditor(root, highlighter, styles_dict)
root.mainloop()



