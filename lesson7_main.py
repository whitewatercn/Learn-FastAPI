
"""
本节学习sqlmodel
"""

from fastapi import FastAPI, HTTPException, Path, Query,Depends
from enum import Enum
from lesson7_models import Band,Album, BandCreate,GeneralURLChoices
from typing import Annotated
from contextlib import asynccontextmanager
from sqlmodel import Session, select
from lesson7_db import init_db,get_session
@asynccontextmanager
async def lifespan(app: FastAPI):
	init_db()
	yield	 

app = FastAPI(lifespan=lifespan)


@app.get("/bands",)
async def bands(
	genre:GeneralURLChoices | None = None,
	q: Annotated[str | None, Query(max_length=10)] = None,
	session:Session= Depends(get_session)
)  -> list[Band]:
	
	band_list = session.exec(select(Band)).all()


	if genre:
		band_list = [ band for band in band_list if band.genre.value.lower() == genre.value.lower() ]
	if q:
		band_list = [ band for band in band_list if q.lower() in band.name.lower() ]
	
	return band_list

@app.get("/bands/{band_id}")
async def band(
	band_id: Annotated[int, Path(title='The band ID')],
	session:Session= Depends(get_session)
) -> Band:
	band = session.get(Band, band_id)
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
async def create_band(
	band_data:BandCreate,
	session:Session= Depends(get_session)
	
	) -> Band:
	band = Band(name=band_data.name, genre=band_data.genre)

	session.add(band)

	if band_data.albums:
		for album_data in band_data.albums:
			album_obj = Album(
				title=album_data.title,
				release_date=album_data.release_date,
				band=band
			)
			session.add(album_obj)
	session.commit()
	session.refresh(band)

	return band
	

