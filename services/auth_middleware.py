from flask import jsonify,request
from config import SECRET_KEY
from functools import wraps
import jwt

def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth_header=request.headers.get("Authorization")

        if not auth_header:
            return jsonify({"error":"Token is Missing"}),401
        
        try:
            token=auth_header.split(" ")[1]
        except IndexError:
            return jsonify({"error":"Invalid Token Format"}),401
        
        try:
            data=jwt.decode(
                token,
                SECRET_KEY,
                algorithms=["HS256"]
            )
        except jwt.ExpiredSignatureError:
            return jsonify({"error":"Expired Token.Login Again"}),401
        
        except jwt.InvalidTokenError:
            return jsonify({"error":"Invalid Token"}),401
        
        user_id=data.get("user_id")

        return f(user_id,*args,**kwargs)
    return decorated    







