from typing import Optional

from sqlalchemy.orm import Session

from database.database import get_db
from database import meal_crud

from fastapi import APIRouter, Depends, HTTPException

from schemes.meal_scheme import NewDate
import os
from dotenv import load_dotenv

load_dotenv()

app = APIRouter(
    prefix='/meal',
    tags=['meal'],
    include_in_schema=False
)

"""
from, to
"""


@app.get('/list')
async def get_all_meal(db: Session = Depends(get_db)):
    try:
        data = meal_crud.get_all_meal(db)
        return {'success': True, 'data': data}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.get('/')
async def get_meal(date: str, db: Session = Depends(get_db)):
    try:
        return {'success': True, 'data': meal_crud.get_meal_by_date(date, db)}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.get('/period')
async def get_meal_range(date_from: str, date_to: str, db: Session = Depends(get_db)):
    try:
        data = meal_crud.get_meal_by_date_range(date_from, date_to, db)
        return {'success': True, 'data': data}
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.get('/limit')
async def get_meal_period(date_from: str, limit: int, db: Session = Depends(get_db)):
    try:
        data = meal_crud.get_meal_by_date_limit(date_from, limit, db)

        return {
            'success': True,
            'data': data,
            'day_count': len(data)
        }
    except Exception as e:
        return {'success': False, 'message': str(e)}


@app.post('/')
async def insert_meal(new_meal: NewDate, password: Optional[str] = None, db: Session = Depends(get_db)):
    if password != os.environ.get('PASSWORD'):
        raise HTTPException(status_code=401, detail='Unauthorized')
    else:
        try:
            return {'success': True, 'data': meal_crud.insert_meal(new_meal, db)}
        except Exception as e:
            return {'success': False, 'message': str(e)}
