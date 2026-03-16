from flask import Flask,jsonify,request
from app import deposit_money,withdraw_money

app=Flask(__name__)

@app.route("/deposit",methods=["POST"])
def deposit():
    data=request.json or {}
    name=data.get("name")
    amount=data.get("amount")

    try:
        if name and amount is None:
            raise ValueError("Name and Amount Required")
    
        deposit_money(name,float(amount))
        return jsonify({"message":"Deposit Successful"}),200

    except Exception as e:
        return jsonify({"error":str(e)}),400
    


@app.route("/withdraw",methods=["POST"])
def withdraw():
    data=request.json or {}
    name=data.get("name")
    amount=data.get("amount")

    try:
        if name or amount is None:
         raise ValueError("Name and Amount Required")
    
        withdraw_money(name,float(amount))
        return jsonify({"message":"Withdrawal Successful"}),200

    except Exception as e:
        return jsonify({"error":str(e)}),400
