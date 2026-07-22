from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.user import User

router = APIRouter()
templates = Jinja2Templates(directory="templates")

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse(
        "register.html",
        {"request": request}
    )

@router.post("/register")
async def register(
    nom: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...)
):
    db: Session = SessionLocal()

    user = User(
        nom=nom,
        email=email,
        mot_de_passe=mot_de_passe
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "Inscription réussie !"}
