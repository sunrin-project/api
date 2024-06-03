from pydantic import BaseModel
from typing import Optional, List


class NewMeal(BaseModel):
    meal: str
    code: Optional[str] = None


class MealScheme(BaseModel):
    id: int
    meal: str
    code: Optional[str] = None


class DateScheme(BaseModel):
    id: int
    date: str
    meals: Optional[List[MealScheme]] = None
    existence: bool


class NewDate(BaseModel):
    date: str
    meals: Optional[List[NewMeal]] = None
    existence: bool
