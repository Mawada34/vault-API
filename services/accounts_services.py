from flask import Flask
from db.db_helper import connect


def deposit_money(user_id,amount):
    if not user_id or not amount:
        raise ValueError("Required fields missing")
    
    conn=connect()
    cursor=conn.cursor()
    
    
    cursor.execute("""
       UPDATE accounts
       SET balance= balance + ?
       WHERE user_id=?
     """,(amount,user_id))
    
    conn.commit()

    cursor.execute("SELECT balance FROM accounts WHERE user_id=?",(user_id,))
    result=cursor.fetchone()
    
    conn.close()
    return result

def withdraw_money(user_id,amount):
    if not user_id or not amount:
        raise ValueError("Required fields missing")
    
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""
    UPDATE accounts
    SET balance= balance -?
    WHERE user_id =?
    AND balance >=?
""",(amount,user_id,amount))
    
    conn.commit()

    cursor.execute("SELECT balance FROM accounts WHERE user_id=?",(user_id,))
    result=cursor.fetchone()
    
    conn.close()
    return result

