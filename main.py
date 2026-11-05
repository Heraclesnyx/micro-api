from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Session
from sqlalchemy import select

from db import get_db, engine
from models import Task, Base



# Définit les actions a effectuer au démarrage et l'arrêt de l'application
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Création de la base de données définie dans le fichier db.py si elles n'existent pas.
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)   # l'application, c'est l'objet qu'uvicorn charge (main:app)

class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool

class TaskRead(BaseModel):
    id: int
    title: str
    model_config = ConfigDict(from_attributes=True)
    done: bool



def get_task_or_404(db: Session, task_id: int) -> Task:
    # Un seul endroit gère le "introuvable", partagé par GET, PUT et DELETE
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/health")
def health():
    # Servira plus tard à Docker, à la CI et au cloud pour vérifier que l'app tourne.
    return {"status": "ok"}


@app.get("/tasks", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db)):
    return db.scalars(select(Task).order_by(Task.id)).all()


@app.post("/tasks", status_code=201, response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db)):

    # Créer un objet SQLAlchemy à partir des données reçues
    new_task = Task(title=task.title)

    # Ajouter le nouvel objet à la session
    db.add(new_task)

    # Enregistrer les changements dans la base de données
    db.commit()

    # Récupérer les valeurs générées par la base de données
    db.refresh(new_task)

    return new_task
    

@app.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: int, db: Session = Depends(get_db)):
    return get_task_or_404(db, task_id)


@app.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int,data: TaskUpdate ,db: Session = Depends(get_db)):

    task = get_task_or_404(db, task_id)
    task.title = data.title
    task.done = data.done
    db.commit()
    return task


@app.delete("/tasks/{task_id}", status_code=204) 
def delete_task(task_id: int, db: Session = Depends(get_db)):

    task = get_task_or_404(db, task_id)

    # Suppression de la tâche
    db.delete(task)
    db.commit()
   
    


