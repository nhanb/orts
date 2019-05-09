import json
import os
from functools import partial
from tkinter import HORIZONTAL, E, N, S, StringVar, Tk, W, ttk

from utils.ui import AutocompleteCombobox, SmashggTab

STATE_FILE_PATH = "./web/state.json"
COUNTRIES_FILE_PATH = "./data/countries.txt"


def build_ui(
    *,
    root,
    countries,
    smashgg_tab,
    p1_wins,
    p2_wins,
    apply_state,
    discard_unapplied_state,
    reset_scores,
    swap_players,
    trace_widget,
):
    root.title("Overly Repetitive Tedious Software")

    style = ttk.Style()
    # Default Windows theme (xpnative/vista) doesn't support `fieldbackground`
    # so we're settling with "clam" theme for now.
    style.theme_use("clam")
    style.configure("Active.TEntry", fieldbackground="#dffcde")
    style.configure("Active.TCombobox", fieldbackground="#dffcde")
    style.configure("Active.TSpinbox", fieldbackground="#dffcde")

    # 2 tabs in main Notebook
    notebook = ttk.Notebook(root)
    notebook.grid(column=0, row=0, sticky=(N, S, E, W))
    frame1 = ttk.Frame(notebook, padding=5)
    frame2 = smashgg_tab.init_frame(notebook)
    notebook.add(frame1, text="Main")
    notebook.add(frame2, text="Smash.gg")

    # Main tab has these frames:
    misc = ttk.Frame(frame1, padding=(0, 0, 0, 7))
    players = ttk.Frame(frame1, padding=(0, 0, 0, 0))
    actions = ttk.Frame(frame1, padding=(0, 7, 0, 0))
    misc.grid(column=0, row=0, sticky=(N, S, E, W))
    players.grid(column=0, row=1, sticky=(N, S, E, W))
    actions.grid(column=0, row=2, sticky=(N, S, E, W))

    # Misc: (fields not belonging to any player)
    descriptionlbl = ttk.Label(misc, text="Match description")
    description = ttk.Entry(misc)
    trace_widget(description, "description", "TEntry")
    descriptionlbl.grid(column=0, row=0, padx=(0, 4))
    description.grid(column=1, row=0, sticky=(E, W))
    misc.grid_columnconfigure(1, weight=1)

    # Players:

    ## Declare widgets, bind values:

    name1lbl = ttk.Label(players, text="Player 1")
    name1 = AutocompleteCombobox(players, width="30")
    trace_widget(name1, "p1name", "TCombobox")

    country1 = ttk.Combobox(players, width="6", values=countries)
    trace_widget(country1, "p1country", "TCombobox")

    score1 = ttk.Spinbox(players, from_=0, to=777, width="4")
    trace_widget(score1, "p1score", "TSpinbox")

    team1lbl = ttk.Label(players, text="Team 1")
    team1 = AutocompleteCombobox(players)
    trace_widget(team1, "p1team", "TCombobox")

    win1 = ttk.Button(players, text="▲ Win", width="6", command=p1_wins)

    name2lbl = ttk.Label(players, text="Player 2")
    name2 = AutocompleteCombobox(players, width="30")
    trace_widget(name2, "p2name", "TCombobox")

    country2 = ttk.Combobox(players, width="6", values=countries)
    trace_widget(country2, "p2country", "TCombobox")

    score2 = ttk.Spinbox(players, from_=0, to=777, width="4")
    trace_widget(score2, "p2score", "TSpinbox")

    team2lbl = ttk.Label(players, text="Team 2")
    team2 = AutocompleteCombobox(players)
    trace_widget(team2, "p2team", "TCombobox")

    win2 = ttk.Button(players, text="▲ Win", width="6", command=p2_wins)

    ## Layout via grid:

    name1lbl.grid(column=0, row=0, padx=(0, 2))
    name1.grid(column=1, row=0, padx=2)
    country1.grid(column=2, row=0, padx=2)
    score1.grid(column=3, row=0, padx=2)
    win1.grid(column=4, row=0, padx=(2, 0), rowspan=2, sticky=(N, S))
    team1lbl.grid(column=0, row=1, padx=(0, 2))
    team1.grid(column=1, row=1, padx=2, columnspan=3, sticky=(E, W))

    ttk.Separator(players, orient=HORIZONTAL).grid(
        column=0, row=2, columnspan=5, sticky="ew", pady=10
    )

    name2lbl.grid(column=0, row=3, padx=(0, 2))
    name2.grid(column=1, row=3, padx=2)
    country2.grid(column=2, row=3, padx=2)
    score2.grid(column=3, row=3, padx=2)
    win2.grid(column=4, row=3, padx=(2, 0), rowspan=2, sticky=(N, S))
    team2lbl.grid(column=0, row=4, padx=(0, 2))
    team2.grid(column=1, row=4, padx=2, columnspan=3, sticky=(E, W))

    def update_player_names(players_dict):
        names = sorted(players_dict.keys(), key=lambda s: s.casefold())
        name1.set_possible_values(names)
        name2.set_possible_values(names)

        # set comprehension to ensure no repeated team values
        teams = sorted({team for country, team in players_dict.values() if team})
        team1.set_possible_values(teams)
        team2.set_possible_values(teams)

    smashgg_tab.callbacks.append(update_player_names)
    # Update once on init too
    update_player_names(smashgg_tab.players_dict)

    # Actions:
    apply = ttk.Button(actions, text="▶ Apply", command=apply_state)
    discard = ttk.Button(actions, text="✖ Discard", command=discard_unapplied_state)
    reset = ttk.Button(actions, text="↶ Reset scores", command=reset_scores)
    swap = ttk.Button(actions, text="⇄ Swap players", command=swap_players)
    apply.grid(column=0, row=0, padx=(0, 5))
    discard.grid(column=1, row=0, padx=5)
    reset.grid(column=2, row=0, padx=5)
    swap.grid(column=3, row=0, padx=5)

    root.mainloop()


def load_countries():
    with open(COUNTRIES_FILE_PATH, "r") as countries_file:
        countries = countries_file.read().split()
        return countries


def init_states():
    state = {
        "description": StringVar(),
        "p1name": StringVar(),
        "p1country": StringVar(),
        "p1team": StringVar(),
        "p1score": StringVar(),
        "p2name": StringVar(),
        "p2country": StringVar(),
        "p2score": StringVar(),
        "p2team": StringVar(),
    }

    # Attempt to read existing state from file if available
    if os.path.isfile(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r") as state_file:
                state_json = json.load(state_file)

            for field, value in state_json.items():
                if field in state:
                    state[field].set(value)
        except json.decoder.JSONDecodeError:
            print(f"WARNING: {STATE_FILE_PATH} doesn't contain valid json.")
            print("Starting with empty state. The file will be overwritten on Apply.")

    applied_state = {field: tk_var.get() for field, tk_var in state.items()}

    return state, applied_state


def player_wins(state, player):
    score_field = f"p{player}score"
    try:
        score = int(state[score_field].get())
    except ValueError:
        score = 0
    state[score_field].set(score + 1)


def apply_state(state, applied_state):
    for field, tk_var in state.items():
        new_value = tk_var.get()
        applied_state[field] = new_value
        # need to trigger "on change" event which changes widget
        # back to default style:
        tk_var.set(new_value)

    with open(STATE_FILE_PATH, "w") as state_file:
        content = json.dumps(applied_state, indent=2)
        state_file.write(content)


def discard_unapplied_state(state, applied_state):
    for field, tk_var in state.items():
        tk_var.set(applied_state[field])


def reset_scores(state):
    state["p1score"].set("0")
    state["p2score"].set("0")


def swap_players(state):
    score1, score2 = state["p1score"].get(), state["p2score"].get()
    name1, name2 = state["p1name"].get(), state["p2name"].get()
    country1, country2 = state["p1country"].get(), state["p2country"].get()
    team1, team2 = state["p1team"].get(), state["p2team"].get()
    state["p1score"].set(score2)
    state["p2score"].set(score1)
    state["p1name"].set(name2)
    state["p2name"].set(name1)
    state["p1country"].set(country2)
    state["p2country"].set(country1)
    state["p1team"].set(team2)
    state["p2team"].set(team1)


def trace_widget(state, applied_state, widget, field_name, style_name="TEntry"):
    # Bind widget to relevant variable in state and highlight when
    # the widget's value differs from applied_state

    widget.configure(textvariable=state[field_name])

    def on_change_callback(*args):
        if state[field_name].get() != applied_state[field_name]:
            widget.configure(style=f"Active.{style_name}")
        else:
            widget.configure(style=style_name)

    state[field_name].trace("w", on_change_callback)


if __name__ == "__main__":
    # Need to init Tk before creating any StringVar instance
    root = Tk()
    state, applied_state = init_states()

    countries = load_countries()

    smashgg_tab = SmashggTab()

    # TOREFACTOR
    def sync_func(name_field, country_field, *args):
        name = state[name_field].get()
        player_data = smashgg_tab.players_dict.get(name)
        if player_data:
            country, _ = player_data
            state[country_field].set(country)

    state["p1name"].trace("w", partial(sync_func, "p1name", "p1country"))
    state["p2name"].trace("w", partial(sync_func, "p2name", "p2country"))
    # END TOREFACTOR

    build_ui(
        root=root,
        countries=countries,
        smashgg_tab=smashgg_tab,
        p1_wins=partial(player_wins, state, 1),
        p2_wins=partial(player_wins, state, 2),
        apply_state=partial(apply_state, state, applied_state),
        discard_unapplied_state=partial(discard_unapplied_state, state, applied_state),
        reset_scores=partial(reset_scores, state),
        swap_players=partial(swap_players, state),
        trace_widget=partial(trace_widget, state, applied_state),
    )
