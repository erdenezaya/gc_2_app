# tests/conftest.py
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app, db as _db
from app.models import User

# ------------------------------------------------------------------  
# Flask app for tests – uses an in-memory SQLite DB
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret",
    )
    # one global app-context for the whole session
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()

# ------------------------------------------------------------------  
# Create tables once
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def db(app):
    _db.create_all()
    return _db

# ------------------------------------------------------------------  
# Roll back everything done in each test
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    SessionRegistry = scoped_session(sessionmaker(bind=connection))
    db.session = SessionRegistry         # <- registry (callable), not instance

    yield SessionRegistry

    SessionRegistry.remove()             # flush/close
    transaction.rollback()
    connection.close()

# ------------------------------------------------------------------  
# Factory helper: make_user(...)
# ------------------------------------------------------------------
@pytest.fixture
def make_user(db):
    def _factory(username="alice", email="a@ex.com", pwd="secret"):
        u = User(username=username, email=email)
        u.set_password(pwd)
        db.session.add(u)
        db.session.commit()
        return u
    return _factory
