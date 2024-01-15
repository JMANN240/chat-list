from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

@app.get("/task_list", response_model=schemas.TaskList)
async def get_task_list(uuid: str, db: Session = Depends(get_db)):
	return crud.get_task_list(db, uuid)

@app.post("/task_list", response_model=schemas.TaskList)
async def create_task_list(db: Session = Depends(get_db)):
	return crud.create_task_list(db)

@app.post("/task", response_model=schemas.Task)
async def create_task(task_create: schemas.TaskCreate, db: Session = Depends(get_db)):
	print(task_create)
	return crud.create_task(db, task_create)