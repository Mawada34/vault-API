from flask import Blueprint, jsonify, request
from services.accounts_services import deposit_money, withdraw_money,transfer_money,get_user_transactions,get_all_accounts,admin_get_transactions
from services.auth_middleware import token_required
from services.role_middleware import role_required
from db.db_helper import connect

account = Blueprint("account", __name__)


@account.route("/balance", methods=["GET"])
@token_required
def get_balance(user_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT balance FROM accounts WHERE user_id=?",
        (user_id,)
    )

    result = cursor.fetchone()
    conn.close()

    if not result:
        return jsonify({
            "error": "Account not found"
        }), 404

    return jsonify({
        "balance": result[0],
        "user_id": user_id
    }), 200


@account.route("/deposit", methods=["POST"])
@token_required
def deposit(user_id):
    data = request.json or {}
    amount = data.get("amount")

    try:
        if not amount:
            raise ValueError("Amount required")

        deposit_money(user_id, float(amount))
        return jsonify({
            "message": "Deposit Successful"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@account.route("/withdraw", methods=["POST"])
@token_required
def withdraw(user_id):
    data = request.json or {}
    amount = data.get("amount")

    try:
        if not amount:
            raise ValueError("Amount required")

        withdraw_money(user_id, float(amount))
        return jsonify({
            "message": "Withdrawal Successful"
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@account.route("/transfer",methods=["POST"])
@token_required

def transfer(user_id):
    data=request.json or {}

    receiver_name=data.get("receiver_name")
    amount=data.get("amount")

    if not receiver_name or not amount:
        return jsonify({"error":"Receiver name and Amount Required"}),400
    try:
        transfer_money(
            user_id,
            receiver_name,
            float(amount)
        )
        return jsonify({
            "Message":"Transfer Successful"
        }),200
    
    except Exception as e:
        return jsonify({"error":str(e)}),400


@account.route("/transactions",methods=["GET"])
@token_required


def get_transactions(user_id):
    transactions = get_user_transactions(user_id)

    if not transactions:
        return jsonify({
            "message": "No transactions found yet"
        }), 200

    return jsonify({
        "transactions": transactions
    }), 200


@account.route("/accounts/admin",methods=["GET"])
@token_required
@role_required("admin")

def get_accounts(user_id):
    accounts= get_all_accounts()

    if not accounts:
        return jsonify({
        "message":"No accounts"}),200
    return jsonify({"accounts":accounts}),200
    

@account.route("/transactions/admin",methods=["GET"])
@token_required
@role_required("admin")

def admin_transactions(user_id):
    transactions=admin_get_transactions()

    if not transactions:
        return jsonify({"message":"No transactions Found"}),200
    return jsonify({"transactions":transactions}),200 

