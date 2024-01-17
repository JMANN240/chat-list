from typing import Union
from uuid import uuid4

import bcrypt
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import models, schemas

def get_user(db: Session, username: str):
	return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user_create: schemas.UserCreate):
	salt = bcrypt.gensalt()
	passhash = bcrypt.hashpw(user_create.password.encode('utf-8'), salt)
	db_user = models.User(uuid=str(uuid4()), username=user_create.username, passhash=passhash)
	db.add(db_user)
	db.commit()
	return db_user

def verify_user(db: Session, form_data: OAuth2PasswordRequestForm):
	db_user = get_user(db, form_data.username)
	if db_user is None:
		return None
	if not bcrypt.checkpw(form_data.password.encode('utf-8'), db_user.passhash):
		return None
	return db_user

def create_task(db: Session, user: models.User, task_create: schemas.TaskCreate) -> models.Task:
	db_task = models.Task(uuid=str(uuid4()), description=task_create.description, owner_uuid=user.uuid, parent_task_uuid=task_create.parent_task_uuid)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task

def get_root_tasks(db: Session, user: models.User) -> list[models.Task]:
	return db.query(models.Task).filter(models.Task.owner_uuid == user.uuid, models.Task.parent_task == None).all()

def get_tasks(db: Session, user: models.User) -> list[models.Task]:
	return db.query(models.Task).filter(models.Task.owner_uuid == user.uuid).all()

def get_task(db: Session, user: models.User, uuid: str) -> models.Task:
	return db.query(models.Task).filter(models.Task.owner_uuid == user.uuid, models.Task.uuid == uuid).first()

def complete_task(db: Session, user: models.User, uuid: str) -> models.Task:
	db_task = get_task(db, user, uuid)
	db_task.complete = True
	db.commit()
	db.refresh(db_task)
	return db_task

def uncomplete_task(db: Session, user: models.User, uuid: str) -> models.Task:
	db_task = get_task(db, user, uuid)
	db_task.complete = False
	db.commit()
	db.refresh(db_task)
	return db_task

def update_task(db: Session, user: models.User, task_update: schemas.TaskUpdate) -> models.Task:
	db_task = get_task(db, user, task_update.uuid)
	db_task.description = task_update.description
	db_task.parent_task_uuid = task_update.parent_task_uuid
	db.commit()
	db.refresh(db_task)
	return db_task

def delete_task(db: Session, user: models.User, uuid: str) -> None:
	db_task = get_task(db, user, uuid)
	db.delete(db_task)
	db.commit()