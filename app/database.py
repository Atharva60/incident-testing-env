import logging
import os

from pymongo import MongoClient
from pymongo.errors import PyMongoError


logger = logging.getLogger("incident-testing-env")


MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DB_NAME = os.getenv(
    "MONGODB_DB_NAME",
    "incident_test_db"
)


client = None
database = None


def connect_to_mongodb():
    global client
    global database

    if not MONGODB_URI:
        logger.error(
            "MongoDB configuration missing | variable=MONGODB_URI"
        )

        return False

    try:
        logger.info(
            "MongoDB connection attempt started"
        )

        client = MongoClient(
            MONGODB_URI,
            serverSelectionTimeoutMS=5000
        )

        # Force an actual connection test
        client.admin.command("ping")

        database = client[MONGODB_DB_NAME]

        logger.info(
            "MongoDB connection successful | database=%s",
            MONGODB_DB_NAME
        )

        return True

    except PyMongoError:

        logger.exception(
            "MongoDB connection failed"
        )

        return False


def check_mongodb_health():

    if client is None:
        return False

    try:
        client.admin.command("ping")
        return True

    except PyMongoError:

        logger.exception(
            "MongoDB health check failed"
        )

        return False

def get_users_collection():
    if database is None:
        return None

    return database["users"]