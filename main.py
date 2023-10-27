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