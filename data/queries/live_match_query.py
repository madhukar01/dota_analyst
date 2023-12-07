from typing import Dict

query_string = """
    query GetLiveMatches($numMatches: Int!) {
    live {
        matches(request: {
            take: $numMatches,
            orderBy: AVERAGE_RANK,
            isCompleted: true,
            gameStates: [POST_GAME]
        }) {
        matchId
        __typename
        }
        __typename
    }
    }
"""


def build_query(num_matches: int) -> Dict:
    """
    Build the GraphQL query to request the live matches.
    :param num_matches: the number of matches to request
    """
    query = {
        "operationName": "GetLiveMatches",
        "variables": {"numMatches": num_matches},
        "query": query_string,
    }

    return query
