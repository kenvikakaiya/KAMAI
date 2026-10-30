from datetime import datetime
from sqlalchemy import UniqueConstraint
from extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=False)
    reward = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    deadline = db.Column(db.DateTime, nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    assignments = db.relationship(
        "TaskAssignment",
        back_populates="task",
        cascade="all, delete-orphan"
    )


class TaskAssignment(db.Model):
    __tablename__ = "task_assignments"

    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(
        db.Integer,
        db.ForeignKey("tasks.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )
    status = db.Column(db.String(30), default="accepted")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    task = db.relationship(
        "Task",
        back_populates="assignments"
    )

    user = db.relationship(
        "User",
        back_populates="task_assignments"
    )

    __table_args__ = (
        UniqueConstraint(
            "task_id",
            "user_id",
            name="unique_user_task"
        ),
    )