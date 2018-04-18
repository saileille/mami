#Name subject to change - preferable if this could host multiple functions.

from Permission import Permission
from PermissionChanger import PermissionChanger
from StringHandler import StringHandler

#Returns a boolean based on whether the command is allowed or not.
async def checkCommandPermission(
	userObject
	,serverSettings
	,channelSettings
	,commandList
	,channelObject = None
):
	#Channel object is not given if we are syncing servers...
	if (channelObject != None):
		userPermissions = userObject.permissions_in(channelObject)
	else:
		userPermissions = userObject.server_permissions
	"""
	#Admins get past everything.
	if (userPermissions.administrator == True):
		return True
	"""
	permissionKey = ".".join(commandList)
	
	#Channel permission check. If none specified, moves to server permission check.
	if (permissionKey in channelSettings.permissions):
		permission = channelSettings.permissions[permissionKey]
		
		#print(await permission.toDict())
		return await permission.checkPermission(userObject, userPermissions)
	
	#If the channel does not belong to a server, we get the default thing.
	if (serverSettings == None):
		cmdObject = await StringHandler(permissionKey).getCommandFromString()
		
		permission = Permission()
		await permission.forceDefault()
		permission.permissions = cmdObject.default_permissions
		
		return await permission.checkPermission(userObject, userPermissions)
	
	#Server permission check.
	#Adds a default Permission object if the command is lacking one for this server.
	permission = await PermissionChanger().getPermissionObject(permissionKey, serverSettings.permissions)
	
	#print(await permission.toDict())
	#Checking server-wide permissions.
	return await permission.checkPermission(userObject, userPermissions)