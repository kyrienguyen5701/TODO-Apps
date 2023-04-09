from fastapi import FastAPI, Depends, Request, Form, status

from starlette.responses import RedirectResponse
from starlette.templating import Jinja2Templates

from sqlalchemy.orm import Session

import models
from database import SessionLocal, engine

# create all db tables
models.Base.metadata.create_all(bind=engine)

# get the templates for rendering HTML
templates = Jinja2Templates(directory='templates')

app = FastAPI()

# Dependency
# if cannot access db, throw an error
def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get('/')
def home(request: Request, db: Session = Depends(get_db)):
  todos = db.query(models.Todo).all()
  
  # return a template with information passing in a dictionary
  return templates.TemplateResponse(
    'base.html',
    {
      'request': request,
      'todo_list': todos
    }
  )

@app.post('/add')
def add(request: Request, title: str=Form(), db: Session=Depends(get_db)):
  new_todo = models.Todo(title=title)
  db.add(new_todo)
  db.commit()
  
  return RedirectResponse(url=app.url_path_for('home'), status_code=status.HTTP_303_SEE_OTHER)

@app.get('/update/{todo_id}')
def add(request: Request, todo_id: int, db: Session=Depends(get_db)):
  todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
  todo.finished = not todo.finished
  db.commit()
  
  return RedirectResponse(url=app.url_path_for('home'), status_code=status.HTTP_302_FOUND)

@app.get('/update/{todo_id}')
def add(request: Request, todo_id: int, db: Session=Depends(get_db)):
  todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
  db.delete(todo)
  db.commit()
  
  return RedirectResponse(url=app.url_path_for('home'), status_code=status.HTTP_302_FOUND)
