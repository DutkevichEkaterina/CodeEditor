class Theme:
    def __init__(self, theme: dict, txtArea):
        self.txtArea = txtArea
        for style in theme:
            txtArea.tag_configure(str(theme[style].get("color")), foreground = str(theme[style].get("color")))