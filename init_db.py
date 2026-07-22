from database.database import Base, engine
from models.user import User

Base.metadata.create_all(bind=engine)

print("Base de données créée avec succès !")
