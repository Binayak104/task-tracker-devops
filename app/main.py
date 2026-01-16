from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()
conn = sqlite3.connect("tasks.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
)
""")

class Task(BaseModel):
    title: str

@app.post("/tasks")
def create_task(task: Task):
    cur.execute("INSERT INTO tasks (title) VALUES (?)", (task.title,))
    conn.commit()
    return {"message": "Task created"}

@app.get("/tasks")
def get_tasks():
    cur.execute("SELECT id, title FROM tasks")
    return [{"id": r[0], "title": r[1]} for r in cur.fetchall()]