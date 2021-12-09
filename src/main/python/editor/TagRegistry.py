class TagRegistry:
    def __init__(self, styles_dict):
        self.styles_dict = styles_dict

    def findTagByName(self, name: str) -> str:
        # поиск по убыванию длины имени
        if name in self.styles_dict:
            return self.styles_dict[name].get("color")
        else:
            i = name.rfind(".")
            while i != -1:
                # тут надо будет обрезать строку и поискать
                name = name[:i]
                if name in self.styles_dict:
                    return self.styles_dict[name].get("color")
                i = name.rfind(".")
            return None

    styles_dict: dict

#В конструктор передаем множество имен тэгов из темы
# передать HashSet