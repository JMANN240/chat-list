from uuid import uuid4

from sqlalchemy.orm import Session

import models, schemas

def get_task_list(db: Session, task_list_uuid: str) -> models.TaskList:
	return db.query(models.TaskList).filter(models.TaskList.uuid == task_list_uuid).first()

def create_task_list(db: Session) -> models.TaskList:
	db_task_list = models.TaskList(uuid=str(uuid4()))
	db.add(db_task_list)
	db.commit()
	db.refresh(db_task_list)
	return db_task_list

def get_tasks(db: Session, task_list_uuid: str):
	return db.query(models.Task).filter(models.TaskList.uuid == task_list_uuid).all()

def create_task(db: Session, task: schemas.TaskCreate) -> models.Task:
	db_task = models.Task(uuid=str(uuid4()), description=task.description, task_list_uuid=task.task_list_uuid)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task