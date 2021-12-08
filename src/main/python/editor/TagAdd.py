class TagAdd():

	def __init__(self, tagRegistry, txtArea):
		self.tagRegistry = tagRegistry
		self.txtArea = txtArea

	def call(self, tag: str, start: str, end:str):
		styleName = self.tagRegistry.findTagByName(tag)
		if styleName != None:
			self.txtArea.tag_add(styleName, start, end);