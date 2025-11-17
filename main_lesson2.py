from fastapi import FastAPI, HTTPException
from enum import Enum

app = FastAPI()

class GeneralURLChoices(Enum):
	ROCK = "rock"
	PROGRESSIVE_ROCK = "progressive_rock"
	HIP_HOP = "hip_hop"

BANDS= [
	{'id':1 , 'name':'The Beatles', 'genre':'Rock'},
	{'id':2 , 'name':'Led Zeppelin', 'genre':'Rock'},
	{'id':3 , 'name':'Pink Floyd', 'genre':'Progressive Rock'},
	{'id':4 , 'name':'Wu-Tang Clan', 'genre':'Hip Hop'},
]
@app.get("/bands")
async def bands() -> list[dict]:
	return BANDS

@app.get("/bands/{band_id}", status_code=200)
async def band(band_id: int) -> dict:
	band = next((band for band in BANDS if band['id'] == band_id), None)
	if band is None:
		raise HTTPException(status_code=404, detail="Band not found")
	return band
	
# 查询时如果有错误，提示genre清单有什么
@app.get('/bands/genre/{genre_name}')
async def bands_for_genre(genre_name: str) -> list[dict]:
	result = [
		band for band in BANDS if band['genre'].lower() == genre_name.lower()
	]
	if not result:
		available_genres = [genre.value for genre in GeneralURLChoices]
		raise HTTPException(
			status_code=404, 
			detail=f"No bands found for genre '{genre_name}'. Available genres: {', '.join(available_genres)}"
		)
	return result

# # 查询时如果有错误，不提示是否在genre清单里，只返回报错，避免使用这个api的人发现genre里有什么
# @app.get('/bands/genre/{genre_name}')
# async def bands_for_genre(genre_name: str) -> list[dict]:
# 	# 验证 genre_name 是否有效，但不暴露有效值列表
# 	valid_genres = [genre.value for genre in GeneralURLChoices]
# 	if genre_name not in valid_genres:
# 		raise HTTPException(status_code=404, detail="Genre not found")
	
# 	result = [
# 		band for band in BANDS if band['genre'].lower() == genre_name.lower()
# 	]
# 	if not result:
# 		raise HTTPException(status_code=404, detail="No bands found")
# 	return result