from flask import Blueprint,jsonify,request
from services.auth_services import register_user,login_user

auth=Blueprint("auth",__name__)

@auth.route("/register",methods=["POST"])
def register():
    data=request.json or {}

    try:
        register_user(data.get("name"),data.get("password"))
        return jsonify ({"message":"User Created"}),201
    except Exception as e:
        return jsonify({"error":str(e)}),400

@auth.route("/login",methods=["POST"])
def login():
    data=request.json or {}

    try:
        token=login_user(data.get("name"),data.get("password"))
        return jsonify({"token":token}),200

    except Exception as e:
        return jsonify({"error":str(e)}),400


