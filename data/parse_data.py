import glob
import json
import logging
from typing import Dict

import numpy as np
import pandas as pd


def parse_match_data(data: Dict) -> Dict:
    """
    Parse JSON data and extract relevant information
    :param data: JSON data
    """
    stored_data = {}
    live_data = data["data"]["live"]["match"]
    match_stats = data["data"]["match"]

    # game info
    stored_data["match_id"] = live_data["matchId"]
    stored_data["game_mode"] = live_data["gameMode"]
    stored_data["game_duration"] = live_data["gameTime"]

    stored_data["radiant_score"] = live_data["radiantScore"]
    stored_data["dire_score"] = live_data["direScore"]
    stored_data["average_mmr"] = live_data["averageRank"]

    stored_data["radiant_win"] = match_stats["didRadiantWin"]
    stored_data["dire_win"] = not match_stats["didRadiantWin"]
    stored_data["winner"] = "radiant" if stored_data["radiant_win"] else "dire"

    # parse player and hero data
    for player in match_stats["players"]:
        if player["isRadiant"]:
            team_prefix = "radiant"
        else:
            team_prefix = "dire"

        player_pos = player["position"]
        player_prefix = f"{team_prefix}_{player_pos}".lower()

        # steam id
        stored_data[f"{player_prefix}_steam_id"] = player["steamAccount"]["id"]

        # game data (hero and stats)
        stored_data[f"{player_prefix}_hero"] = player["heroId"]

        # fetch player stats at minutes: 5, 10, 15, 20
        player_stats = player["stats"]
        stats_minutes = [5, 10, 15, 20]

        for minute in stats_minutes:
            # last hits
            last_hits = player_stats["lastHitsPerMinute"]
            if len(last_hits) >= minute:
                last_hit_sum = sum(last_hits[:minute])
            else:
                last_hit_sum = None
            stored_data[f"{player_prefix}_last_hits_{minute}"] = last_hit_sum

            # denies
            denies = player_stats["deniesPerMinute"]
            if len(denies) >= minute:
                denies_sum = sum(denies[:minute])
            else:
                denies_sum = None
            stored_data[f"{player_prefix}_denies_{minute}"] = denies_sum

            # average gpm
            gpm = player_stats["goldPerMinute"]
            if len(gpm) >= minute:
                avg_gpm = np.round(np.mean(gpm[:minute]), 2)
            else:
                avg_gpm = None
            stored_data[f"{player_prefix}_gpm_{minute}"] = avg_gpm

            # average xpm
            xpm = player_stats["experiencePerMinute"]
            if len(xpm) >= minute:
                avg_xpm = np.round(np.mean(xpm[:minute]), 2)
            else:
                avg_xpm = None
            stored_data[f"{player_prefix}_xpm_{minute}"] = avg_xpm

            # networth
            networth = player_stats["networthPerMinute"]
            if len(networth) >= minute:
                networth_sum = networth[minute - 1]
            else:
                networth_sum = None
            stored_data[f"{player_prefix}_networth_{minute}"] = networth_sum

            # actions
            actions = player_stats["actionsPerMinute"]
            if len(actions) >= minute:
                actions_sum = sum(actions[:minute])
            else:
                actions_sum = None
            stored_data[f"{player_prefix}_actions_{minute}"] = actions_sum

            # camps stacked
            camps_stacked = player_stats["campStack"]
            if len(camps_stacked) >= minute:
                camps_stacked_sum = sum(camps_stacked[:minute])
            else:
                camps_stacked_sum = None
            key = f"{player_prefix}_camps_stacked_{minute}"
            stored_data[key] = camps_stacked_sum

            # hero damage
            hero_damage = player_stats["heroDamagePerMinute"]
            if len(hero_damage) >= minute:
                hero_damage_sum = sum(hero_damage[:minute])
            else:
                hero_damage_sum = None
            stored_data[
                f"{player_prefix}_hero_damage_{minute}"
            ] = hero_damage_sum

            # healing
            healing = player_stats["healPerMinute"]
            if len(healing) >= minute:
                healing_sum = sum(healing[:minute])
            else:
                healing_sum = None
            stored_data[f"{player_prefix}_heal_{minute}"] = healing_sum

            # hero damage taken
            hero_damage_taken = player_stats["heroDamageReceivedPerMinute"]
            if len(hero_damage_taken) >= minute:
                hero_damage_taken_sum = hero_damage_taken[minute - 1]
            else:
                hero_damage_taken_sum = None
            key = f"{player_prefix}_hero_damage_taken_{minute}"
            stored_data[key] = hero_damage_taken_sum

            # tower damage
            tower_damage = player_stats["towerDamagePerMinute"]
            if len(tower_damage) >= minute:
                tower_damage_sum = sum(tower_damage[:minute])
            else:
                tower_damage_sum = None
            key = f"{player_prefix}_tower_damage_{minute}"
            stored_data[key] = tower_damage_sum

            # kills
            kill_events = player_stats["killEvents"]
            kills = 0
            for event in kill_events:
                if event["time"] <= minute * 60:
                    kills += 1
                else:
                    break
            stored_data[f"{player_prefix}_kills_{minute}"] = kills

            # deaths
            death_events = player_stats["deathEvents"]
            deaths = 0
            for event in death_events:
                if event["time"] <= minute * 60:
                    deaths += 1
                else:
                    break
            stored_data[f"{player_prefix}_deaths_{minute}"] = deaths

            # assists
            assist_events = player_stats["assistEvents"]
            assists = 0
            for event in assist_events:
                if event["time"] <= minute * 60:
                    assists += 1
                else:
                    break

            # level
            level_events = player_stats["level"]
            level = -1
            for event in level_events:
                if event < minute * 60:
                    level += 1
                else:
                    break
            stored_data[f"{player_prefix}_level_{minute}"] = level

            # wards and sentries
            ward_events = player_stats["wards"]
            wards_count = 0
            sentries_count = 0
            for event in ward_events:
                if event["time"] <= minute * 60:
                    if event["type"] == 0:
                        wards_count += 1
                    elif event["type"] == 1:
                        sentries_count += 1
                else:
                    break
            stored_data[f"{player_prefix}_wards_{minute}"] = wards_count
            stored_data[f"{player_prefix}_sentries_{minute}"] = sentries_count

    # fetch match stats at minutes: 5, 10, 15, 20
    for minute in stats_minutes:
        # kills
        radiant_kills = match_stats["radiantKills"]
        dire_kills = match_stats["direKills"]
        if len(radiant_kills) >= minute:
            radiant_kills_sum = sum(radiant_kills[:minute])
            dire_kills_sum = sum(dire_kills[:minute])
        else:
            radiant_kills_sum = None
            dire_kills_sum = None
        stored_data[f"radiant_kills_{minute}"] = radiant_kills_sum
        stored_data[f"dire_kills_{minute}"] = dire_kills_sum

        # win rates
        win_rates = match_stats["winRates"]
        if len(win_rates) >= minute:
            radiant_win_rate = win_rates[minute - 1]
            dire_win_rate = np.round(1 - radiant_win_rate, 2)
        else:
            radiant_win_rate = None
            dire_win_rate = None
        stored_data[f"radiant_win_rate_{minute}"] = radiant_win_rate
        stored_data[f"dire_win_rate_{minute}"] = dire_win_rate

        # networth lead
        networth_leads = match_stats["radiantNetworthLeads"]
        if len(networth_leads) >= minute:
            radiant_networth_lead = networth_leads[minute - 1]
            dire_networth_lead = -1 * radiant_networth_lead
        else:
            radiant_networth_lead = None
            dire_networth_lead = None

        key = f"radiant_networth_lead_{minute}"
        stored_data[key] = radiant_networth_lead
        key = f"dire_networth_lead_{minute}"
        stored_data[key] = dire_networth_lead

        # towers lost
        tower_death_events = match_stats["towerDeaths"]
        radiant_towers_lost = 0
        dire_towers_lost = 0
        for event in tower_death_events:
            if event["time"] <= minute * 60:
                if event["isRadiant"]:
                    radiant_towers_lost += 1
                else:
                    dire_towers_lost += 1
            else:
                break
        stored_data[f"radiant_towers_lost_{minute}"] = radiant_towers_lost
        stored_data[f"dire_towers_lost_{minute}"] = dire_towers_lost

    return stored_data


def generate_csv():
    """
    Find all the json files in the json_data folder and parse them to csv
    """
    # open all json files in "json_data" folder
    json_files = glob.glob("json_data/*.json")

    # create a list of all the data
    parsed_data_list = []
    errors = 0
    for json_file in json_files:
        with open(json_file, encoding="utf-8") as f:
            raw_json = json.load(f)

        try:
            parsed_json = parse_match_data(raw_json)
        except Exception as exc:
            logging.error(exc)
            logging.error(f"Error parsing file: {json_file}")
            errors += 1
            continue

        parsed_data_list.append(parsed_json)

    logging.info("Parsing complete")
    logging.info(f"Total files parsed: {len(json_files)}")
    logging.info(f"Total errors: {errors}")

    # convert the data to a dataframe
    df = pd.DataFrame(parsed_data_list)

    # save the data to a csv file
    df.to_csv("parsed_data.csv", index=False)


if __name__ == "__main__":
    generate_csv()
