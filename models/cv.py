from sqlalchemy import Column, Integer, String, Text
from database.database import Base


class CV(Base):
    __tablename__ = "cvs"

    id = Column(Integer, primary_key=True, index=True)

    nom = Column(String)
    email = Column(String)
    telephone = Column(String)

    profil = Column(Text)
    experience = Column(Text)
    formation = Column(Text)
    competences = Column(Text)
