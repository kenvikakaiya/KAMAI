from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from extensions import db
from models import User


auth = Blueprint("auth", __name__)


def get_reset_serializer():
    from flask import current_app

    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )


@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not username or not email or not password:
            flash("Please fill in all required fields.", "error")
            return redirect(url_for("auth.register"))

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect(url_for("auth.register"))

        existing_user = User.query.filter(
            (User.username == username) |
            (User.email == email)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "error")
            return redirect(url_for("auth.register"))

        user = User(
            username=username,
            email=email,
            role="earner"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully. Please log in.", "success")

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):

           login_user(user)

        if user.role == "admin":
            return redirect(url_for("admin.submissions"))

        return redirect(url_for("dashboard"))
        flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth.route("/logout", methods=["POST"])
def logout():
    logout_user()
    flash("You have been logged out successfully.", "success")
    return redirect(url_for("auth.login"))

# -------------------------------------------------
# FORGOT PASSWORD
# -------------------------------------------------

@auth.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()

        user = User.query.filter_by(email=email).first()

        if not user:
            flash(
                "If an account exists with this email, "
                "a password reset link has been generated.",
                "info"
            )
            return redirect(url_for("auth.forgot_password"))

        serializer = get_reset_serializer()

        token = serializer.dumps(
            user.email,
            salt="password-reset"
        )

        reset_link = url_for(
            "auth.reset_password",
            token=token,
            _external=True
        )

        # For local development/testing
        print("\n========================================")
        print("PASSWORD RESET LINK")
        print(reset_link)
        print("========================================\n")

        flash(
            "Password reset link has been generated. "
            "Check the terminal for the link.",
            "success"
        )

        return redirect(url_for("auth.forgot_password"))

    return render_template("forgot_password.html")


@auth.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    serializer = get_reset_serializer()

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=1800
        )

    except SignatureExpired:

        flash(
            "This password reset link has expired.",
            "error"
        )

        return redirect(url_for("auth.forgot_password"))

    except BadSignature:

        flash(
            "Invalid password reset link.",
            "error"
        )

        return redirect(url_for("auth.forgot_password"))

    user = User.query.filter_by(email=email).first()

    if not user:

        flash(
            "User account was not found.",
            "error"
        )

        return redirect(url_for("auth.forgot_password"))

    if request.method == "POST":

        password = request.form.get("password", "")
        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not password:

            flash(
                "Please enter a new password.",
                "error"
            )

            return redirect(
                url_for(
                    "auth.reset_password",
                    token=token
                )
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for(
                    "auth.reset_password",
                    token=token
                )
            )

        user.set_password(password)

        db.session.commit()

        flash(
            "Your password has been reset successfully. "
            "Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "reset_password.html"
    )