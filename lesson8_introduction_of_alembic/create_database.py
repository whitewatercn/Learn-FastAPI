from requests import Session
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
"""
这个代码用于创建一个简单的数据库
"""


# 先写好数据库地址
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# 创建一个engine，管理与数据库的连接、SQL执行等
# 然后创建一个会话session，追踪内存中对象变化，执行增删改查，最终把改动写入数据库，用完要关闭session
# 接下来创建一个Base类，用于规范元数据，这个表里有什么列，每个列叫什么名字，类型是什么，等
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, index=True)
	email = Column(String, unique=True, index=True)
	password=Column(String, nullable=True)
	birthday=Column(String, nullable=True)

	def __repr__(self): 
		return f"<User(name={self.name}, email={self.email})>"
	
if __name__ == "__main__":
	# 如果执行，就创建所有表
	Base.metadata.create_all(bind=engine) 