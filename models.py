from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	description = Column(String, index=True)
	complete = Column(Boolean, default=False)
	owner_id = Column(Integer, ForeignKey("users.id"))

	user = relationship("User", back_populates="tasks")


class User(Base):
	__tablename__ = "users"

	id = Column(Integer, primary_key=True, index=True)
	username = Column(String, unique=True, index=True)
	passhash = Column(String)

	tasks = relationship("Task", back_populates="user")