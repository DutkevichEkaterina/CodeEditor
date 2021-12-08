from src.main.python.highlighter import HighlighterCallback

class HighlighterInterface:

    def __init__(self, highlightsQuery, localsQuery):

        pass

    def highlight(self, code: str, callback: HighlighterCallback):
        """Load in the file for extracting text."""
        pass
