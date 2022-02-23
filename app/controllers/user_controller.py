from flask import jsonify, request
from app.models.user_model import User
from app.configs.database import db
from secrets import token_urlsafe
from app.configs.auth import auth
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta


@auth.login_required
def list_users():
    users = User.query.all()

    return jsonify(users), 200


def welcome():
    return {"msg": "Bem vindo"}


@jwt_required()
def get_profile():
    # user = User.query.filter_by(user_id=user_id).first()
    user_jwt = get_jwt_identity()

    # comparando user['user_ud'] == user_jwt['user_id']

    return jsonify(user_jwt), 200


def login_user():
    data = request.get_json()

    user: User = User.query.filter_by(email=data["email"]).first()

    if not user:
        return {"error": "email not found"}, 401

    if not user.check_password(data["password"]):
        return {"error": "email and password missmatch"}, 401

    token = create_access_token(user, expires_delta=timedelta(minutes=1))

    return {"token": token}, 200


def create_user():
    data = request.get_json()
    data["api_key"] = token_urlsafe(16)

    user = User(**data)

    db.session.add(user)
    db.session.commit()

    return jsonify(user), 201
