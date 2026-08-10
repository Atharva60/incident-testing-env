import logging
import os

import requests
from requests.auth import HTTPBasicAuth


logger = logging.getLogger("incident-testing-env")


ATLASSIAN_EMAIL = os.getenv("ATLASSIAN_EMAIL")
ATLASSIAN_API_TOKEN = os.getenv("ATLASSIAN_API_TOKEN")
ATLASSIAN_BASE_URL = os.getenv("ATLASSIAN_BASE_URL")

JIRA_PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY")
CONFLUENCE_SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")


def get_auth():

    return HTTPBasicAuth(
        ATLASSIAN_EMAIL,
        ATLASSIAN_API_TOKEN
    )


def check_jira_connection():

    try:

        url = (
            f"{ATLASSIAN_BASE_URL}"
            f"/rest/api/3/project/{JIRA_PROJECT_KEY}"
        )

        logger.info(
            "Jira connection test started | project=%s",
            JIRA_PROJECT_KEY
        )

        response = requests.get(
            url,
            auth=get_auth(),
            headers={
                "Accept": "application/json"
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            logger.info(
                "Jira connection successful | project=%s",
                data.get("key")
            )

            return {
                "connected": True,
                "project_key": data.get("key"),
                "project_name": data.get("name")
            }

        logger.error(
            "Jira connection failed | status_code=%s | response=%s",
            response.status_code,
            response.text
        )

        return {
            "connected": False,
            "status_code": response.status_code
        }

    except requests.RequestException:

        logger.exception(
            "Jira connection failed | reason=request_exception"
        )

        return {
            "connected": False
        }


def check_confluence_connection():

    try:

        url = (
            f"{ATLASSIAN_BASE_URL}"
            f"/wiki/api/v2/spaces"
        )

        logger.info(
            "Confluence connection test started | space_key=%s",
            CONFLUENCE_SPACE_KEY
        )

        response = requests.get(
            url,
            auth=get_auth(),
            headers={
                "Accept": "application/json"
            },
            params={
                "keys": CONFLUENCE_SPACE_KEY
            },
            timeout=10
        )

        if response.status_code == 200:

            data = response.json()

            results = data.get("results", [])

            if results:

                space = results[0]

                logger.info(
                    "Confluence connection successful | space_key=%s",
                    space.get("key")
                )

                return {
                    "connected": True,
                    "space_key": space.get("key"),
                    "space_name": space.get("name")
                }

            logger.warning(
                "Confluence connected but space not found | space_key=%s",
                CONFLUENCE_SPACE_KEY
            )

            return {
                "connected": False,
                "reason": "space_not_found"
            }

        logger.error(
            "Confluence connection failed | status_code=%s | response=%s",
            response.status_code,
            response.text
        )

        return {
            "connected": False,
            "status_code": response.status_code
        }

    except requests.RequestException:

        logger.exception(
            "Confluence connection failed | reason=request_exception"
        )

        return {
            "connected": False
        }