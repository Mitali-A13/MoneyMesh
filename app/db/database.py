from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# name of the database notebook
DATABASE_URL = "sqlite:///./finance.db"

# connection b/w app & database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# created session, to interact with database temporarily
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# created base (template to create tables)
Base = declarative_base()
