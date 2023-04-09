from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# db config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create db model
class Todo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  finished = db.Column(db.Boolean)
  
# create db
app.app_context().push()
db.create_all()

@app.get('/')
def home():
  todo_list = db.session.query(Todo).all()
  return render_template('base.html', todo_list=todo_list)

@app.post('/add')
def add():
  
  # get form with name 'title'
  title = request.form.get('title')
  
  # create and add a new task
  new_todo = Todo(title=title, finished=False)
  db.session.add(new_todo)
  
  # commit change
  db.session.commit()
  
  # redirect to index
  return redirect(url_for('home'))

@app.get('/update/<int:todo_id>')
def update(todo_id):
  todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
  todo.finished = not todo.finished
  db.session.commit()
  return redirect(url_for('home'))

@app.get('/remove/<int:todo_id>')
def remove(todo_id):
  todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
  db.session.delete(todo)
  db.session.commit()
  return redirect(url_for('home'))
