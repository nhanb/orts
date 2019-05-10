import csv
import logging
import os
import traceback
from tkinter import E, N, S, StringVar, W, ttk
from tkinter.scrolledtext import ScrolledText

from utils.countries import country_name_to_code
from utils.logger import WidgetLogger
from utils.smashgg import get_players

PLAYERS_FILE_PATH = "./data/players.csv"


class SmashggTab:
    def __init__(self):
        self.callbacks = []
        self.tournament_id_var = StringVar()
        self.tournament_id_var.set("saigon-cup-2019")
        self.players_dict = _load_players_from_file()
        self.frame = None

    def init_frame(self, parent):
        self.frame = ttk.Frame(parent, padding=5)

        tournament_id_lbl = ttk.Label(self.frame, text="Tournament ID")
        tournament_id = ttk.Entry(self.frame, textvariable=self.tournament_id_var)
        tournament_id.bind("<Return>", lambda _: self._import_players())
        tournament_id_lbl.grid(column=0, row=0, padx=(0, 4))
        tournament_id.grid(column=1, row=0, sticky=(E, W))
        self.frame.grid_columnconfigure(1, weight=1)

        import_btn = ttk.Button(
            self.frame, text="⬇ Import players", command=self._import_players
        )
        import_btn.grid(column=1, row=1, sticky=(E), pady=(5, 0))

        scrolled_text = ScrolledText(self.frame, width=50, height=4)
        scrolled_text.grid(
            column=0, columnspan=2, row=2, sticky=(N, W, E, S), pady=(5, 0)
        )

        # Output logs into GUI ScrolledText
        log_handler = WidgetLogger(scrolled_text)
        logger = logging.getLogger()
        logger.addHandler(log_handler)
        logger.setLevel(logging.INFO)

        return self.frame

    def _import_players(self):
        tournament_id = self.tournament_id_var.get()

        if not tournament_id:
            logging.error("Please enter a tournament ID!")
            return

        try:
            players_data = get_players(tournament_id)
        except Exception:
            logging.error(traceback.format_exc())
            return

        players_dict = {
            player: (country_name_to_code(country_name), team)
            for player, (country_name, team) in players_data.items()
        }
        self.players_dict = players_dict

        for cb in self.callbacks:
            cb(players_dict)

        _save_players_to_file(players_dict)


def _load_players_from_file():
    if not os.path.isfile(PLAYERS_FILE_PATH):
        return {}

    with open(PLAYERS_FILE_PATH, "r", newline="") as pfile:
        reader = csv.DictReader(pfile, fieldnames=["name", "country", "team"])
        players = {row["name"]: (row["country"], row["team"]) for row in reader}

    logging.info(f"Loaded {len(players)} players from file {PLAYERS_FILE_PATH}")
    return players


def _save_players_to_file(players):
    with open(PLAYERS_FILE_PATH, "w", newline="") as pfile:
        writer = csv.DictWriter(pfile, fieldnames=["name", "country", "team"])
        writer.writeheader()
        for name, (country, team) in players.items():
            writer.writerow({"name": name, "country": country, "team": team})
    logging.info(f"Saved {len(players)} players to file {PLAYERS_FILE_PATH}")
