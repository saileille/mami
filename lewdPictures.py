#Functions for lewd command.
#This was Spec's idea, by the way.

import random
from discord import File

from fileIO import getLewdList
from fileIO import loadJsonFromWeb
from sendFunctions import send

async def getLewds(message, arguments, nsfw):
	pictureNames = await getLewdList()
	
	#5% chance for an actual lewd when in NSFW channel. ;)
	if (nsfw == True and random.random() < 0.05):
		url = await getApiLewd()
		await send(message.discord_py.channel, url)
	else:
		async with message.discord_py.channel.typing():
			await send(
				message.discord_py.channel
				,filePaths = [random.choice(pictureNames)]
			)

async def getApiLewd():
	yandereLewds = await loadJsonFromWeb("https://yande.re/post.json?limit=100&tags=tomoe_mami+-rating:s")
	lewdDict = random.choice(yandereLewds)
	return lewdDict["file_url"]