from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer

class Machines(db.Model):
    __tablename__ = "machines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    ip: Mapped[str] = mapped_column(String(15), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False, default="#d1e7dd")