from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import os
import psycopg
from psycopg.rows import dict_row
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

app = FastAPI(title="Notes API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def ping():
    return {"message": "Hello from Notes API"}

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)

@app.get("/notes")
def list_notes():
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM notes ORDER BY id;")
            notes = cur.fetchall()
    return notes

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, title, content",
                (note.title, note.content),
            )
            new_note = cur.fetchone()
            conn.commit()
    return new_note

@app.get("/notes/{id}")
def read_note(id: int):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM notes WHERE id = %s", (id,))
            note = cur.fetchone()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note