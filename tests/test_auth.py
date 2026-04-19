import pytest
from auth import get_password_hash, verify_password, create_user, authenticate_user
from database import init_db, SessionLocal


def test_password_hash_and_verify():
    """Hashed password should verify correctly."""
    password = "MySecurePassword123!"
    hashed = get_password_hash(password)
    assert hashed != password
    assert verify_password(password, hashed)


def test_wrong_password_fails():
    """Wrong password should not verify."""
    hashed = get_password_hash("correct-password")
    assert not verify_password("wrong-password", hashed)


def test_create_and_authenticate_user():
    """Created user should be authenticatable."""
    init_db()
    db = SessionLocal()

    user = create_user(db, email="auth_test@ci.com", password="TestPass@123", full_name="Auth Tester")
    assert user is not None
    assert user.email == "auth_test@ci.com"

    authenticated = authenticate_user(db, "auth_test@ci.com", "TestPass@123")
    assert authenticated is not False

    db.delete(user)
    db.commit()
    db.close()
