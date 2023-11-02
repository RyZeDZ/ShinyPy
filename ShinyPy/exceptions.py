class InvalidDetails(Exception):
	def __init__(self, message):
		self.message = message
		self.status_code = 400
		super().__init__(f"{self.message} ({self.status_code})")


class Unauthorized(Exception):
	def __init__(self, message):
		self.message = message
		self.status_code = 401
		super().__init__(f"{self.message} ({self.status_code})")


class UnknownError(Exception):
	def __init__(self, message):
		self.message = message
		self.status_code = 500
		super().__init__(f"{self.message} ({self.status_code})")