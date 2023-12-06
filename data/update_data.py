import asyncio
import glob
import json
import logging

import match_stats_query
from stratz_client import fetch_graphql_data


async def update_data():
    """
    Update missing stats data in existing json
    """
    # open all json files in "json_data" folder
    json_files = glob.glob("json_data/*.json")

    for json_file in json_files:
        # load the data from the file
        with open(json_file, encoding="utf-8") as f:
            live_data = json.load(f)

        # check if match stats already exist
        match_id = live_data["data"]["live"]["match"]["matchId"]
        current_match_data = live_data["data"]["match"]
        if "gameMode" in current_match_data:
            continue

        # fetch end match statistics
        query = match_stats_query.build_query(match_id)
        match_data, status = await fetch_graphql_data(query=query)
        await asyncio.sleep(1)

        if status != 200:
            logging.error(
                f"Error fetching stats for match {match_id}: {status}",
            )
            continue

        stats_data = match_data["data"]["match"]
        current_match_data.update(stats_data)
        live_data["data"]["match"] = current_match_data

        # write the data to a file
        with open(f"json_data/{match_id}.json", "w", encoding="utf-8") as f:
            json.dump(live_data, f, ensure_ascii=False, indent=4)

        logging.info(f"Updated file: {json_file}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(update_data())
