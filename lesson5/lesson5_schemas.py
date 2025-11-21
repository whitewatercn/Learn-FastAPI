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

	@field_validator('genre', mode='before')
	@classmethod
	def _normalize_genre(cls, value):
		"""Normalize incoming genre strings so they match enum values.

		Examples: 'Rock' -> 'rock', 'Progressive Rock' -> 'progressive_rock'
		"""
		if isinstance(value, str):
			return value.strip().lower().replace(' ', '_')
		return value


class BandCreate(BandBase):
	# BandCreate 保留以便作为创建输入模型；
	# `genre` 的规范化在 `BandBase` 的 `_normalize_genre` 中完成。
	"""
	BandCreate 继承自 BandBase，用作创建接口的输入模型。
	`genre` 的规范化（把 "Rock" -> "rock"、把空格换成下划线）由
	 `BandBase._normalize_genre` 处理，因此这里不需要额外的验证器。
	"""


class BandWithID(BandBase):
	id:int
	"""
	BandWithID继承了BandBase，并添加了一个id字段，用于表示乐队的唯一标识符
	"""