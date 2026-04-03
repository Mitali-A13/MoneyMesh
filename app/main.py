from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.models.financial_record import FinancialRecord
from app.routes import user_routes, financial_routes, dashboard_routes, auth_routes

app = FastAPI(title="Finance Backend API")

# registering routes
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(financial_routes.router)
app.include_router(dashboard_routes.router)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "API is running"}
