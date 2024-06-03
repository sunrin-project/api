from sqlalchemy import and_
from sqlalchemy.orm import Session

from schemes.meal_scheme import NewDate, NewMeal
from models.models import Meal, Date
from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'


def insert_meal(new_meal: NewDate, db: Session):
    date = Date(
        date=datetime.strptime(new_meal.date, '%Y-%m-%d'),
        existence=True
    )

    if new_meal.meals:
        for meal in new_meal.meals:
            meal_data = Meal(
                meal=meal.meal,
                code=meal.code,
                date_id=date.id
            )

            date.meals.append(meal_data)

    db.add(date)
    db.commit()
    db.refresh(date)

    return date


def get_all_meal(db: Session):
    lists = db.query(Date).all()

    date_list = []

    for d in lists:
        meal = db.query(Meal).filter(Meal.date_id == d.id).all()

        meal_list = []

        for m in meal:
            meal_list.append(NewMeal(
                meal=m.meal,
                code=m.code,
            ))

        date_list.append(NewDate(
            date=to_date_str(d.date),
            meals=meal_list,
            existence=d.existence
        ))

    return date_list


def get_meal_by_date(date: str, db: Session):
    date = db.query(Date).filter(Date.date == to_date_obj(date)).first()

    meal = db.query(Meal).filter(Meal.date_id == date.id).all()

    meal_list = []

    for m in meal:
        meal_list.append(NewMeal(
            meal=m.meal,
            code=m.code,
        ))

    return NewDate(
        date=to_date_str(date.date),
        meals=meal_list,
        existence=date.existence
    )


def get_meal_by_date_range(date_from: str, date_to: str, db: Session):
    date = db.query(Date).filter(and_(Date.date >= to_date_obj(date_from), Date.date <= to_date_obj(date_to))).all()

    date_list = []

    for d in date:
        meal = db.query(Meal).filter(Meal.date_id == d.id).all()

        meal_list = []

        for m in meal:
            meal_list.append(NewMeal(
                meal=m.meal,
                code=m.code,
            ))

        date_list.append(NewDate(
            date=to_date_str(d.date),
            meals=meal_list,
            existence=d.existence
        ))

    return date_list


def get_meal_by_date_limit(date_from: str, limit: int, db: Session):
    date = db.query(Date).filter(Date.date >= to_date_obj(date_from)).limit(limit).all()

    date_list = []

    for d in date:
        meal = db.query(Meal).filter(Meal.date_id == d.id).all()

        meal_list = []

        for m in meal:
            meal_list.append(NewMeal(
                meal=m.meal,
                code=m.code,
            ))

        date_list.append(NewDate(
            date=to_date_str(d.date),
            meals=meal_list,
            existence=d.existence
        ))

    return date_list


def to_date_obj(date: str):
    return datetime.strptime(date, '%Y-%m-%d')


def to_date_str(date):
    return date.strftime('%Y-%m-%d')
