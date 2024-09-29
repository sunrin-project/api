from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import and_
from sqlalchemy.orm import Session

from exceptions.meal_exceptions import MealNotFoundException
from models.models import Meal, Date
from schemes.meal_scheme import NewDate, NewMeal

DATE_FORMAT = '%Y-%m-%d'


def insert_meal(new_meal: NewDate, db: Session):
    date = Date(
        date=datetime.strptime(new_meal.date, '%Y-%m-%d'),
        existence=new_meal.existence
    )

    if new_meal.meals:
        for meal in new_meal.meals:
            if meal.code == '' or meal.meal == '':
                raise HTTPException(status_code=400, detail='meal and code must not be empty')
            meal_data = Meal(
                meal=meal.meal,
                code=meal.code,
                date_id=date.id
            )

            date.meals.append(meal_data)

    db.add(date)
    db.commit()
    db.refresh(date)

    return NewDate(
        date=to_date_str(date.date),
        meals=new_meal.meals,
        existence=date.existence
    )


def get_all_meal(db: Session):
    lists = db.query(Date).order_by(Date.date.asc()).all()

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
    found_date = db.query(Date).filter(Date.date == to_date_obj(date)).first()

    if not found_date:
        raise MealNotFoundException(
            message=f'Meal with date {date} not found'
        )

    meal = db.query(Meal).filter(Meal.date_id == found_date.id).all()

    meal_list = []

    for m in meal:
        meal_list.append(NewMeal(
            meal=m.meal,
            code=m.code,
        ))

    return NewDate(
        date=to_date_str(found_date.date),
        meals=meal_list,
        existence=found_date.existence
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


def update_meal_by_date(new_meal: NewDate, db: Session):
    date = new_meal.date

    found_date = db.query(Date).filter(Date.date == to_date_obj(date)).first()

    if not found_date:
        raise MealNotFoundException(
            message=f'Meal with date {date} not found'
        )

    found_date.existence = new_meal.existence

    if new_meal.meals:
        previous_meal = db.query(Meal).filter(Meal.date_id == found_date.id).all()
        for p in previous_meal:
            db.delete(p)

        meal_list = []
        for meal in new_meal.meals:
            meal_data = Meal(
                meal=meal.meal,
                code=meal.code,
                date_id=found_date.id
            )

            meal_list.append(meal_data)

        found_date.meals = meal_list

    db.commit()
    db.refresh(found_date)

    return NewDate(
        date=to_date_str(found_date.date),
        meals=new_meal.meals,
        existence=found_date.existence
    )


def delete_meal_by_date(date: str, db: Session):
    found_date = db.query(Date).filter(Date.date == to_date_obj(date)).first()

    if not found_date:
        raise MealNotFoundException(
            message=f'Meal with date {date} not found'
        )

    meals = db.query(Meal).filter(Meal.date_id == found_date.id).all()
    for m in meals:
        db.delete(m)

    db.delete(found_date)
    db.commit()

    return True

def get_rest_day_in_month(year: int, month: int, db: Session):
    date = db.query(Date).filter(and_(Date.date >= to_date_obj(f'{year}-{month}-01'), Date.date <= to_date_obj(f'{year}-{month}-31'))).all()

    date_list = []

    for d in date:
        if not d.existence:
            meal = db.query(Meal).filter(Meal.date_id == d.id).first()

            date_list.append(NewDate(
                date=to_date_str(d.date),
                meals=meal.meal,
                existence=d.existence
            ))

    return date_list



def to_date_obj(date: str):
    return datetime.strptime(date, '%Y-%m-%d')


def to_date_str(date):
    return date.strftime('%Y-%m-%d')
