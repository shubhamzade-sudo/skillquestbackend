# app/db/snowflakedb.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

SF_USER = os.getenv("SF_USER")
SF_PASSWORD = os.getenv("SF_PASSWORD")
SF_ACCOUNT = os.getenv("SF_ACCOUNT")      # e.g. "xy12345.ap-southeast-1"
SF_DATABASE = os.getenv("SF_DATABASE")    # e.g. "SNOWFLAKE_LEARNING_DB"
SF_SCHEMA = os.getenv("SF_SCHEMA", "PUBLIC")
SF_WAREHOUSE = os.getenv("SF_WAREHOUSE")  # e.g. "COMPUTE_WH"
SF_ROLE = os.getenv("SF_ROLE")            # optional

DATABASE_URL_Test = (
    f"snowflake://{SF_USER}:{SF_PASSWORD}@{SF_ACCOUNT}/{SF_DATABASE}/{SF_SCHEMA}"
    f"?warehouse={SF_WAREHOUSE}&role={SF_ROLE}"
)

# create engine (sqlalchemy + snowflake-sqlalchemy must be installed)
engine = create_engine(DATABASE_URL_Test, echo=False, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()   # <--- fixed (removed stray dot)
