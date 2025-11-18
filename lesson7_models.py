from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field,Relationship

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

class GeneralChoices(Enum):
	ROCK = "Rock"
	PROGRESSIVE_ROCK = "Progressive Rock"
	HIP_HOP = "Hip_Hop"

class AlbumBase(SQLModel):
	title:str
	release_date:date
	band_id: int = Field(foreign_key="band.id")

class AlbumCreate(SQLModel):
	title:str
	release_date:date

class Album(AlbumBase,table=True):
	id:int = Field(default=None, primary_key=True)
	band: "Band" = Relationship(back_populates="albums")

class BandBase(SQLModel):
	name:str
	genre:GeneralChoices


class BandCreate(BandBase):
	albums:list[AlbumCreate] | None = None

	@field_validator('genre', mode='before')
	@classmethod
	def title_case_genre(cls, value):
		return value.title()  # RoCK -> Rock
	


class Band(BandBase, table=True):
	id:int = Field(default=None, primary_key=True)
	albums: list[Album] = Relationship(back_populates="band")