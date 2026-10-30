from datetime import datetime
from decimal import Decimal
from extensions import db


class Service(db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)

    description = db.Column(db.Text, nullable=False)

    price = db.Column(
        db.Numeric(10, 2),
        default=Decimal("0.00"),
        nullable=False
    )

    city = db.Column(db.String(100))
    image = db.Column(db.String(255))

    status = db.Column(
        db.String(30),
        default="pending",
        nullable=False
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship(
        "User",
        back_populates="services"
    )

    def __repr__(self):
        return f"<Service {self.title}>"