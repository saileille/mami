#Name subject to change - preferable if this could host multiple functions.

from Permission import Permission
from PermissionChanger import PermissionChanger
from StringHandler import StringHandler

#Returns a boolean based on whether the command is allowed or not.
async def checkCommandPermission(
	cmdCode
	,userObject
	,serverSettings
	,channelSettings
	,channelObject = None
):
	if (channelObject != None):
		userPermissions = userObject.permissions_in(channelObject)
	else:
		#Channel object is not given if we are syncing servers...
		userPermissions = userObject.server_permissions
	"""
	#Admins get past everything.
	if (userPermissions.administrator == True):
		return True
	"""
	
	#Channel permission check. If none specified, moves to server permission check.
	if (cmdCode in channelSettings.permissions):
		permission = channelSettings.permissions[cmdCode]
		
		return await permission.checkPermission(userObject, userPermissions)
	
	#If the channel does not belong to a server, we get the default thing.
	if (serverSettings == None):
		cmdObject = await StringHandler(cmdCode).getCommandFromString()
		
		permission = Permission()
		await permission.forceDefault()
		permission.permissions = cmdObject.default_permissions
		
		return await permission.checkPermission(userObject, userPermissions)
	
	#Server permission check.
	#Adds a default Permission object if the command is lacking one for this server.
	permission = await PermissionChanger().getPermissionObject(cmdCode, serverSettings.permissions)
	
	#Checking server-wide permissions.
	return await permission.checkPermission(userObject, userPermissions)