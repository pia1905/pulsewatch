from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.models import User, Preference


router = APIRouter(
    prefix="/api/preferences",
    tags=["Preferences"]
)


@router.get("/")
def get_preferences(
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    preference = (
        db.query(Preference)
        .filter(
            Preference.user_id == user_id
        )
        .first()
    )

    if not preference:

        preference = Preference(
            user_id=user_id,
            price_threshold=3.0,
            volume_threshold=1.5
        )

        db.add(preference)
        db.commit()
        db.refresh(preference)

    return {
        "user_id": user_id,
        "price_threshold": preference.price_threshold,
        "volume_threshold": preference.volume_threshold
    }


@router.put("/")
def update_preferences(
    price_threshold: float,
    volume_threshold: float,
    user_id: int = 1,
    db: Session = Depends(get_db)
):
    if price_threshold <= 0:
        raise HTTPException(
            status_code=400,
            detail="Price threshold must be greater than 0"
        )

    if volume_threshold <= 0:
        raise HTTPException(
            status_code=400,
            detail="Volume threshold must be greater than 0"
        )

    preference = (
        db.query(Preference)
        .filter(
            Preference.user_id == user_id
        )
        .first()
    )

    if not preference:

        preference = Preference(
            user_id=user_id,
            price_threshold=price_threshold,
            volume_threshold=volume_threshold
        )

        db.add(preference)

    else:

        preference.price_threshold = price_threshold
        preference.volume_threshold = volume_threshold

    db.commit()
    db.refresh(preference)

    return {
        "message": "Preferences updated",
        "price_threshold": preference.price_threshold,
        "volume_threshold": preference.volume_threshold
    }