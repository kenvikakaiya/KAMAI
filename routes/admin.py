
from decimal import Decimal

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app
)

from flask_login import login_required, current_user
from sqlalchemy import update

from extensions import db
from models import Submission, TaskAssignment, Wallet, Transaction


admin = Blueprint("admin", __name__)


def is_admin():
    return (
        current_user.is_authenticated
        and current_user.role == "admin"
    )


@admin.route("/admin/submissions")
@login_required
def submissions():

    if not is_admin():
        flash(
            "You are not authorized to access the admin panel.",
            "error"
        )
        return redirect(url_for("dashboard"))

    pending_submissions = Submission.query.filter_by(
        status="pending"
    ).order_by(
        Submission.created_at.desc()
    ).all()

    return render_template(
        "admin_submission.html",
        submissions=pending_submissions
    )


@admin.route(
    "/admin/submissions/<int:submission_id>/approve",
    methods=["POST"]
)
@login_required
def approve_submission(submission_id):

    if not is_admin():
        flash(
            "You are not authorized to perform this action.",
            "error"
        )
        return redirect(url_for("dashboard"))

    try:
        # Claim the submission only if it is still pending.
        claimed = db.session.execute(
            update(Submission)
            .where(
                Submission.id == submission_id,
                Submission.status == "pending"
            )
            .values(status="processing")
        )

        if claimed.rowcount != 1:
            db.session.rollback()
            flash(
                "This submission has already been reviewed or is unavailable.",
                "info"
            )
            return redirect(url_for("admin.submissions"))

        submission = Submission.query.populate_existing().filter_by(
            id=submission_id
        ).first()

        if not submission:
            raise ValueError("Submission not found.")

        task = submission.task
        user = submission.user

        if not task or not user:
            raise ValueError("Task or user information is missing.")

        # Verify that this submission belongs to the correct assignment.
        assignment = db.session.get(
            TaskAssignment,
            submission.assignment_id
        )

        if (
            not assignment
            or assignment.task_id != submission.task_id
            or assignment.user_id != submission.user_id
            or assignment.status != "submitted"
        ):
            raise ValueError("Task assignment is invalid.")

        # Validate the task reward.
        reward = Decimal(str(task.reward))

        if not reward.is_finite() or reward <= Decimal("0.00"):
            raise ValueError("Invalid task reward.")

        # Get or create the user's wallet.
        wallet = Wallet.query.filter_by(
            user_id=user.id
        ).first()

        if not wallet:
            wallet = Wallet(
                user_id=user.id,
                available_balance=Decimal("0.00"),
                pending_balance=Decimal("0.00")
            )
            db.session.add(wallet)
            db.session.flush()

        if wallet.available_balance is None:
            raise ValueError("Wallet balance is invalid.")

        # Credit the reward.
        wallet.available_balance = (
            wallet.available_balance + reward
        )

        # Record the payment.
        transaction = Transaction(
            wallet_id=wallet.id,
            amount=reward,
            transaction_type="task_earning",
            description=f"Earning from task: {task.title}"
        )

        db.session.add(transaction)

        # Update submission and assignment.
        submission.status = "approved"
        submission.feedback = (
            "Your work has been approved. "
            "The reward has been added to your wallet."
        )

        assignment.status = "completed"

        # Save payment and status changes together.
        db.session.commit()

        flash(
            "Submission approved and reward added to the user's wallet.",
            "success"
        )

    except Exception:
        db.session.rollback()

        current_app.logger.exception(
            "Failed to approve submission %s",
            submission_id
        )

        flash(
            "Could not approve this submission. No payment was confirmed.",
            "error"
        )

    return redirect(url_for("admin.submissions"))


@admin.route(
    "/admin/submissions/<int:submission_id>/reject",
    methods=["POST"]
)
@login_required
def reject_submission(submission_id):

    if not is_admin():
        flash(
            "You are not authorized to perform this action.",
            "error"
        )
        return redirect(url_for("dashboard"))

    try:
        # Reject only if the submission is still pending.
        claimed = db.session.execute(
            update(Submission)
            .where(
                Submission.id == submission_id,
                Submission.status == "pending"
            )
            .values(
                status="rejected",
                feedback=(
                    "Your submission needs improvement. "
                    "Please review the task requirements and submit again."
                )
            )
        )

        if claimed.rowcount != 1:
            db.session.rollback()
            flash(
                "This submission has already been reviewed.",
                "info"
            )
            return redirect(url_for("admin.submissions"))

        submission = Submission.query.populate_existing().filter_by(
            id=submission_id
        ).first()

        if not submission:
            raise ValueError("Submission not found.")

        assignment = db.session.get(
            TaskAssignment,
            submission.assignment_id
        )

        if (
            not assignment
            or assignment.task_id != submission.task_id
            or assignment.user_id != submission.user_id
            or assignment.status != "submitted"
        ):
            raise ValueError("Task assignment is invalid.")

        # Allow the earner to submit the work again.
        assignment.status = "accepted"

        db.session.commit()

        flash(
            "Submission rejected. The user can submit the work again.",
            "info"
        )

    except Exception:
        db.session.rollback()

        current_app.logger.exception(
            "Failed to reject submission %s",
            submission_id
        )

        flash(
            "Could not reject this submission.",
            "error"
        )

    return redirect(url_for("admin.submissions"))
