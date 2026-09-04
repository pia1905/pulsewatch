from database import SessionLocal
from models.models import User


db = SessionLocal()

existing_user = db.query(User).filter(User.id == 1).first()

if not existing_user:
    user = User(
        name="Demo User",
        email="demo@pulsewatch.com"
    )

    db.add(user)
    db.commit()

    print("Demo user created successfully!")

else:
    print("Demo user already exists.")

db.close()