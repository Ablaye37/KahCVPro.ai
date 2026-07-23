from fastapi.responses import FileResponse
from reportlab.pdfgen import canvas
from services.ai_service import ameliorer_cv

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.cv import CV

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/create-cv", response_class=HTMLResponse)
async def create_cv_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="create_cv.html"
    )


@router.post("/create-cv")
async def save_cv(
    nom: str = Form(...),
    email: str = Form(...),
    telephone: str = Form(...),
    profil: str = Form(...),
    experience: str = Form(...),
    formation: str = Form(...),
    competences: str = Form(...)
):

    db: Session = SessionLocal()

    cv = CV(
        nom=nom,
        email=email,
        telephone=telephone,
        profil=profil,
        experience=experience,
        formation=formation,
        competences=competences
    )

    db.add(cv)
    db.commit()
    db.close()

    return {
        "message": "CV enregistré avec succès !"
    }
@router.get("/my-cv", response_class=HTMLResponse)
async def my_cv(request: Request):
    db: Session = SessionLocal()

    cv = db.query(CV).all()

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="my_cv.html",
        context={
            "cvs": cv
        }
    )
@router.get("/download-cv/{cv_id}")
async def download_cv(cv_id: int):

    db: Session = SessionLocal()

    cv = db.query(CV).filter(CV.id == cv_id).first()

    db.close()

    if cv is None:
        return {"message": "CV introuvable"}

    filename = f"cv_{cv.id}.pdf"

    pdf = canvas.Canvas(filename)

    pdf.drawString(50, 800, f"Nom : {cv.nom}")
    pdf.drawString(50, 770, f"Email : {cv.email}")
    pdf.drawString(50, 740, f"Telephone : {cv.telephone}")

    pdf.drawString(50, 700, "Profil :")
    pdf.drawString(50, 670, cv.profil)

    pdf.drawString(50, 630, "Experience :")
    pdf.drawString(50, 600, cv.experience)

    pdf.drawString(50, 560, "Formation :")
    pdf.drawString(50, 530, cv.formation)

    pdf.drawString(50, 490, "Competences :")
    pdf.drawString(50, 460, cv.competences)

    pdf.save()

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )

@router.get("/improve-cv/{cv_id}")
async def improve_cv(cv_id: int):

    db: Session = SessionLocal()

    cv = db.query(CV).filter(CV.id == cv_id).first()

    if cv is None:
        db.close()
        return {"message": "CV introuvable"}

    cv.profil = ameliorer_cv(cv.profil)

    db.commit()
    db.close()

    return {
        "message": "CV amélioré avec succès !"
    }
