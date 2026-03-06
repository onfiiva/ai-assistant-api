from sqlalchemy import Column, String, Boolean
from app.infra.db.models.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user")
    is_active = Column(Boolean, default=True)
