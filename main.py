import aiohttp

from exceptions import Unauthorized, UnknownError, InvalidDetails


class ShinyClient:
	def __init__(self, key: str, host: str = "0.0.0.0", port: int = 5000, ssl: bool = False):
		"""
		 Initialize the connection to ShinyDB. This is the entry point for the ShinyClient instance.
		 
		 Args:
		 	 key: The key to use for authenticating the connection.
		 	 host: The host to connect to. If not specified the default is " 0. 0. 0. 0 ".
		 	 port: The port to connect to. If not specified the default is 5000.
		 	 ssl: Whether to use HTTPS or HTTP. Default is False
		"""
		self._url = f"http{('' if ssl == False else 's')}://{host}:{port}"
		self._headers = {"content-type": "application/json", "KEY": key}
		self._session = aiohttp.ClientSession(headers = self._headers)
	

	async def close(self):
		"""
		Close the session. This is a coroutine. 
		Raises asyncio.TimeoutError if the session cannot be closed
		"""
		await self._session.close()
	

	async def get_users(self):
		async with self._session.get(f"{self._url}/api/users") as response:
			res = await response.json()
			if res["status_code"] == 200:
				users = []
				for user in res["details"]:
					users.append(user)
				return users
			elif res["status_code"] == 401 or res["status_code"] == 403:
				raise Unauthorized(res["message"])
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
	

	async def get_user(self, username: str):
		async with self._session.get(f"{self._url}/api/users/{username}") as response:
			res = await response.json()
			if res["status_code"] == 200:
				return res["details"]
			elif res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
	

	async def create_user(self, username: str, email: str, password: str, admin: int = 0):
		params = {
			"username": username,
			"email": email,
			"password": password,
			"admin": admin
		}
		async with self._session.post(f"{self._url}/api/users", params = params) as response:
			res = await response.json()
			if res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])	
			elif res["status_code"] == 200:
				return res["details"]
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
	

	async def update_user(self, user: str, **new_data):
		params = {}
		if "username" in new_data: params["username"] = new_data["username"]
		if "email" in new_data: params["email"] = new_data["email"]
		if "password" in new_data: params["password"] = new_data["password"]
		if "key" in new_data: params["key"] = new_data["key"]
		if "admin" in new_data: params["admin"] = new_data["admin"]
		async with self._session.put(f"{self._url}/api/users/{user}", params = params) as response:
			res = await response.json()
			if res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])
			elif res["status_code"] == 200:
				return res["details"]
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
			

	async def delete_user(self, username: str):
		async with self._session.delete(f"{self._url}/api/users/{username}") as response:
			res = await response.json()
			if res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])
			elif res["status_code"] == 200:
				return res["details"]
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
	

	async def get_databases(self):
		async with self._session.get(f"{self._url}/api/databases") as response:
			res = await response.json()
			if res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])
			elif res["status_code"] == 200:
				return res["details"]
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")
	

	async def get_database(self, database_id: str):
		async with self._session.get(f"{self._url}/api/databases/{database_id}") as response:
			res = await response.json()
			if res["status_code"] == 400:
				raise InvalidDetails(res["message"])
			elif res["status_code"] == 401:
				raise Unauthorized(res["message"])
			elif res["status_code"] == 200:
				return res["details"]
			else:
				raise UnknownError("An unknown error occured, please contact an administrator.")