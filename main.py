from fastapi import FastAPI, HTTPException, Depends
from routers import notes, auth, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Notes API", version="0.1.0")

app.include_router(notes.router)
app.include_router(auth.router)
app.include_router(users.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Разрешаем запросы с любых адресов (для учебы сойдет)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/")
def start_menu():
    return "Welcome to Notes API"

@app.get("/hello")
def ping():
    return {"message": "Hello from Notes API"}