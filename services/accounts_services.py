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

def transfer_money(sender_id,receiver_name,amount):
    if not sender_id or not receiver_name or not amount:
        raise ValueError("RequiredFields Missing")
    conn=connect()
    cursor=conn.cursor()
    try:
        cursor.execute("SELECT id from users WHERE name=?",(receiver_name,))
        receiver=cursor.fetchone()

        if not receiver:
            raise ValueError("Receiver does not exist")
        
        receiver_id=receiver[0]

        if receiver_id==sender_id:
            raise ValueError("Cannot Transfer Money To Your Own Account")
        
        cursor.execute("""
        UPDATE accounts
        SET balance= balance -?
        WHERE user_id =?
        AND balance >=?
        """,(amount,sender_id,amount))

        if cursor.rowcount==0:
            raise ValueError("Insufficient Funds")    

        cursor.execute("""
        UPDATE accounts
        SET balance=balance +?
        WHERE user_id=?
        """,(amount,receiver_id))

        cursor.execute("""
        INSERT INTO transactions
        (sender_id,receiver_id,amount,type)
        VALUES(?,?,?,?)
        """,(sender_id,receiver_id,amount,"transfer"))
        
        conn.commit()
    
    except Exception as e:
        conn.rollback()
        raise ValueError(str(e))
    finally:
        conn.close()
    
    # account_services.py
# Add this function:

def get_user_transactions(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT * FROM transactions
        WHERE sender_id = ?
        OR receiver_id = ?
        ORDER BY created_at DESC
    """, (user_id, user_id))

    transactions = cursor.fetchall()
    conn.close()
    return transactions

def get_all_accounts():
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("SELECT * FROM accounts")
    result=cursor.fetchall()
    conn.close()
    return result 


def admin_get_transactions():
    conn=connect()
    cursor=conn.cursor()
    cursor.execute("""
      SELECT *FROM transactions
      ORDER BY created_at DESC
""")
  
    result=cursor.fetchall()
    conn.close()
    return result