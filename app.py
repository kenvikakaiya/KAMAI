
import os

from flask import Flask, render_template
from flask_login import login_required, current_user

from config import Config
from extensions import db, login_manager, csrf

from models import (
    User,
    Task
)

from routes.auth import auth
from routes.tasks import tasks
from routes.wallet import wallet
from routes.my_work import my_work
from routes.submissions import submissions
from routes.admin import admin

def create_app():
    app = Flask(__name__)
    print("APP ROOT:", app.root_path)
    print("TEMPLATE FOLDER:", app.template_folder)
    print("TEMPLATE PATH:", app.jinja_loader.searchpath)

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "error"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    app.register_blueprint(auth)
    app.register_blueprint(tasks)  
    app.register_blueprint(wallet)
    app.register_blueprint(my_work)
    app.register_blueprint(submissions)
    app.register_blueprint(admin)
    @app.route("/")
    def home():
        return render_template("index.html")

    @app.route("/dashboard")
    @login_required
    def dashboard():
        total_tasks = Task.query.count()

        full_name = (
            current_user.profile.full_name
            if current_user.profile
            else current_user.username
        )

        wallet_balance = (
        current_user.wallet.available_balance
        if current_user.wallet
        else 0
     )

        return render_template(
            "dashboard.html",
            full_name=full_name,
            wallet_balance=wallet_balance,
            total_tasks=total_tasks
        )

    @app.route("/health")
    def health():
        return {
            "status": "success",
            "message": "Kamai application is running!"
        }

    with app.app_context():
        db.create_all()

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)