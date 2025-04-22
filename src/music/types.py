from typing import List

from pydantic import BaseModel

class UserProfile(BaseModel):
    current_level: str 
    reading_sheet_music: str 
    frequency_of_practice: str 
    time_commitment: str 
    goals: str = ''

class ModuleOutline(BaseModel):
    month: str
    week: str
    title: str
    description: str


class LearningPlanOutline(BaseModel):
    modules: List[ModuleOutline]


class Module(BaseModel):
    month: str
    week: str
    title: str
    content: str