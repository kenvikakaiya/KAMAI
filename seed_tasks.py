from app import app
from extensions import db
from models import Task


tasks_data = [
    {
        "title": "Write a Short Product Description",
        "description": "Write a clear and attractive description of a sample product in 100 to 150 words.",
        "category": "Writing",
        "reward": 50.00
    },
    {
        "title": "Simple Data Entry Task",
        "description": "Enter product information accurately into a spreadsheet.",
        "category": "Data Entry",
        "reward": 75.00
    },
    {
        "title": "Social Media Caption Writing",
        "description": "Create five short and engaging captions for a small business.",
        "category": "Content",
        "reward": 100.00
    },
    {
        "title": "Image Tagging Task",
        "description": "Identify and add suitable tags to a collection of product images.",
        "category": "Image Tagging",
        "reward": 80.00
    },
    {
        "title": "Online Research Task",
        "description": "Find basic information about a list of products and organize the results.",
        "category": "Research",
        "reward": 120.00
    }
]


with app.app_context():

    for task_data in tasks_data:

        existing_task = Task.query.filter_by(
            title=task_data["title"]
        ).first()

        if not existing_task:

            task = Task(
                title=task_data["title"],
                description=task_data["description"],
                category=task_data["category"],
                reward=task_data["reward"],
                is_active=True
            )

            db.session.add(task)

    db.session.commit()

    print("Tasks added successfully!")