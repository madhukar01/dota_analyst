import asyncio
import glob
import json
import logging
from typing import Set
from typing import Tuple

from queries import player_match_ids_query
from stratz_client import fetch_graphql_data


def find_unique_data() -> Tuple[Set, Set]:
    """
    Go through all existing games and find unique data
    """
    logging.info("Finding unique data from existing games")
    json_files = glob.glob("json_data/*.json")
    unique_players = set()
    unique_matches = set()

    for json_file in json_files:
        with open(json_file, encoding="utf-8") as f:
            live_data = json.load(f)

        players = live_data["data"]["match"]["players"]
        for player in players:
            player_id = player["steamAccount"]["id"]
            unique_players.add(player_id)

        match_id = live_data["data"]["match"]["id"]
        unique_matches.add(match_id)
        logging.info(f"Parsed match {match_id}")

    logging.info(f"Found {len(unique_players)} unique players")
    logging.info(f"Found {len(unique_matches)} unique matches")
    return unique_players, unique_matches


async def fetch_new_data(steam_id: int, wait_time: int = 1) -> Tuple[Set, Set]:
    """
    Fetch new data from the last 100 games of a player
    """
    logging.info(f"Fetching data for player {steam_id}")

    unique_players = set()
    unique_matches = set()
    query = player_match_ids_query.build_query(steam_id)
    data, status = await fetch_graphql_data(query=query)
    await asyncio.sleep(wait_time)

    if status != 200:
        logging.error(f"Error fetching data for player {steam_id}: {status}")
        return unique_players, unique_matches

    matches = data["data"]["player"]["matches"]
    for match in matches:
        match_id = match["id"]
        unique_matches.add(match_id)

        players = match["players"]
        for player in players:
            player_id = player["steamAccountId"]
            unique_players.add(player_id)

    logging.info(f"Found {len(unique_players)} unique players")
    logging.info(f"Found {len(unique_matches)} unique matches")
    return unique_players, unique_matches


def main():
    """
    Find unique players and fetch their recent matches
    """
    # load list of players who have already been fetched
    with open("fetch_players.json", encoding="utf-8") as f:
        data = json.load(f)
        fetched_players = set(data.get("fetched_players", []))
        new_players = set(data.get("new_players", []))

    current_players, _ = find_unique_data()
    logging.info(f"Found {len(current_players)} current players")

    # fetch new players from last 100 games of each player
    players_to_fetch = current_players - fetched_players
    total = len(players_to_fetch)
    new_players = new_players - fetched_players
    new_players = new_players - current_players

    for idx, player_id in enumerate(players_to_fetch):
        logging.info(f"Fetching data for player {idx + 1}/{total}")
        players, _ = asyncio.run(fetch_new_data(player_id))
        fetched_players.add(player_id)

        new_players.update(players)
        new_players = new_players - current_players

        # store IDs in a json file
        new_data = {
            "new_players": list(new_players),
            "fetched_players": list(fetched_players),
        }
        with open("fetch_players.json", "w", encoding="utf-8") as f:
            json.dump(new_data, f, ensure_ascii=False, indent=4)

    logging.info(f"Found {len(new_players)} new players")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
