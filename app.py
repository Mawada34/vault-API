from db.db_helper import connect


def deposit_money(name,amount):
    if name and amount is None:
        raise ValueError("Name and Amount Required")
    
    conn=connect()
    cursor=conn.cursor()
    
    
    cursor.execute("""
       UPDATE accounts
       SET balance= balance + ?
       WHERE name=?
     """,(name,amount))
    
    conn.commit()

    cursor.execute("SELECT name,balance FROM accounts WHERE name=?",(name,))
    user=cursor.fetchone()
    
    conn.close()
    return user

def withdraw_money(name,amount):
    if not name or amount is None:
        raise ValueError("Name and amount required")
    
    conn=connect()
    cursor=conn.cursor()

    cursor.execute("""
    UPDATE accounts
    SET balance= balance -?
    WHERE name =?
    AND balance = >?
""",(amount,name,amount))
    
    conn.commit()

    cursor.execute("SELECT name,balance FROM accounts WHERE name=?",(name,))
    user=cursor.fetchone()
    
    conn.close()
    return user
