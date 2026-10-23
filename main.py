from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()   # l'application, c'est l'objet qu'uvicorn charge (main:app)


# "Base de données" temporaire : une liste de dictionnaires en mémoire.
# Elle repart à vide à chaque redémarrage du serveur.
tasks = []

# Compteur qui ne redescend jamais : un id n'est pas réutilisé après un DELETE.
next_id = 1


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str
    done: bool


def find_task(task_id: int):
    # Un seul endroit gère le "introuvable", partagé par GET, PUT et DELETE.
    for task in tasks:
        if task["id"] == task_id:
            return task

    # Rien trouvé : on coupe l'exécution et FastAPI renvoie un 404
    raise HTTPException(status_code=404, detail="Task not found")


@app.get("/health")
def health():
    # Servira plus tard à Docker, à la CI et au cloud pour vérifier que l'app tourne.
    return {"status": "ok"}


@app.get("/tasks")
def list_tasks():
    return tasks


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    global next_id
    new_task = {"id": next_id, "title": task.title, "done": False}
    next_id += 1
    tasks.append(new_task)
    return new_task


@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate):
    # PUT remplace la ressource entière, donc les deux champs sont obligatoires.
    task = find_task(task_id)
    task["title"] = data.title
    task["done"] = data.done
    return task


@app.delete("/tasks/{task_id}", status_code=204) 
def delete_task(task_id: int):       
    task = find_task(task_id)
    tasks.remove(task)

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # {task_id} dans l'URL est récupéré et converti en int.
    # "/tasks/abc" donne un 422 avant même d'entrer dans la fonction.
    return find_task(task_id)