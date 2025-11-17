from fastapi import FastAPI, HTTPException
from enum import Enum
from schemas_lesson3 import Band

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
	{'id':4 , 'name':'Wu-Tang Clan', 'genre':'Hip Hop','albums':[
		{'title':'Enter the Wu-Tang (36 Chambers)', 'release_date':'1993-11-09'},
		{'title':'Wu-Tang Forever', 'release_date':'1997-06-03'}
	]},
]

@app.get("/bands")
async def bands() -> list[Band]:
	return [
		Band(**band) for band in BANDS
	]

@app.get("/bands/{band_id}", status_code=200)
async def band(band_id: int) -> Band:
	band = next((Band(**band) for band in BANDS if band['id'] == band_id), None)
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