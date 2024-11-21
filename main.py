from mangum import Mangum
from typing import Annotated, Union
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from models import User

load_dotenv()

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

rds_postgres_url = os.getenv("AWS_POSTGRES_RDS_URL")

engine = create_engine(rds_postgres_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]


@app.get("/")
async def root():
    return {"message": "Hello From the Backend"}

@app.get("/test")
def get_test():
    return {"message": "From test route..."}

@app.get("/api/users")
def get_users(session: SessionDep):
    all_users = session.exec(select(User)).all()
    return all_users

handler = Mangum(app)