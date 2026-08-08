import logging

from fastapi import FastAPI, HTTPException


# ---------------------------------------------------------
# Logging Configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    )
)

logger = logging.getLogger("incident-test-app")


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

    logger.info("Home endpoint called")

    return {
        "message": "Incident Testing Environment is running"
    }


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------

@app.get("/health")
def health():

    logger.info("Health check successful")

    return {
        "status": "healthy"
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