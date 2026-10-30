from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models import TaskAssignment


my_work = Blueprint("my_work", __name__)


@my_work.route("/my-work")
@login_required
def my_work_page():

    assignments = TaskAssignment.query.filter_by(
        user_id=current_user.id
    ).order_by(
        TaskAssignment.created_at.desc()
    ).all()

    return render_template(
        "my_work.html",
        assignments=assignments
    )