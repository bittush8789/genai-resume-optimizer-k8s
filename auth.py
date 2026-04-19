from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import User
import streamlit as st

# Using PBKDF2-SHA256 which is highly secure and avoids bcrypt's length limitations
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, name, email, password):
    hashed_password = get_password_hash(password)
    db_user = User(name=name, email=email, password_hash=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email, password):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return False
    if not verify_password(password, user.password_hash):
        return False
    return user

def init_session_state():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None
    if "user_name" not in st.session_state:
        st.session_state.user_name = None

def login(user):
    st.session_state.authenticated = True
    st.session_state.user_id = user.id
    st.session_state.user_name = user.name

def logout():
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.user_name = None
    st.rerun()
