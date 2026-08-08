import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pymongo.errors import PyMongoError

load_dotenv()

from app.database import (
    check_mongodb_health,
    connect_to_mongodb,
    get_users_collection
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

@app.post("/users")
def create_user(name: str, email: str):

    logger.info(
        "Create user request received | name=%s | email=%s",
        name,
        email
    )

    users_collection = get_users_collection()

    if users_collection is None:
        logger.error(
            "Create user failed | reason=database_unavailable"
        )

        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

    try:
        existing_user = users_collection.find_one(
            {"email": email}
        )

        if existing_user:
            logger.warning(
                "Create user rejected | email=%s | reason=user_already_exists",
                email
            )

            raise HTTPException(
                status_code=409,
                detail="User already exists"
            )

        user = {
            "name": name,
            "email": email
        }

        result = users_collection.insert_one(user)

        logger.info(
            "User created successfully | user_id=%s | email=%s",
            result.inserted_id,
            email
        )

        return {
            "id": str(result.inserted_id),
            "name": name,
            "email": email
        }

    except HTTPException:
        raise

    except PyMongoError:
        logger.exception(
            "Create user failed | email=%s | reason=mongodb_error",
            email
        )

        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

@app.get("/users/{email}")
def get_user(email: str):

    logger.info(
        "User lookup started | email=%s",
        email
    )

    users_collection = get_users_collection()

    if users_collection is None:
        logger.error(
            "User lookup failed | reason=database_unavailable"
        )

        raise HTTPException(
            status_code=503,
            detail="Database unavailable"
        )

    try:
        user = users_collection.find_one(
            {"email": email}
        )

        if not user:
            logger.warning(
                "User lookup failed | email=%s | reason=user_not_found",
                email
            )

            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        logger.info(
            "User lookup successful | email=%s",
            email
        )

        return {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"]
        }

    except HTTPException:
        raise

    except PyMongoError:
        logger.exception(
            "User lookup failed | email=%s | reason=mongodb_error",
            email
        )

        raise HTTPException(
            status_code=500,
            detail="Database operation failed"
        )

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


