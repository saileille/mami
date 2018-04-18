#Functions for lewd command.
#This was Spec's idea, by the way.

import random

from bot import send
from discord import File
from fileIO import getLewdList
from fileIO import loadJsonFromWeb

async def getLewds(message, arguments):
	pictureNames = await getLewdList()
	
	if (message.discord_py.channel.is_nsfw()):
		if (random.random() < 0.1):
			url = await getApiLewd()
			await send(message.discord_py.channel, url)
			
			return
	
	await message.discord_py.channel.send(
		file = File(random.choice(pictureNames))
	)

async def getApiLewd():
	yandereLewds = await loadJsonFromWeb("https://yande.re/post.json?limit=100&tags=tomoe_mami+-rating:s")
	lewdDict = random.choice(yandereLewds)
	return lewdDict["file_url"]