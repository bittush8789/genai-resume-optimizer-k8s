import pytest
from database import init_db, SessionLocal, User


def test_db_initializes():
    """DB tables should be created without errors."""
    init_db()


def test_create_and_query_user():
    """Should be able to insert and retrieve a user."""
    init_db()
    db = SessionLocal()
    user = User(email="test@ci.com", hashed_password="hashed123", full_name="CI User")
    db.add(user)
    db.commit()
    db.refresh(user)

    fetched = db.query(User).filter(User.email == "test@ci.com").first()
    assert fetched is not None
    assert fetched.full_name == "CI User"

    db.delete(fetched)
    db.commit()
    db.close()
