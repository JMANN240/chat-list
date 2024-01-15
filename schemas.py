from pydantic import BaseModel

class TaskBase(BaseModel):
	task_list_uuid: str
	description: str

class TaskCreate(TaskBase):
	pass

class Task(TaskBase):
	uuid: str
	complete: bool

	class Config:
		from_attributes = True

class TaskListBase(BaseModel):
	uuid: str

class TaskList(TaskListBase):
	tasks: list[Task] = []

	class Config:
		from_attributes = True