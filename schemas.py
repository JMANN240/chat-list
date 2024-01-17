from typing import Optional

from pydantic import BaseModel

class UserBase(BaseModel):
	username: str

class UserCreate(UserBase):
	password: str

class User(UserBase):
	uuid: str

	class Config:
		from_attributes = True

class Token(BaseModel):
	access_token: str
	token_type: str

class TaskBase(BaseModel):
	uuid: str
	owner_uuid: str

class TaskDelete(TaskBase):
	pass

class TaskCreate(BaseModel):
	parent_task_uuid: Optional[str]
	description: str

class TaskUpdate(TaskCreate):
	uuid: str

class Task(TaskBase):
	description: str
	complete: bool
	child_tasks: list['Task']

	class Config:
		from_attributes = True