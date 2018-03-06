class MessagePart(object):
	def __init__(self, message, startsInBlock, endsInBlock):
		self.message = message
		self.start_block = startsInBlock
		self.end_block = endsInBlock