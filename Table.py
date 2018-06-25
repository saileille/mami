#Some neat formatting.

class Table(object):
	def __init__(self):
		self.table = []
		self.columns = []
	
	async def addRow(self, row):
		self.table.append(row)
	
	async def addColumn(self, column):
		for i in range(len(self.table)):
			row = self.table[i]
			row.append(column[i])
	
	async def getTableString(self):
		await self.getColumnWidths()
		
		text = ""
		for i in range(len(self.table)):
			row = self.table[i]
			
			if (text != ""):
				text += "\n"
			
			for columnIndex in range(len(row)):
				cell = row[columnIndex]
				
				if (columnIndex != 0):
					text += (" " * cell.padding)
				
				text += await cell.getCellString(self.columns[columnIndex])
		
		return text
	
	async def getColumnWidths(self):
		for row in self.table:
			for columnIndex in range(len(row)):
				cell = row[columnIndex]
				cellSize = len(cell.content)
				
				#This should never happen.
				while (len(self.columns) < columnIndex):
					self.columns.append(0)
				
				if (len(self.columns) == columnIndex):
					self.columns.append(cellSize)
				elif (cellSize > self.columns[columnIndex]):
					self.columns[columnIndex] = cellSize