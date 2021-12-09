import tree_sitter
from tree_sitter import Language, Parser

from highlighter.HighlighterCallback import HighlighterCallback

class HighlighterTreeSitterImpl :

    def __init__(self, parser, highlightsQuery, localsQuery):
        self.t_parser = parser
        self.highlightsQuery = highlightsQuery
        self.localsQuery = localsQuery
        self.add_tag_method: HighlighterCallback
        # Language.build_library('build/my-languages.so', ['tree-sitter-ruby'])
        # self.t_ruby = Language('build/my-languages.so', 'ruby')
        # self.t_parser = Parser()
        # self.t_parser.set_language(self.t_ruby)
        # self.t_tree = self.t_parser.parse(bytes(" ", "utf8"))
        # self.color_dict = dict()
        # self.highlightsQuery = self.t_ruby.query(open("tree-sitter-ruby/queries/highlights.scm").read())
        # self.localsQuery = self.t_ruby.query(open("tree-sitter-ruby/queries/locals.scm").read())
        # self.styles_dict = json.loads(open("theme.json").read())
        # self.add_tag_method = add_color_tag

    def highlight(self, code: str, callback: HighlighterCallback):
        self.t_tree = self.t_parser.parse(bytes(code, "utf8"))
        captures = self.highlightsQuery.captures(self.t_tree.root_node)
        self.processCaptures(captures, callback)
        captures = self.localsQuery.captures(self.t_tree.root_node)
        self.processCaptures(captures, callback)

    def processCaptures(self, captures, callback: HighlighterCallback):
        for capture in captures:
            node = capture[0]
            name = capture[1]
            start_point = str(node.start_point).replace(", ", ".").replace("(", "").replace(")", "")
            end_point = str(node.end_point).replace(", ", ".").replace("(", "").replace(")", "")
            start_y, start_x = map(int, start_point.split("."))
            end_y, end_x = map(int, end_point.split("."))
            start_point = str(start_y + 1) + "." + str(start_x)
            end_point = str(end_y + 1) + "." + str(end_x)
            callback.call(name, start_point, end_point)
            # style = self.findStyleByName(name)
            # if (style != None):  # если стиль найден
            #     self.highlight_node(node, style)


    add_tag_method: HighlighterCallback
