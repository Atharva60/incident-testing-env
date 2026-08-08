import logging

from fastapi import FastAPI, HTTPException


# ---------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("incident-test-app")


# ---------------------------------------------------------
# FastAPI application
# ---------------------------------------------------------

app = FastAPI(
    title="Incident Testing Environment",
    version="1.0.0"
)


# ---------------------------------------------------------
# API 1 - Home
# ---------------------------------------------------------

@app.get("/")
def home():

    logger.info("Home endpoint called")

    return {
        "message": "Incident Testing Environment is running"
    }


# ---------------------------------------------------------
# API 2 - Health check
# ---------------------------------------------------------

@app.get("/health")
def health():

    logger.info("Health check successful")

    return {
        "status": "healthy"
    }


# ---------------------------------------------------------
# API 3 - Simple calculation
# ---------------------------------------------------------

@app.get("/calculate")
def calculate(a: int, b: int):

    logger.info(
        "Calculate endpoint called with a=%s and b=%s",
        a,
        b
    )

    result = a + b

    logger.info(
        "Calculation successful result=%s",
        result
    )

    return {
        "a": a,
        "b": b,
        "result": result
    }


# ---------------------------------------------------------
# API 4 - Controlled 404 error
# ---------------------------------------------------------

@app.get("/users/{user_id}")
def get_user(user_id: int):

    logger.info(
        "Searching for user_id=%s",
        user_id
    )

    if user_id != 1:

        logger.warning(
            "User not found user_id=%s",
            user_id
        )

        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "id": 1,
        "name": "Test User"
    }


# ---------------------------------------------------------
# API 5 - Intentional server error
# ---------------------------------------------------------

@app.get("/test-error")
def test_error():

    logger.info(
        "Intentional error endpoint called"
    )

    try:

        value = 10 / 0

        return {
            "result": value
        }

    except Exception:

        logger.exception(
            "Intentional division by zero error"
        )

        raise


