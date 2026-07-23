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
        request=request,
        name="register.html"
    )


@router.post("/register")
async def register(
    nom: str = Form(...),
    email: str = Form(...),
    mot_de_passe: str = Form(...)
):
    db: Session = SessionLocal()

    # Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        db.close()
        return {"message": "Cet email est déjà utilisé."}

    user = User(
        nom=nom,
        email=email,
        mot_de_passe=mot_de_passe
    )

    db.add(user)
    db.commit()
    db.close()

    return {"message": "Inscription réussie !"}


@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html"
    )


@router.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    mot_de_passe: str = Form(...)
):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == email).first()

    db.close()

    if user is None:
        return {"message": "Email introuvable"}

    if user.mot_de_passe != mot_de_passe:
        return {"message": "Mot de passe incorrect"}

    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "nom": user.nom
        }
    )
