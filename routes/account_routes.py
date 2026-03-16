from flask import Blueprint, jsonify, request
from services.accounts_services import deposit_money, withdraw_money
from services.auth_middleware import token_required
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