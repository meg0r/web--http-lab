from fastapi import FastAPI, Response,HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI(title="Notes API", version="0.1.0")

@app.get("/health")
def health_check():
    return {"status": "ok"}
@app.get("/hello")
def ping():
    return {"message": "Hello from Notes API"}

class NoteCreate(BaseModel):
    title: str = Field(...,min_length=1, max_length=80)
    content: str = Field(...,min_length=1, max_length=500)

notes = []

next_id = 1

@app.get("/notes")
def list_notes():
    return notes

@app.post("/notes",status_code=201)
def create_note(note: NoteCreate):
    global next_id
    new_note=note.dict()
    new_note["id"] = next_id
    notes.append(new_note)

    next_id+=1
    return new_note

@app.get("/notes/{id}")
def read_note(id: int):
    for note in notes:
        if note["id"] == id:
            return note
    raise HTTPException(status_code=404, detail="Note not found")