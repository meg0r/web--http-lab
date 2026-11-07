from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db
from schemas import UserCreate, UserResponse, Token, NoteCreate
from auth import get_password_hash, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(note: UserCreate, cur=Depends(get_db)):
    cur.execute("SELECT * FROM users WHERE email = %s", (note.email,))
    if cur.fetchone():
        raise HTTPException(status_code=400,detail="Этот адрес электронной почты уже занят")
    hashed_pwd = get_password_hash(note.password)
    cur.execute('INSERT INTO users (email, password_hash) VALUES (%s, %s) RETURNING id,email',(note.email, hashed_pwd))
    new_user = cur.fetchone()
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),cur=Depends(get_db)):
    cur.execute("SELECT * FROM users WHERE email = %s", (form_data.username,))
    user = cur.fetchone()

    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=400,detail="Неправильный адрес электронной почты или пароль")
    token = create_access_token(data={"sub": user["email"],"user_id":user["id"]})
    return {"access_token":token,"token_type":"bearer"}

@router.get("/me",response_model=UserResponse)
def read_users_me(current_user:dict = Depends(get_current_user)):
    return current_user

