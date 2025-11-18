from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

class GeneralChoices(Enum):
	ROCK = "Rock"
	PROGRESSIVE_ROCK = "Progressive Rock"
	HIP_HOP = "Hip_Hop"

class Album(BaseModel):
	title:str
	release_date:date

class BandBase(BaseModel):
	name:str
	genre:GeneralChoices
	albums:list[Album] = []


class BandCreate(BandBase):
	@field_validator('genre', mode='before')
	@classmethod
	def title_case_genre(cls, value):
		return value.title()  # RoCK -> Rock
	


class BandWithID(BandBase):
	id:int