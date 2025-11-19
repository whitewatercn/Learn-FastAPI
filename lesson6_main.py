"""
本节学习annotated type（从3.5开始支持）以及装饰器（见lesson6_decorator.py）
"""

from fastapi import FastAPI, HTTPException, Path, Query
from enum import Enum
from lesson5_schemas import BandBase, BandCreate,BandWithID,GeneralURLChoices
from typing import Annotated


app = FastAPI()

BANDS= [
	{'id':1 , 'name':'The Beatles', 'genre':'Rock','albums':[
		{'title':'Abbey Road', 'release_date':'1969-09-26'},
		{'title':'Let It Be', 'release_date':'1970-05-08'}
	]},
	{'id':2 , 'name':'Led Zeppelin', 'genre':'Rock','albums':[
		{'title':'Led Zeppelin IV', 'release_date':'1971-11-08'},
		{'title':'Physical Graffiti', 'release_date':'1975-02-24'}
	]},
	{'id':3 , 'name':'Pink Floyd', 'genre':'Progressive Rock','albums':[
		{'title':'The Dark Side of the Moon', 'release_date':'1973-03-01'},
		{'title':'Wish You Were Here', 'release_date':'1975-09-12'}
	]},
	{'id':4 , 'name':'Wu-Tang Clan', 'genre':'Hip_Hop','albums':[]}

]

@app.get("/bands",)
async def bands(
	genre:GeneralURLChoices | None = None,
	q: Annotated[str | None, Query(max_length=10)] = None,
)  -> list[BandWithID]:
	"""
	lesson6比lesson5增加了一个查询用的q，且使用Query（max_length=10）来限制查询参数q的长度
	使用案例如：127.0.0.1:8000/bands?q=beatles
	止于Query是如何实现的？请看fastapi源码，我是看不下去，你可以试试：）
	"""
	band_list = [BandWithID(**band) for band in BANDS]

	if genre:
		band_list = [ band for band in band_list if band.genre.value.lower() == genre.value.lower() ]
	if q:
		band_list = [ band for band in band_list if q.lower() in band.name.lower() ]
	
	return band_list

@app.get("/bands/{band_id}")
async def band(band_id: Annotated[int, Path(title='The band ID')]) -> BandWithID:
	"""
	这里给band_id添加了Path(title='The band ID')，这样在自动生成的swagger文档里会显示"The band ID"说明
	"""
	band = next((BandWithID(**band) for band in BANDS if band['id'] == band_id), None)
	if band is None:
		raise HTTPException(status_code=404, detail="Band not found")
	return band

@app.get('/bands/genre/{genre_name}')
async def bands_for_genre(genre_name: str) -> list[dict]:
	# 验证 genre_name 是否有效，但不暴露有效值列表
	valid_genres = [genre.value for genre in GeneralURLChoices]
	if genre_name not in valid_genres:
		raise HTTPException(status_code=404, detail="Genre not found")
	
	result = [
		band for band in BANDS if band['genre'].lower() == genre_name.lower()
	]
	if not result:
		raise HTTPException(status_code=404, detail="No bands found")
	return result


@app.post('/bands')
async def create_band(band_data:BandCreate) -> BandWithID:
	id = BANDS[-1]['id'] + 1
	band = BandWithID(id=id, **band_data.model_dump()).model_dump()
	BANDS.append(band)
	return band
	

