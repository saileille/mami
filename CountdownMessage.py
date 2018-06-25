#Contains data about the channel and the message content that needs to be sent/edited.

class CountdownMessage(object):
	def __init__(self, channel, content):
		self.channel = channel
		self.content = content
	
	async def send(self, timer):
		return await self.channel.send(await self.getContent(timer))
	
	async def getContent(self, timer):
		return self.content.format(timer = timer)