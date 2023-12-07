from typing import Dict

query_string = """
query GetUserMatches($steamId: Long!, $numMatches: Int!) {
    player(steamAccountId:$steamId)
    {
        matches(request: {
            isParsed: true,
            take: $numMatches,
            playerList: ALL,
            rankIds:[80]
    }) {
            id,
            players{
                steamAccountId
            }
        }
    }
}
"""


def build_query(steam_id: int, num_matches: int = 10) -> Dict:
    """
    Build the GraphQL query to request old matches of a player
    :param num_matches: the number of matches to request
    """
    query = {
        "operationName": "GetUserMatches",
        "variables": {"steamId": steam_id, "numMatches": num_matches},
        "query": query_string,
    }

    return query
