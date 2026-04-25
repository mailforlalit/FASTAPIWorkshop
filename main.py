from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, sessionLocal
from models import TaskDB
from schema import Task
app = FastAPI()

#to create database table
TaskDB.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.session.close()

#tasks = []
@app.get("/") # create a route for home page
def home():
    return {"message": "Welcome to FASTAPI Workshop"}

@app.post("/tasks")
def createtask(task:Task, db: Session = Depends(get_db)):
    new_task = TaskDB(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'message' : 'Task created successfully', 'tasks' : new_task}

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()

