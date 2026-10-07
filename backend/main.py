from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models

Base.metadata.create_all(bind=engine)
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/check-ins")
def create_check_in(feeling: str, note: str | None=None, db: Session=Depends(get_db)):
    check_in = models.CheckIn(feeling=feeling, note=note)

    db.add(check_in)
    db.commit()
    db.refresh(check_in)

    return check_in

@app.get("/check-ins")
def get_check_in(db: Session=Depends(get_db)):
    return db.query(models.CheckIn).order_by(
        models.CheckIn.created_at.desc()
    ).all()

@app.get("/")
def root():
    return {
        "message": "Hello from Asahi"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }