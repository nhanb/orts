import logging

import requests

BASE_TOURNAMENT_URL = "https://api.smash.gg/tournament"
BASE_GROUP_URL = "https://api.smash.gg/phase_group"

session = requests.Session()


def get_players(tournament_id):
    logging.info(f"Fetching tournament '{tournament_id}'...")
    tournament_url = f"{BASE_TOURNAMENT_URL}/{tournament_id}?expand[]=groups"
    tournament_resp = session.get(tournament_url)
    groups = tournament_resp.json()["entities"]["groups"]

    logging.info(f"Found {len(groups)} groups.")

    merged_players_data = {}

    for group in groups:
        logging.info("Processing group {}...".format(group["id"]))
        group_url = f"{BASE_GROUP_URL}/{group['id']}"
        group_resp = session.get(group_url, params={"expand[]": "entrants"})

        entities = group_resp.json()["entities"]
        entrants = entities.get("entrants")
        players = entities.get("player")

        if not entrants or not players:
            continue

        # Read names from "entrants" array.
        # Because a player can use a different name for each tournament,
        # we can't just read the name directly from "player" array.
        for entrant in entrants:
            player_ids = tuple(val for val in entrant["playerIds"].values())

            if len(player_ids) > 1:
                dict_key = player_ids  # team entrant
            else:
                dict_key = player_ids[0]  # single player entrant

            merged_players_data[dict_key] = {
                **(merged_players_data.get(dict_key) or {}),
                "name": entrant["name"],
            }

        # Read countries from "players" array.
        for player in players:
            player_id = player["id"]
            player_data = merged_players_data.get(player_id) or {}
            player_data["country"] = player["country"]
            merged_players_data[player_id] = {
                # fill in player's main gamerTag as a fallback in case they didn't have
                # a tournament-specific name
                "name": player["gamerTag"],
                **(merged_players_data.get(player_id) or {}),
                "country": player["country"],
            }

    # Remove player ID, transform into just a {name: country} dict
    player_dicts = merged_players_data.values()
    result = {dict_["name"]: dict_.get("country") for dict_ in player_dicts}

    logging.info(f"Found {len(result)} players.")

    return result
