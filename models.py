from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
	__tablename__ = "users"

	uuid = Column(String, primary_key=True, index=True)
	username = Column(String, unique=True, nullable=False, index=True)
	passhash = Column(String, nullable=False)

	tasks = relationship("Task", back_populates="owner")

class Task(Base):
	__tablename__ = "tasks"

	uuid = Column(String, primary_key=True, index=True)
	description = Column(String, index=True)
	complete = Column(Boolean, default=False)
	parent_task_uuid = Column(String, ForeignKey("tasks.uuid"))
	owner_uuid = Column(String, ForeignKey("users.uuid"))

	owner = relationship("User", back_populates="tasks")
	parent_task = relationship("Task", back_populates="child_tasks", remote_side=[uuid])
	child_tasks = relationship("Task", back_populates="parent_task")
