from flask import jsonify
from functools import wraps
from db.db_helper import connect

#The Logic Begins Here 
def role_required(required_role):
    def decorator(f):
        @wraps(f)
        def decorated(user_id,*args,**kwargs):

            conn=connect()
            cursor=conn.cursor()

            cursor.execute("SELECT role FROM users WHERE id=?",(user_id,))

            user=cursor.fetchone()
            conn.close()

            if not user:
                return jsonify ({"error":"user not found"}),404
            
            user_role=user[0]

            if user_role != required_role:
                return jsonify({"error":f"Access Forbidden {required_role}s only"}),403
            
            
            return f(user_id,*args,**kwargs)  
        return decorated
    return decorator