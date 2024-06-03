from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import meal_crud
from database.database import get_db

app = APIRouter(
    prefix='/lunch',
    tags=['lunch'],
)


@app.get('/')
async def get_lunch(db: Session = Depends(get_db)):
    try:
        today = datetime.now().strftime('%Y-%m-%d')

        return {'success': True, 'data': meal_crud.get_meal_by_date(today, db)}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.get('/period')
async def get_lunch_range(startDate: Optional[str] = None, numOfDays: int = 6, db: Session = Depends(get_db)):
    try:
        if not startDate:
            startDate = datetime.now().strftime('%Y-%m-%d')

        data = meal_crud.get_meal_by_date_limit(startDate, numOfDays, db)
        return {'success': True, 'data': data, 'day_count': len(data)}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.get('/week')
async def get_lunch_week(db: Session = Depends(get_db)):
    try:
        today = datetime.now()

        weekday = today.weekday()

        monday = today - timedelta(days=weekday)
        sunday = monday + timedelta(days=6)

        monday_str = monday.strftime('%Y-%m-%d')
        sunday_str = sunday.strftime('%Y-%m-%d')

        data = meal_crud.get_meal_by_date_range(monday_str, sunday_str, db)
        return {'success': True, 'data': data, 'day_count': len(data)}
    except Exception as e:
        return {'success': False, 'message': str(e)}
