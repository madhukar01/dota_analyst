import asyncio
import glob
import json
import logging
import os


async def update_data():
    """
    Update missing stats data in existing json
    """
    # open all json files in "json_data" folder
    json_files = glob.glob("json_data/*.json")

    for json_file in json_files:
        # load the data from the file
        with open(json_file, encoding="utf-8") as f:
            match_data = json.load(f)

        # remove the match if last hits per minute is null
        match_id = match_data["data"]["match"]["id"]
        players = match_data["data"]["match"]["players"]
        deleted = False

        for player in players:
            if player["stats"]["lastHitsPerMinute"] is None:
                logging.info(f"Removing match {match_id}")
                os.remove(json_file)
                deleted = True
                break

        if deleted:
            continue


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(update_data())
