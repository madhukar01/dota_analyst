import asyncio
import glob
import json
import logging
import random

from pull_data import save_match_data
from queries import player_matches_query
from stratz_client import fetch_graphql_data


async def fetch_player_games(player_id: int, saved_games: set) -> int:
    """
    Fetch all games for a player.
    :param player_id: id of player to fetch games for
    :param wait_time: seconds to wait between requests
    """
    # fetch the data for each match
    logging.info(f"Fetching data for player {player_id}")

    query = player_matches_query.build_query(player_id, num_matches=5)
    all_matches, status = await fetch_graphql_data(query=query)

    if status != 200:
        logging.error(
            f"Error fetching data for player {player_id}: {status}",
        )
        return 0

    matches = all_matches["data"]["player"]["matches"]
    match_data = {}

    for match in matches:
        match_id = match["id"]
        if match_id in saved_games:
            continue
        match_data[match_id] = match

    # pick a random match id
    data_saved = 0
    while data_saved < 1 and len(match_data) > 0:
        match_id = random.choice(list(match_data.keys()))
        data_to_save = match_data[match_id]

        data = {"data": {"match": data_to_save}}

        data_saved = save_match_data(data, match_id)
        match_data.pop(match_id)

        if data_saved < 0:
            return 0

    return data_saved


async def fetch_old_games():
    # read player_ids from file
    with open("new_data.json", encoding="utf-8") as f:
        data = json.load(f)

    new_players = set(data["new_players"])
    fetched_players = set(data["fetched_players"])

    # ids of saved games
    saved_games = set()
    json_files = glob.glob("json_data/*.json")
    for file in json_files:
        saved_games.add(int(file.split("\\")[1].split(".")[0]))

    # fetch games from each player
    counter = 0
    while len(new_players) > 0:
        player_id = new_players.pop()
        counter += await fetch_player_games(player_id, saved_games)
        # await asyncio.sleep(0.1)

        fetched_players.add(player_id)
        logging.info(f"Fetched {counter} new games")

        if counter % 10 == 0:
            # save the new data
            data["new_players"] = list(new_players)
            data["fetched_players"] = list(fetched_players)
            with open("new_data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

    # save the new data
    data["new_players"] = list(new_players)
    data["fetched_players"] = list(fetched_players)
    with open("new_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(fetch_old_games())
