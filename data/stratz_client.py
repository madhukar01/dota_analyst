import logging
from typing import Dict

import httpx

logging.getLogger("httpx").setLevel(logging.ERROR)

# URL and auth token for the Stratz GraphQL endpoint
AUTH_TOKEN = ""
STRATZ_URL = "https://api.stratz.com/graphql"


async def fetch_graphql_data(query: Dict) -> tuple[Dict, int]:
    """
    Run the query against the GraphQL endpoint and return the response data
    and status code.
    :param query: the GraphQL query
    :param url: the GraphQL endpoint
    """
    async with httpx.AsyncClient() as client:
        client.headers.update({"Authorization": f"Bearer {AUTH_TOKEN}"})
        response = await client.post(STRATZ_URL, json=query, timeout=None)

        if response.status_code == 200:
            data = response.json()
        else:
            data = {}

        return data, response.status_code
