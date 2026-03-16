import jwt
import bcrypt
import datetime
from db.db_helper import connect
from config import SECRET_KEY

def register_user(name,password):
    if not name or not password :
        raise ValueError("Name and Password required")
    
    conn=connect()
    cursor=conn.cursor()

    try:
        hashed=bcrypt.hashpw(password.encode(),bcrypt.gensalt())
        cursor.execute("INSERT INTO users(name,password) VALUES(?,?)",(name,hashed))
        #Get the new user id
        user_id=cursor.lastrowid #<-gets id just inserted

        #Auto create Bank account
        cursor.execute("INSERT INTO accounts(user_id, balance) VALUES(?,?)",
            (user_id, 0))             # ← starts at 0")
        conn.commit()
    
    except Exception as e:
        raise ValueError("User already Exists")
    
    finally:
        conn.close()

def login_user(name,password):
    conn=connect()
    cursor=conn.cursor()

    
    cursor.execute("SELECT id,password FROM users WHERE name=?",(name,))
    user=cursor.fetchone()
            
    conn.close()

    if not user:
        raise ValueError("Invlid Credentials")
   
    user_id=user[0]
    hashed=user[1]

    
    if not bcrypt.checkpw(password.encode(),hashed):
        raise ValueError("Invalid Credentials")
            
    token=jwt.encode(
        {
            "user_id":user_id,
            "exp":datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
         SECRET_KEY,
        algorithm="HS256"
    )

    return token

