class TableCell(object):
	def __init__(self, content, alignment="<", padding=1):
		self.content = content
		self.alignment = alignment
		self.padding = padding
	
	async def getCellString(self, padding):
		cellString = "{cell.content:" + self.alignment + str(padding) + "}"
		return cellString.format(cell = self)