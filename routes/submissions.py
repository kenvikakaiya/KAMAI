
from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user
from sqlalchemy import update

from extensions import db
from models import Task, TaskAssignment, Submission


submissions = Blueprint("submissions", __name__)


@submissions.route(
    "/tasks/<int:task_id>/submit",
    methods=["GET", "POST"]
)
@login_required
def submit_work(task_id):

    task = Task.query.get_or_404(task_id)

    assignment = TaskAssignment.query.filter_by(
        task_id=task.id,
        user_id=current_user.id
    ).first()

    if not assignment:
        flash(
            "You must accept this task before submitting your work.",
            "error"
        )
        return redirect(
            url_for("tasks.task_detail", task_id=task.id)
        )

    existing_submission = Submission.query.filter_by(
        assignment_id=assignment.id
    ).order_by(
        Submission.created_at.desc(),
        Submission.id.desc()
    ).first()

    # Prevent another submission while one is pending.
    if (
        existing_submission
        and existing_submission.status == "pending"
    ):
        flash(
            "Your submission is already under review.",
            "info"
        )
        return redirect(
            url_for(
                "submissions.submission_status",
                submission_id=existing_submission.id
            )
        )

    # Prevent submitting an already completed task.
    if assignment.status == "completed":
        flash(
            "You have already completed this task.",
            "info"
        )
        return redirect(
            url_for("tasks.task_detail", task_id=task.id)
        )

    # Only accepted tasks can receive a new submission.
    if assignment.status != "accepted":
        flash(
            "You cannot submit this task in its current status.",
            "error"
        )
        return redirect(
            url_for("tasks.task_detail", task_id=task.id)
        )

    if request.method == "POST":

        content = request.form.get("content", "").strip()

        if not content:
            flash(
                "Please enter your completed work.",
                "error"
            )
            return render_template(
                "submit_work.html",
                task=task,
                submission=existing_submission
            ), 400

        if len(content) < 10:
            flash(
                "Please provide at least 10 characters describing your completed work.",
                "error"
            )
            return render_template(
                "submit_work.html",
                task=task,
                submission=existing_submission
            ), 400

        if len(content) > 5000:
            flash(
                "Your submission must be 5000 characters or fewer.",
                "error"
            )
            return render_template(
                "submit_work.html",
                task=task,
                submission=existing_submission
            ), 400

        try:
            # Atomically claim the accepted assignment.
            claimed = db.session.execute(
                update(TaskAssignment)
                .where(
                    TaskAssignment.id == assignment.id,
                    TaskAssignment.user_id == current_user.id,
                    TaskAssignment.status == "accepted"
                )
                .values(status="submitted")
            )

            if claimed.rowcount != 1:
                db.session.rollback()

                flash(
                    "This task has already been submitted or its status has changed.",
                    "info"
                )
                return redirect(
                    url_for("tasks.task_detail", task_id=task.id)
                )

            submission = Submission(
                assignment_id=assignment.id,
                task_id=task.id,
                user_id=current_user.id,
                content=content,
                status="pending"
            )

            db.session.add(submission)
            db.session.commit()

            flash(
                "Your work has been submitted successfully!",
                "success"
            )

            return redirect(
                url_for(
                    "submissions.submission_status",
                    submission_id=submission.id
                )
            )

        except Exception:
            db.session.rollback()

            current_app.logger.exception(
                "Failed to submit work for task %s",
                task_id
            )

            flash(
                "We could not submit your work. Please try again.",
                "error"
            )

            return render_template(
                "submit_work.html",
                task=task,
                submission=existing_submission
            ), 500

    return render_template(
        "submit_work.html",
        task=task,
        submission=existing_submission
    )


@submissions.route("/submissions/<int:submission_id>")
@login_required
def submission_status(submission_id):

    submission = Submission.query.get_or_404(submission_id)

    # Users can only view their own submissions.
    if submission.user_id != current_user.id:
        flash(
            "You cannot view this submission.",
            "error"
        )
        return redirect(
            url_for("my_work.my_work_page")
        )

    return render_template(
        "submission_status.html",
        submission=submission
    )
