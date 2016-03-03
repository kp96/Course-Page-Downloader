from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from base import Base
class User(Base):
	__tablename__ = 'user'
	user_regno = Column(String(11), primary_key = True)
	user_password = Column(String(15))
	def __init__(self, user_regno = None, user_password = None):
		self.user_regno  = user_regno
		self.user_password = user_password