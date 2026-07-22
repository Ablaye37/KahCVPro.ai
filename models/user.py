from sqlalchemy import Column, Integer, String
from database.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer,
 primary_key=True, index=True)
    nom = Column(String,
 index=True)
    email = Column(String,
 unique=True, index=True)
    mot_de_passe = Column(String)
