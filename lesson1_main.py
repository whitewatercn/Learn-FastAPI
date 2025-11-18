"""
第一课，学习FastAPI的基础用法
创建一个最简单的FastAPI应用
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def index() -> dict[str, str]:
	return {"hello": " World!"}

@app.get("/about")
async def about() -> str:
	return "一个记录fastapi学习笔记的网站"