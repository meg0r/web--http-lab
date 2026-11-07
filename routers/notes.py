from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from schemas import NoteCreate,NoteUpdate

router = APIRouter(prefix="/notes",tags=["Notes"])

@router.get("/")
def list_notes(cur=Depends(get_db)):
    cur.execute("SELECT * FROM notes ORDER BY id;")
    return cur.fetchall()

@router.post("/")
def create_note(note: NoteCreate,cur=Depends(get_db)):
    cur.execute(
        "INSERT INTO notes (title, content) VALUES (%s, %s) RETURNING id, title, content",
            (note.title, note.content),
        )
    new_note=cur.fetchone()
    return new_note

@router.get("/notes/{id}")
def read_note(id: int,cur=Depends(get_db)):
    cur.execute("SELECT * FROM notes WHERE id = %s", (id,))
    note = cur.fetchone()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/notes/{id}",status_code=204)
def delete_note(id: int,cur=Depends(get_db)):
        cur.execute("DELETE FROM notes WHERE id = %s RETURNING id", (id,))
        deleted_note = cur.fetchone()
        if deleted_note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return

@router.delete("/notes",status_code=204)
def delete_all_notes(cur=Depends(get_db)):
    cur.execute("DELETE  FROM notes")
    return

@router.patch("/notes/{id}")
def patch_note(id: int,note_data: NoteUpdate,cur=Depends(get_db)):
    cur.execute("UPDATE notes SET title = COALESCE(%s,title), content = COALESCE (%s,content) WHERE id = %s RETURNING id,title,content", (note_data.title, note_data.content, id))
    updated_note = cur.fetchone()
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note