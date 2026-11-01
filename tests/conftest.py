import os


# On définit SQLite comme base de test par défaut
# seulement si DATABASE_URL n'est pas défini
os.environ.setdefault(
    "DATABASE_URL",
    "sqlite://",
)
from models import Base
from db import get_db
from main import app
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
import pytest



# Fixture utilisé par les tests pour préparer le nettoyage de la BDD
@pytest.fixture(autouse=True)
def db_session():

    # On crée une base SQLite en mémoire pour les tests
    # StaticPool permet de réutiliser la même base pendant les tests
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False}, poolclass=StaticPool
    )


    # On crée les tables à partir des modèles SQLAlchemy
    Base.metadata.create_all(bind=engine)

    # On prépare une fabrique qui permettra de créer des sessions
    SessionLocal = sessionmaker(bind=engine, autoflush=False)



    # On remplace la dépendance get_db de l'application 
    # pour que les routes utilisent la base SQLite de test
    def override_get_db():
        db = SessionLocal()
        try:
            # On fournit la session à la route
            yield db
        finally:
            # On ferme la session après utilisation
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    try:
        # On laisse le test s'exécuter avec la base de test
        yield
    finally:
        # On retire le remplacement de get_db
        app.dependency_overrides.pop(get_db, None)

        # On supprime les tables après les tests
        Base.metadata.drop_all(bind=engine)
    