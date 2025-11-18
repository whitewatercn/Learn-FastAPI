"""
本节进一步学习query parameter以及如何通过post写入数据
还有pydantic的field_validator装饰器（见lesson5_schemas.py）
"""

from fastapi import FastAPI, HTTPException
from enum import Enum
from lesson5_schemas import BandBase, BandCreate, BandWithID, GeneralURLChoices

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
	{'id':4 , 'name':'Wu-Tang Clan', 'genre':'Hip Hop','albums':[]}

]


"""
和lesson4_main.py类似，不过这里返回的是BandWithID
@app.get("/bands/{band_id}", status_code=200)
@app.get('/bands/genre/{genre_name}')
这两个同理

"""
@app.get("/bands")
async def bands(
	genre:GeneralURLChoices | None = None,
	has_albums:bool | None = None
)  -> list[BandWithID]:

	band_list = [BandWithID(**band) for band in BANDS]

	if genre:
		return [ band for band in band_list if band.genre.lower() == genre.value ]

	if has_albums is not None:
		if has_albums:
			band_list = [ band for band in band_list if len(band.albums) > 0 ]
		else:
			band_list = [ band for band in band_list if len(band.albums) == 0 ]
	
	return band_list

@app.get("/bands/{band_id}", status_code=200)
async def band(band_id: int) -> BandWithID:
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




"""
增加了一个POST方法用于创建新的band
使用BandCreate输入，返回BandWithID
"""
@app.post('/bands')
async def create_band(band_data:BandCreate) -> BandWithID:
	id = BANDS[-1]['id'] + 1
	band = BandWithID(id=id, **band_data.model_dump()).model_dump()
	BANDS.append(band)
	return band
	

