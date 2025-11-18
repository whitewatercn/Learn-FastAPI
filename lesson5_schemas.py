from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

class Album(BaseModel):
	title:str
	release_date:date

class BandBase(BaseModel):
	name:str
	genre:GeneralURLChoices
	albums:list[Album] = []


class BandCreate(BandBase):
	@field_validator('genre', mode='before')
	@classmethod
	def title_case_genre(cls, value):
		return value.title()  # RoCK -> Rock
	"""
	BandCreate继承了BandBase，并添加了一个字段验证器，用于在创建Band实例时将genre字段转换为标题格式，也就是首字母大写
	这里的validator是pydantic validator v2的用法
	"""


class BandWithID(BandBase):
	id:int