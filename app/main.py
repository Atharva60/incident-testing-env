import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

from app.database import (
    check_mongodb_health,
    connect_to_mongodb
)


# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

APP_NAME = os.getenv("APP_NAME", "incident-testing-env")
APP_ENV = os.getenv("APP_ENV", "development")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

logger = logging.getLogger(APP_NAME)

mongodb_connected = connect_to_mongodb()


# ---------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------

app = FastAPI(
    title="Incident Testing Environment",
    version="1.0.0"
)


# ---------------------------------------------------------
# Home
# ---------------------------------------------------------

@app.get("/")
def home():

    logger.info(
        "Home endpoint called | environment=%s",
        APP_ENV
    )

    return {
        "message": "Incident Testing Environment is running",
        "app_name": APP_NAME,
        "environment": APP_ENV
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    mongodb_healthy = check_mongodb_health()

    if mongodb_healthy:

        logger.info(
            "Health check successful | mongodb=connected"
        )

    else:

        logger.warning(
            "Health check degraded | mongodb=disconnected"
        )

    return {
        "status": (
            "healthy"
            if mongodb_healthy
            else "degraded"
        ),
        "environment": APP_ENV,
        "mongodb": (
            "connected"
            if mongodb_healthy
            else "disconnected"
        )
    }


# ---------------------------------------------------------
# Calculate
# ---------------------------------------------------------

@app.get("/calculate")
def calculate(a: int, b: int):

    logger.info(
        "Calculate request received | a=%s | b=%s",
        a,
        b
    )

    result = a + b

    logger.info(
        "Calculate request completed | result=%s",
        result
    )

    return {
        "a": a,
        "b": b,
        "result": result
    }


# ---------------------------------------------------------
# User Lookup
# ---------------------------------------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):

    logger.info(
        "User lookup started | user_id=%s",
        user_id
    )

    if user_id != 1:

        logger.warning(
            "User lookup failed | user_id=%s | reason=user_not_found",
            user_id
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    logger.info(
        "User lookup completed | user_id=%s",
        user_id
    )

    return {
        "id": 1,
        "name": "Test User"
    }


# ---------------------------------------------------------
# Intentional Error
# ---------------------------------------------------------

@app.get("/test-error")
def test_error():

    logger.info(
        "Intentional error endpoint triggered"
    )

    try:
        result = 10 / 0

        return {
            "result": result
        }

    except Exception:

        logger.exception(
            "Unhandled exception occurred | scenario=division_by_zero"
        )

        raise


