from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.mysql_models import Base
import os
from dotenv import load_dotenv

load_dotenv()
#DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3307/my_db"
#DATABASE_URL = "mysql+pymysql://user1:mysql123456@localhost:3306/my_db"
DATABASE_URL = os.getenv("DATABASE_URL")
# MYSQL_host_3307 = os.getenv("MYSQL_URL_3307")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
    
# สำหรับใช้กับ FastAPI (Depends)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()