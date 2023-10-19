# ShinyPy
An API wrapper for ShinyDB!

Example:
```
from shinypy import ShinyClient
import asyncio


async def main():
	client = ShinyClient("API-KEY")
	user = await client.get_user("RyZe")
	await client.close()
	print(user)


asyncio.run(main())

```