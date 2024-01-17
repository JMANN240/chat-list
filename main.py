from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from sqlalchemy.orm import Session

import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

JWT_SECRET_KEY = 'secret'
JWT_ALGORITHM = 'HS256'

app = FastAPI(servers=[{'url': 'https://chat-listkentsoftwarecollective.com'}])

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail="Could not validate credentials",
		headers={'WWW-Authenticate': 'Bearer'}
	)
	try:
		payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
		username: str = payload.get('sub')
		if username is None:
			raise credentials_exception
	except jwt.InvalidTokenError:
		raise credentials_exception
	user = crud.get_user(db, username)
	if user is None:
		raise credentials_exception
	return user

@app.post("/token")
async def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
	verified_user = crud.verify_user(db, form_data)
	if verified_user is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Incorrect username or password",
			headers={'WWW-Authenticate': 'Bearer'}
		)
	access_token_expires = timedelta(days=60)
	access_token = jwt.encode({
		'exp': datetime.now(timezone.utc) + access_token_expires,
		'sub': verified_user.username
	}, JWT_SECRET_KEY, JWT_ALGORITHM)
	return schemas.Token(access_token=access_token, token_type='bearer')

@app.post("/user", response_model=schemas.User)
async def create_user(user_create: schemas.UserCreate, db: Annotated[Session, Depends(get_db)]):
	return crud.create_user(db, user_create)

@app.post("/task/complete", response_model=schemas.Task)
async def complete_task(
		uuid: str,
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.complete_task(db, user, uuid)

@app.post("/task/uncomplete", response_model=schemas.Task)
async def uncomplete_task(
		uuid: str,
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.uncomplete_task(db, user, uuid)

@app.get("/tasks", response_model=list[schemas.Task])
async def get_tasks(
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.get_root_tasks(db, user)

@app.post("/task", response_model=schemas.Task)
async def create_task(
		task_create: schemas.TaskCreate,
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.create_task(db, user, task_create)

@app.put("/task", response_model=schemas.Task)
async def update_task(
		task_update: schemas.TaskUpdate,
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.update_task(db, user, task_update)

@app.delete("/task", response_model=schemas.Task)
async def delete_task(
		task_delete: schemas.TaskDelete,
		db: Annotated[Session, Depends(get_db)],
		user: Annotated[models.User, Depends(get_current_user)]
	):
	return crud.delete_task(db, user, task_delete.uuid)