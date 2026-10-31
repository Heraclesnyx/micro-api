import os
from sqlalchemy import create_engine


database_url = os.getenv("DATABASE_URL")  # On récupère la configuration

if not database_url:
    raise ValueError("DATABASE_URL is not set")  # On vérifie qu'elle existe

engine = create_engine(database_url) # On crée le moteur de connexion à la BDD.