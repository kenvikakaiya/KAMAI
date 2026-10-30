
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from extensions import db
from models import Task, TaskAssignment


tasks = Blueprint("tasks", __name__)


@tasks.route("/tasks")
@login_required
def task_list():

    available_tasks = Task.query.filter_by(
        is_active=True
    ).all()

    accepted_assignments = TaskAssignment.query.filter_by(
        user_id=current_user.id
    ).all()

    accepted_task_ids = {
        assignment.task_id
        for assignment in accepted_assignments
    }

    return render_template(
        "tasks.html",
        tasks=available_tasks,
        accepted_task_ids=accepted_task_ids
    )


@tasks.route("/tasks/<int:task_id>")
@login_required
def task_detail(task_id):

    task = Task.query.get_or_404(task_id)

    assignment = TaskAssignment.query.filter_by(
        task_id=task.id,
        user_id=current_user.id
    ).first()

    return render_template(
        "task_detail.html",
        task=task,
        assignment=assignment
    )


@tasks.route("/tasks/<int:task_id>/accept", methods=["POST"])
@login_required
def accept_task(task_id):

    task = Task.query.get_or_404(task_id)

    if not task.is_active:
        flash(
            "This task is no longer available.",
            "error"
        )
        return redirect(url_for("tasks.task_list"))

    existing_assignment = TaskAssignment.query.filter_by(
        task_id=task.id,
        user_id=current_user.id
    ).first()

    if existing_assignment:
        flash(
            "You have already accepted this task.",
            "info"
        )
        return redirect(
            url_for("tasks.task_detail", task_id=task.id)
        )

    assignment = TaskAssignment(
        task_id=task.id,
        user_id=current_user.id,
        status="accepted"
    )

    try:
        db.session.add(assignment)
        db.session.commit()

        flash(
            "Task accepted successfully!",
            "success"
        )

    except IntegrityError:
        db.session.rollback()

        flash(
            "You have already accepted this task.",
            "info"
        )

    except Exception:
        db.session.rollback()

        current_app.logger.exception(
            "Failed to accept task %s",
            task_id
        )

        flash(
            "Could not accept this task. Please try again.",
            "error"
        )

    return redirect(
        url_for("tasks.task_detail", task_id=task.id)
    )
