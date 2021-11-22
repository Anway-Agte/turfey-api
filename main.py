from fastapi import FastAPI
from routes.auth_routes import auth_router
from routes.turf_routes import turf_router
from routes.booking_routes import booking_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth")
app.include_router(turf_router, prefix="/turf")
app.include_router(booking_router, prefix="/book")
