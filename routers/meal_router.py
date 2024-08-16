import os
from datetime import datetime, timedelta

from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session

from database import meal_crud
from database.database import get_db
from decorators.handle_exceptions import handle_exceptions
from schemes.meal_scheme import NewDate, SuccessScheme, ErrorScheme, SuccessDayCountScheme, ResponseScheme

load_dotenv()

app = APIRouter(
    prefix='/meal',
    tags=['meal'],
)


@app.get('/list')
@handle_exceptions
async def get_all_meal(db: Session = Depends(get_db)) -> ResponseScheme:
    data = meal_crud.get_all_meal(db)
    return SuccessDayCountScheme(
        data=data,
        day_count=len(data)
    )


@app.get('')
@handle_exceptions
async def get_meal(date: str, db: Session = Depends(get_db)) -> ResponseScheme:
    data = meal_crud.get_meal_by_date(date, db)
    return SuccessScheme(
        data=data
    )


@app.get('/today')
@handle_exceptions
async def get_today_meal(db: Session = Depends(get_db)) -> ResponseScheme:
    today = datetime.now().strftime('%Y-%m-%d')
    data = meal_crud.get_meal_by_date(today, db)
    return SuccessScheme(
        success=True,
        data=data
    )


@app.get('/yesterday')
@handle_exceptions
async def get_yesterday_meal(db: Session = Depends(get_db)) -> ResponseScheme:
    yesterday = datetime.now() - timedelta(days=1)
    yesterday_str = yesterday.strftime('%Y-%m-%d')
    data = meal_crud.get_meal_by_date(yesterday_str, db)
    return SuccessScheme(
        data=data
    )


@app.get('/tomorrow')
@handle_exceptions
async def get_tomorrow_meal(db: Session = Depends(get_db)) -> ResponseScheme:
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_str = tomorrow.strftime('%Y-%m-%d')
    data = meal_crud.get_meal_by_date(tomorrow_str, db)
    return SuccessScheme(
        data=data
    )


@app.get('/week')
@handle_exceptions
async def get_lunch_week(db: Session = Depends(get_db)) -> ResponseScheme:
    today = datetime.now()
    weekday = today.weekday()
    monday = today - timedelta(days=weekday)
    sunday = monday + timedelta(days=6)
    monday_str = monday.strftime('%Y-%m-%d')
    sunday_str = sunday.strftime('%Y-%m-%d')
    data = meal_crud.get_meal_by_date_range(monday_str, sunday_str, db)
    return SuccessDayCountScheme(
        data=data,
        day_count=len(data)
    )


@app.get('/month')
@handle_exceptions
async def get_lunch_month(db: Session = Depends(get_db)) -> ResponseScheme:
    today = datetime.now()
    month = today.month
    year = today.year
    last_day = 31

    if month == 2:
        if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
            last_day = 29
        else:
            last_day = 28
    elif month in [4, 6, 9, 11]:
        last_day = 30

    first_day = datetime(year, month, 1)
    last_day = datetime(year, month, last_day)

    first_day_str = first_day.strftime('%Y-%m-%d')
    last_day_str = last_day.strftime('%Y-%m-%d')

    data = meal_crud.get_meal_by_date_range(first_day_str, last_day_str, db)
    return SuccessDayCountScheme(
        data=data,
        day_count=len(data)
    )


@app.get('/period')
@handle_exceptions
async def get_meal_range(date_from: str, date_to: str, db: Session = Depends(get_db)) -> ResponseScheme:
    data = meal_crud.get_meal_by_date_range(date_from, date_to, db)
    return SuccessScheme(
        data=data
    )


@app.get('/limit')
@handle_exceptions
async def get_meal_period(date_from: str, limit: int, db: Session = Depends(get_db)) -> ResponseScheme:
    data = meal_crud.get_meal_by_date_limit(date_from, limit, db)
    return SuccessDayCountScheme(
        data=data,
        day_count=len(data)
    )


@app.post('')
@handle_exceptions
async def insert_meal(new_meal: NewDate, st_key: str = Header(None), db: Session = Depends(get_db)) -> ResponseScheme:
    if st_key != os.environ.get('KEY'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        data = meal_crud.insert_meal(new_meal, db)
        return SuccessScheme(
            data=data
        )


@app.put('')
@handle_exceptions
async def update_meal(new_meal: NewDate, st_key: str = Header(None), db: Session = Depends(get_db)) -> ResponseScheme:
    if st_key != os.environ.get('KEY'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        data = meal_crud.update_meal_by_date(new_meal, db)
        return SuccessScheme(
            data=data
        )


@app.delete('')
@handle_exceptions
async def delete_meal(date: str, st_key: str = Header(None), db: Session = Depends(get_db)) -> ResponseScheme:
    if st_key != os.environ.get('KEY'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        data = meal_crud.delete_meal_by_date(date, db)
        return SuccessScheme(
            data=data
        )
