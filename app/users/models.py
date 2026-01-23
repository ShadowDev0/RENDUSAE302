#!/bin/env python3

from app import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer
from werkzeug.security import generate_password_hash


class Users(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    mot_de_passe: Mapped[str] = mapped_column(String(255), nullable=False)
    role_id: Mapped[int] = mapped_column(Integer, db.ForeignKey("roles.id"), nullable=False)

    @staticmethod
    def create_user(nom,password,role_id):
        id_role = ["1","2","3"]
        if role_id in id_role:
            user = Users(nom=nom, mot_de_passe=generate_password_hash(password),role_id=role_id)
            db.session.add(user)
            db.session.commit()
            return user
        return "Id de role incorrect"

    @staticmethod
    def delete_user(id_compte):
        user = Users.query.get(id_compte)
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return "Account successfully delete"
        return "Account not found"

    @staticmethod
    def maj_user(id, nom, mot_de_passe, role_id):
        user = Users.query.get(id)
        if user is not None:
            user.nom = nom
            user.mot_de_passe = generate_password_hash(mot_de_passe)
            user.role_id = role_id
            db.session.commit()
            return "Account Updated"
        return "Account not found"

    @staticmethod
    def get_role_id(user_id):
        user = Users.query.get(user_id)
        if user is not None:
            return user.role_id
        return None

class Roles(db.Model):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(50), nullable=False)