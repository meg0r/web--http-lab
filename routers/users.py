from fastapi import APIRouter, Depends, HTTPException
from typing import List
from database import get_db
from schemas import UserResponse
from auth import get_current_user

from database import get_db
from schemas import UserResponse

router = APIRouter(prefix="/users",tags=["users"])

@router.get("/",response_model=List[UserResponse])
def get_all_users(current_user: dict = Depends(get_current_user),cur=Depends(get_db)):
    cur.execute("SELECT id,email FROM users")
    return cur.fetchall()

@router.get("/{user_id}",response_model=UserResponse)
def get_user(user_id: int,cur=Depends(get_db),current_user:dict = Depends(get_current_user)):
    cur.execute("SELECT id,email FROM users WHERE id = %s",(user_id,))
    user= cur.fetchone()
    if user is None:
        raise HTTPException(status_code=404,detail="Пользователь с данным id не найден")
    return user
