from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    make_response,
    g,
    current_app,
)

from .extensions import db
from .models import User
from .auth import (
    generate_token,
    login_required,
    admin_required,
)

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    user = getattr(g, "user", None)

    if user:
        return redirect("/dashboard")

    return redirect("/login")


@main_bp.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        client_ip = request.headers.get("X-Real-IP", request.remote_addr)

        user = User.query.filter_by(
            username=username,
            is_active=True,
        ).first()

        if not user or not user.verify_password(password):
            current_app.auth_logger.warning(
                "LOGIN_FAILED ip=%s username=%s path=/login",
                client_ip,
                username or "-",
            )
            error = "Неверный логин или пароль"
            return render_template("login.html", error=error), 401

        token = generate_token(
            user.id,
            user.username,
            user.is_admin,
        )

        response = make_response(redirect("/dashboard"))
        response.set_cookie(
            "auth_token",
            token,
            httponly=True,
            samesite="Lax",
            secure=False,
            max_age=60 * current_app.config["TOKEN_EXPIRE_MINUTES"],
        )

        return response

    return render_template("login.html", error=error)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template(
        "dashboard.html",
        username=g.user["username"],
        is_admin=g.user.get("is_admin", False),
    )


@main_bp.route("/admin")
@login_required
@admin_required
def admin_panel():
    users = User.query.order_by(User.id).all()

    return render_template(
        "admin.html",
        users=users,
    )


@main_bp.route("/admin/create-user", methods=["POST"])
@login_required
@admin_required
def create_user():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    is_admin = bool(request.form.get("is_admin"))

    if not username or not password:
        return redirect("/admin")

    existing = User.query.filter_by(username=username).first()

    if existing:
        return redirect("/admin")

    user = User(
        username=username,
        is_admin=is_admin,
        is_active=True,
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return redirect("/admin")


@main_bp.route("/admin/toggle-user/<int:user_id>", methods=["POST"])
@login_required
@admin_required
def toggle_user(user_id: int):
    user = User.query.get_or_404(user_id)

    user.is_active = not user.is_active

    db.session.commit()

    return redirect("/admin")


@main_bp.route("/logout")
def logout():
    response = make_response(redirect("/login"))
    response.set_cookie("auth_token", "", expires=0)

    return response
