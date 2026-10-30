from flask import Blueprint, render_template
from flask_login import login_required, current_user

wallet = Blueprint("wallet", __name__)


@wallet.route("/wallet")
@login_required
def wallet_page():
    wallet_data = current_user.wallet

    balance = wallet_data.available_balance if wallet_data else 0
    pending = wallet_data.pending_balance if wallet_data else 0
    transactions = wallet_data.transactions if wallet_data else []

    return render_template(
        "wallet.html",
        balance=balance,
        pending=pending,
        transactions=transactions
    )