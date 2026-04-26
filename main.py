from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.testing.pickleable import User

from database import engine, sessionLocal
from models import TaskDB
from schema import Task
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth import create_token, verify_jwt
#object creation
app = FastAPI()
security = HTTPBearer()

#to create database table
TaskDB.metadata.create_all(bind=engine)

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.session.close()

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")

    payload = verify_jwt(token)

    if payload is None:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

    return payload

#tasks = []
@app.post("/login")
def login(username: str, password: str):
    if username != 'admin' and password != 'admin123':
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_token({'username': username})
    return {'access_token': token}



@app.get("/") # create a route for home page
def home():
    return {"message": "Welcome to FASTAPI Workshop"}

#@app.post("/tasks")
#def create_task(task:Task, db: Session = Depends(get_db)):
#    new_task = TaskDB(**task.dict())
#    db.add(new_task)
#    db.commit()
#    db.refresh(new_task)
#    return {'message' : 'Task created successfully', 'tasks' : new_task}

@app.post("/tasks")
def create_task(task:Task, db: Session = Depends(get_db),
                user: dict = Depends(verify_token)):
    new_task = TaskDB(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {'message' : 'Task created successfully', 'tasks' : new_task}


#@app.get("/tasks")
#def get_tasks(db: Session = Depends(get_db)):
#    return db.query(TaskDB).all()

@app.get("/tasks")
def get_tasks(db: Session = Depends(get_db),
              user: dict = Depends(verify_token)):
    return db.query(TaskDB).all()

#@app.put("/tasks/{id}")
#def update_task(id:int, task:Task, db:Session= Depends(get_db)):
#    existing_task = db.query(TaskDB).filter(TaskDB.id == id).first()
#    if not existing_task:
#        raise HTTPException(status_code=404, detail="Task not found")
#    existing_task.title = task.title
#    existing_task.description = task.description
#    existing_task.status = task.status
#    db.commit()
#    return {'message' : 'Task updated successfully', 'task' : task.dict()}

@app.put("/tasks/{id}")
def update_task(id:int, task:Task, db:Session= Depends(get_db),
                user: dict = Depends(verify_token)):
    existing_task = db.query(TaskDB).filter(TaskDB.id == id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    existing_task.title = task.title
    existing_task.description = task.description
    existing_task.status = task.status
    db.commit()
    return {'message' : 'Task updated successfully', 'task' : task.dict()}


#@app.delete("/tasks/{id}")
#def delete_task(id:int, db: Session = Depends(get_db)):
#    existing_task = db.query(TaskDB).filter(TaskDB.id == id).first()
#    if not existing_task:
#        raise HTTPException(status_code=404, detail="Task not found")
#    db.delete(existing_task)
#    db.commit()
#    return {'message' : 'Task deleted successfully'}

@app.delete("/tasks/{id}")
def delete_task(id:int, db: Session = Depends(get_db),
                user: dict = Depends(verify_token)):
    existing_task = db.query(TaskDB).filter(TaskDB.id == id).first()
    if not existing_task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(existing_task)
    db.commit()
    return {'message' : 'Task deleted successfully'}



