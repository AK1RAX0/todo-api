from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Todo API")

# задачи храним в списке
tasks = []
next_id = 1


class TaskCreate(BaseModel):
    title: str


class Task(BaseModel):
    id: int
    title: str
    done: bool = False


@app.get("/")
def root():
    return {"message": "Todo API работает! Документация: /docs"}


@app.get("/tasks", response_model=list[Task])
def get_tasks():
    return tasks


@app.post("/tasks", response_model=Task, status_code=201)
def create_task(data: TaskCreate):
    global next_id
    task = Task(id=next_id, title=data.title)
    tasks.append(task)
    next_id += 1
    return task


@app.put("/tasks/{task_id}", response_model=Task)
def complete_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            task.done = True
            return task
    raise HTTPException(status_code=404, detail="Задача не найдена")


@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task.id == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail="Задача не найдена")