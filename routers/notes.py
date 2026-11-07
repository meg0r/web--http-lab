from fastapi import APIRouter,Depends,HTTPException
from database import get_db
from schemas import NoteCreate,NoteUpdate
from auth import get_current_user

router = APIRouter(prefix="/notes",tags=["Notes"])

@router.get("/")
def list_notes(cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
    cur.execute("SELECT * FROM notes WHERE user_id=%s ORDER BY id;",(current_user["id"],))
    return cur.fetchall()

@router.post("/",status_code=201)
def create_note(note: NoteCreate,cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
    cur.execute(
        "INSERT INTO notes (title, content,user_id) VALUES (%s, %s, %s) RETURNING id, title, content",
            (note.title, note.content,current_user["id"]),
        )
    new_note=cur.fetchone()
    return new_note

@router.get("/{id}")
def read_note(id: int,cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
    cur.execute("SELECT * FROM notes WHERE id = %s AND user_id = %s", (id,current_user["id"]))
    note = cur.fetchone()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.delete("/{id}",status_code=204)
def delete_note(id: int,cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
        cur.execute("DELETE FROM notes WHERE id = %s AND user_id = %s RETURNING id", (id,current_user["id"]))
        deleted_note = cur.fetchone()
        if deleted_note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return

@router.delete("/",status_code=204)
def delete_all_notes(cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
    cur.execute("DELETE  FROM notes WHERE user_id=%s",(current_user["id"],))
    return

@router.patch("/{id}")
def patch_note(id: int,note_data: NoteUpdate,cur=Depends(get_db),current_user: dict = Depends(get_current_user)):
    cur.execute("UPDATE notes SET title = COALESCE(%s,title), content = COALESCE (%s,content) WHERE id = %s AND user_id=%s RETURNING id,title,content", (note_data.title, note_data.content, id,current_user["id"]))
    updated_note = cur.fetchone()
    if updated_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note