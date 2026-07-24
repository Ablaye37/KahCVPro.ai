from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from database.database import SessionLocal
from models.user import User
from models.cv import CV

router = APIRouter()

templates = Jinja2Templates(directory="templates")


@router.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):

    db: Session = SessionLocal()

    users = db.query(User).all()
    cvs = db.query(CV).all()

    nombre_users = len(users)
    nombre_cvs = len(cvs)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="admin.html",
        context={
            "users": users,
            "cvs": cvs,
            "nombre_users": nombre_users,
            "nombre_cvs": nombre_cvs
        }
    )
