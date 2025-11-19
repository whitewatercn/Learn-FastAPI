"""
lesson7开始，用sqlmodel来定义模型（基于sqlmodel），而不是以前的basemodel（基于pydantic）
从这节课开始，使用sql数据库了（这次使用的是sqlite）
"""
from datetime import date
from enum import Enum
from pydantic import BaseModel, field_validator
from sqlmodel import SQLModel, Field,Relationship

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

class AlbumBase(SQLModel):
	title:str
	release_date:date
	band_id: int = Field(foreign_key="band.id")
	"""
	AlbumBase定义了专辑的基本属性，还有一个外键band_id，关联到Band表的id字段
	这意味着每个album必须绑定一个已有的band_id
	如果album绑定一个不存在的band_id，数据库会报错
	"""
class AlbumCreate(SQLModel):
	title:str
	release_date:date

class Album(AlbumBase,table=True):
	id:int = Field(default=None, primary_key=True)
	band: "Band" = Relationship(back_populates="albums")
	"""
	Album继承自AlbumBase，并添加了一个id字段作为主键
	还定义了一个关系band，表示这个专辑属于哪个乐队
	"""
class BandBase(SQLModel):
	name:str
	genre:GeneralURLChoices


class BandCreate(BandBase):
	albums:list[AlbumCreate] | None = None

	@field_validator('genre', mode='before')
	@classmethod
	def title_case_genre(cls, value):
		return value.title()  # RoCK -> Rock
	


class Band(BandBase, table=True):
	id:int = Field(default=None, primary_key=True)
	albums: list[Album] = Relationship(back_populates="band")

	"""
	Band继承自BandBase，并添加了一个id字段作为主键
	还定义了一个关系albums，表示这个乐队有哪些专辑
	"""