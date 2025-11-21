from datetime import date
from enum import Enum
from pydantic import BaseModel

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

class Album(BaseModel):
	title:str
	release_date:date

class Band(BaseModel):
	id:int
	name:str
	genre:str
	albums:list[Album] = []