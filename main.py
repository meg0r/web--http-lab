from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from database import get_db
from typing import Optional

app = FastAPI(title="Notes API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def start_menu():
    return "Welcome to Notes API"

@app.get("/hello")
def ping():
    return {"message": "Hello from Notes API"}

class NoteCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=80)
    content: str = Field(..., min_length=1, max_length=500)

@app.get("/notes")
def list_notes(cur=Depends(get_db)):
    cur.execute("SELECT * FROM notes ORDER BY id;")
    return cur.fetchall

@app.post("/notes", status_code=201)
def create_note(note: NoteCreate,cur=Depends(get_db)):
    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, title, content",
            (note.title, note.content),
        )
    new_note=cur.fetchone()
    return new_note

@app.get("/notes/{id}")
def read_note(id: int,cur=Depends(get_db)):
    cur.execute("SELECT * FROM notes WHERE id = %s", (id,))
    note = cur.fetchone()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note

@app.delete("/notes/{id}",status_code=204)
def delete_note(id: int,cur=Depends(get_db)):
        cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (id,))
        deleted_note = cur.fetchone()
        if deleted_note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return

@app.delete("/notes",status_code=204)
def delete_all_notes():
    with psycopg.connect(DATABASE_URL,row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE  FROM notes")
            conn.commit()
    return

class NoteUpdate(BaseModel):
    title: str = Field(None, min_length=1, max_length=80)
    content: str = Field(None, min_length=1, max_length=500)

@app.patch("/notes/{id}")
def patch_note(id: int,note_data: NoteUpdate):
    with psycopg.connect(DATABASE_URL, row_factory=dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE notes SET title = COALESCE(%s,title), content = COALESCE (%s,content) WHERE id = %s RETURNING id,title,content", (note_data.title, note_data.content, id))
            updated_note = cur.fetchone()
        if updated_note is None:
            raise HTTPException(status_code=404, detail="Note not found")
    return updated_note