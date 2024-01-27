# ShinyPy/ShinyCode.py
"""Seamlessly connect and use ShinyDB!

Examples: 
	>>> from ShinyPy import ShinyClient
	>>> client = ShinyClient(key = 'secret')
	>>> databases = await client.get_databases()
	>>> print(databases)
	['aIYuvV', 'rHWU8a', 'dcboQq']

"""

import aiohttp

from .exceptions import Unauthorized, UnknownError, InvalidDetails


class ShinyClient:
	def __init__(self, key: str, host: str = "0.0.0.0", ssl: bool = True):
		"""
		 Initialize the connection to ShinyDB. This is the entry point for the ShinyClient instance.
		 
		 Args:
		 	 key: The key to use for authenticating the connection.
		 	 host: The host to connect to. If not specified the default is "0.0.0.0".
		 	 ssl: Whether to use HTTPS or HTTP. Default is False
		"""
		self._url = f"http{('' if ssl == False else 's')}://{host}"
		self._headers = {"content-type": "application/json", "KEY": key}
		self._session = aiohttp.ClientSession(headers = self._headers)
	

	async def __return_response(self, res):
		if res["status_code"] == 200:
			return res["details"]
		elif res["status_code"] == 400:
			raise InvalidDetails(res["message"])
		elif res["status_code"] == 401:
			raise Unauthorized(res["message"])
		else:
			raise UnknownError("An unknown error occured, please contact an administrator.")


	async def close(self):
		"""
		Close the session. This is a coroutine. 

		Raises: 
			asyncio.TimeoutError: if the session cannot be closed
		"""
		await self._session.close()
	

	async def get_users(self):
		"""Get a list of all users.

		Raises:
			Unauthorized: You are not an admin
			UnknownError: Any other error the database server raises

		Returns:
			list or string: Either a list of users or a string
		"""
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
		"""Get a user by username

		Args:
			username (str): The user you want to get.
		"""
		async with self._session.get(f"{self._url}/api/users/{username}") as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def create_user(self, username: str, email: str, password: str, admin: int = 0):
		"""Create a new user

		Args:
			username (str): The username of the user
			email (str): The email of the user
			password (str): THe password of the user
			admin (int, optional): Whether is the user an admin (1) or not (0). Defaults to 0.
		"""
		params = {
			"username": username,
			"email": email,
			"password": password,
			"admin": admin
		}
		async with self._session.post(f"{self._url}/api/users", params = params) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def update_user(self, user: str, **new_data):
		"""Update the user details

		Args:
			user (str): The user you want to update
			username (str, optional): The new username of the user
			email (str, optional): The new email of the user
			password (str, optional): The new password of the user
			key (str, optional): The new key of the user
			admin (int, optional): hi, idk what to put here
		"""
		params = {}
		if "username" in new_data: params["username"] = new_data["username"]
		if "email" in new_data: params["email"] = new_data["email"]
		if "password" in new_data: params["password"] = new_data["password"]
		if "key" in new_data: params["key"] = new_data["key"]
		if "admin" in new_data: params["admin"] = new_data["admin"]
		async with self._session.put(f"{self._url}/api/users/{user}", params = params) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
			

	async def delete_user(self, username: str):
		"""Delete a user

		Args:
			username (str): The username of the user you want to delete
		"""
		async with self._session.delete(f"{self._url}/api/users/{username}") as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def get_databases(self):
		"""Get all databases owned by you
		"""
		async with self._session.get(f"{self._url}/api/databases") as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def get_database(self, database_id: str):
		"""Get a database by ID

		Args:
			database_id (str): The ID of the database you want to get
		"""
		async with self._session.get(f"{self._url}/api/databases/{database_id}") as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
		

	async def create_database(self, **database_data):
		"""Create a new database

		Args:
			name (str): The name of the database
			description (str, optional): The description of the database
			owner (str): The username of the owner of this database
		"""
		params = {}
		if "name" in database_data: params["name"] = database_data["name"]
		if "description" in database_data: params["description"] = database_data["description"]
		if "owner" in database_data: params["owner"] = database_data["owner"]
		async with self._session.post(f"{self._url}/api/databases", params = params) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def update_database(self, database_id: str, **new_data):
		"""Update a database

		Args:
			database_id (str): The ID of the database to update
			name (str, optional): The new name of the database
			description (str, optional): The new description of the database
		"""
		params = {}
		if "name" in new_data: params["name"] = new_data["name"]
		if "description" in new_data: params["description"] = new_data["description"]
		async with self._session.put(f"{self._url}/api/databases/{database_id}", params = params) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data


	async def delete_database(self, database_id: str):
		"""Delete a database by ID

		Args:
			database_id (str): The ID of the database to delete
		"""
		params = {
			"database_id": database_id
		}
		async with self._session.delete(f"{self._url}/api/databases", params = params) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
	

	async def send_data(self, database_id: str, data: dict):
		"""Overwrite the old database data with new data

		Args:
			database_id (str): The ID of the database
			data (dict): The data you want to put in the database
		"""
		async with self._session.post(f"{self._url}/api/databases/{database_id}", json = data) as response:
			res = await response.json()
			data = await self.__return_response(res)
			return data
