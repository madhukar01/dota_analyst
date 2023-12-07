import asyncio
import json
import logging
import time
from pathlib import Path

from queries import live_match_query
from queries import match_stats_query
from stratz_client import fetch_graphql_data

# create a new logger with ID and level
logging.basicConfig(
    filename="pull_data.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# setup logging to console
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
console.setFormatter(formatter)
logging.getLogger("").addHandler(console)


async def run_scraping(num_matches: int = 50, wait_time: int = 1) -> int:
    """
    Run scraping, fetching live matches and their data.
    :param num_matches: number of matches to fetch
    :param wait_time: seconds to wait between requests
    """
    # fetch last num_matches matches that have completed
    logging.info(f"Fetching {num_matches} matches")
    count = 0

    query = live_match_query.build_query(num_matches)
    data, status = await fetch_graphql_data(query=query)
    await asyncio.sleep(wait_time)

    if status != 200:
        logging.error(f"Error fetching live matches: {status}")
        return count

    matches = data["data"]["live"]["matches"]
    matches_to_fetch = []

    # check if this match is already in the data folder
    for match in matches:
        match_id = match["matchId"]

        path = f"json_data/{match_id}.json"
        if Path(path).exists():
            continue

        matches_to_fetch.append(match_id)

    # fetch the data for each match
    for match_id in matches_to_fetch:
        logging.info(f"Fetching data for match {match_id}")

        query = match_stats_query.build_query(match_id)
        match_data, status = await fetch_graphql_data(query=query)
        await asyncio.sleep(wait_time)

        if status != 200:
            logging.error(
                f"Error fetching data for match {match_id}: {status}",
            )
            continue

        # check if the match is ranked and rank is immortal
        game_mode = match_data["data"]["match"]["gameMode"]
        average_rank = match_data["data"]["match"]["rank"]

        if game_mode != "ALL_PICK_RANKED" or average_rank < 80:
            logging.error(f"Skipping match {match_id}: {average_rank}")
            input("Press enter to continue...")
            continue

        # check if match has lastHits data
        players = match_data["data"]["match"]["players"]
        no_last_hits = False
        for player in players:
            if player["stats"]["lastHitsPerMinute"] is None:
                no_last_hits = True
                break

        if no_last_hits:
            continue

        # write the data to a file
        with open(f"json_data/{match_id}.json", "w", encoding="utf-8") as f:
            json.dump(match_data, f, ensure_ascii=False, indent=4)
            count += 1

    return count


if __name__ == "__main__":
    wait_between_scrape = 900
    counter = 0
    matches_per_scrape = 100

    while True:
        current_scraped = asyncio.run(run_scraping(matches_per_scrape))
        counter += current_scraped
        logging.info(f"Scraped {current_scraped} matches, {counter} total")
        logging.info(f"Waiting {wait_between_scrape} seconds")
        time.sleep(wait_between_scrape)
