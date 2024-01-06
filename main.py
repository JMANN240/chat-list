from fastapi import Depends, FastAPI, HTTPException, Header
from sqlalchemy.orm import Session
from typing import Annotated

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

@app.get("/tasks", response_model=list[schemas.Task])
async def read_tasks(db: Session = Depends(get_db), authorization: Annotated[str | None, Header()] = None):
	print(authorization)
	return crud.get_user_tasks(db, 0)