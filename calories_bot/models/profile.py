from typing import Optional

from pydantic import BaseModel, Field


class Profile(BaseModel):
    user_id: int
    active: bool = Field(default=False)
    weight: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    age: Optional[int] = Field(default=None)
    activity: Optional[int] = Field(default=None)
    city: Optional[str] = Field(default=None)
    lat: Optional[float] = Field(default=None)
    lon: Optional[float] = Field(default=None)
    water_goal: Optional[int] = Field(default=None)
    calorie_goal: Optional[int] = Field(default=None)
    logged_water: int = Field(default=0)
    logged_calories: int = Field(default=0)
    burned_calories: int = Field(default=0)

    def get_default_calorie_goal(self):
        return 10 * self.weight + 6.25 * self.height - 5 * self.age

    def get_default_water_goal(self, temperature: float):
        high_temp_addition = 750 if temperature > 25 else 0
        return self.weight * 30 + 500 * self.activity / 30 + high_temp_addition


class ActiveProfile(Profile):
    active: bool = True
    weight: int
    height: int
    age: int
    activity: int
    city: str
    lat: float
    lon: float
    water_goal: int
    calorie_goal: int
