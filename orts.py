import os
import json
from functools import partial
from tkinter import Tk, N, S, E, W, StringVar
from tkinter import ttk

STATE_FILE_PATH = "./web/state.json"
COUNTRIES_FILE_PATH = "./data/countries.txt"


def build_ui(
    *,
    root,
    countries,
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

    # Main frames:
    rootframe = ttk.Frame(root, padding=5)
    rootframe.grid(column=0, row=0)
    misc = ttk.Frame(rootframe, padding=(0, 0, 0, 7))
    players = ttk.Frame(rootframe, padding=(0, 0, 0, 0))
    actions = ttk.Frame(rootframe, padding=(0, 7, 0, 0))
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
    name1lbl = ttk.Label(players, text="Player 1")
    name2lbl = ttk.Label(players, text="Player 2")
    name1 = ttk.Entry(players, width="30")
    trace_widget(name1, "p1name", "TEntry")
    name2 = ttk.Entry(players, width="30")
    trace_widget(name2, "p2name", "TEntry")
    country1 = ttk.Combobox(players, width="6", values=countries)
    trace_widget(country1, "p1country", "TCombobox")
    country2 = ttk.Combobox(players, width="6", values=countries)
    trace_widget(country2, "p2country", "TCombobox")
    score1 = ttk.Spinbox(players, from_=0, to=777, width="4")
    trace_widget(score1, "p1score", "TSpinbox")
    score2 = ttk.Spinbox(players, from_=0, to=777, width="4")
    trace_widget(score2, "p2score", "TSpinbox")
    win1 = ttk.Button(players, text="▲ Win", width="6", command=p1_wins)
    win2 = ttk.Button(players, text="▲ Win", width="6", command=p2_wins)

    name1lbl.grid(column=0, row=0, padx=(0, 2))
    name1.grid(column=1, row=0, padx=2)
    country1.grid(column=2, row=0, padx=2)
    score1.grid(column=3, row=0, padx=2)
    win1.grid(column=4, row=0, padx=(2, 0), pady=(0, 3))

    name2lbl.grid(column=0, row=1, padx=(0, 2))
    name2.grid(column=1, row=1, padx=2)
    country2.grid(column=2, row=1, padx=2)
    score2.grid(column=3, row=1, padx=2)
    win2.grid(column=4, row=1, padx=(2, 0))

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
        "p1score": StringVar(),
        "p2name": StringVar(),
        "p2country": StringVar(),
        "p2score": StringVar(),
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
    score = int(state[score_field].get())
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
    state["p1score"].set(score2)
    state["p2score"].set(score1)
    state["p1name"].set(name2)
    state["p2name"].set(name1)
    state["p1country"].set(country2)
    state["p2country"].set(country1)


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
    build_ui(
        root=root,
        countries=countries,
        p1_wins=partial(player_wins, state, 1),
        p2_wins=partial(player_wins, state, 2),
        apply_state=partial(apply_state, state, applied_state),
        discard_unapplied_state=partial(discard_unapplied_state, state, applied_state),
        reset_scores=partial(reset_scores, state),
        swap_players=partial(swap_players, state),
        trace_widget=partial(trace_widget, state, applied_state),
    )
