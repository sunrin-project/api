from typing import Optional, List, Any

from pydantic import BaseModel


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
    meals: Optional[List[NewMeal]] = []
    existence: bool
    rest: bool


class NewDate(BaseModel):
    date: str
    meals: Optional[List[NewMeal]] = []
    existence: bool
    rest: bool


class SuccessScheme(BaseModel):
    success: bool = True
    data: Any = None


class SuccessDayCountScheme(BaseModel):
    success: bool = True
    data: List[NewDate] = []
    day_count: int = None


class ErrorScheme(BaseModel):
    success: bool = False
    message: str = None


ResponseScheme = SuccessScheme | SuccessDayCountScheme | ErrorScheme
