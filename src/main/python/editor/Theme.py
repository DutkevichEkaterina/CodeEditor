class Theme:
    def __init__(self, theme: dict, txtArea):
        self.txtArea = txtArea
        self.theme = theme
        self.update()

    def update(self):
        for style in self.theme:
            self.txtArea.tag_configure(str(self.theme[style].get("color")), foreground = str(self.theme[style].get("color")))