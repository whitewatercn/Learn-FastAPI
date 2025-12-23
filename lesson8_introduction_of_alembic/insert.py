from requests import Session
from create_database import SessionLocal
from create_database import User

with SessionLocal() as session:
	new_user = User(name="Bob", email="dem1@example.org",password="secur1password", 
				 birthday="19900101"
				 )
	session.add(new_user)
	session.commit()