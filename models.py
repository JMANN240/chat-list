from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base

class Task(Base):
	__tablename__ = "tasks"

	uuid = Column(String, primary_key=True, index=True)
	description = Column(String, index=True)
	complete = Column(Boolean, default=False)
	task_list_uuid = Column(String, ForeignKey("task_lists.uuid"))

	task_list = relationship("TaskList", back_populates="tasks")

class TaskList(Base):
	__tablename__ = "task_lists"

	uuid = Column(String, primary_key=True, index=True)

	tasks = relationship("Task", back_populates="task_list")