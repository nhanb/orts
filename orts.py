import os
import json
from functools import partial
from tkinter import Tk, N, S, E, W, Spinbox, StringVar
from tkinter import ttk

STATE_FILE_PATH = "./web/state.json"


def build_ui(root, state, apply_state, reset_scores, swap_players):
    root.title("Overly Repetitive Tedious Software")
    # Main frames:
    misc = ttk.Frame(root, padding=(3, 3, 12, 12))
    players = ttk.Frame(root, padding=(3, 3, 12, 12))
    actions = ttk.Frame(root, padding=(3, 3, 12, 12))
    misc.grid(column=0, row=0, sticky=(N, S, E, W))
    players.grid(column=0, row=1, sticky=(N, S, E, W))
    actions.grid(column=0, row=2, sticky=(N, S, E, W))

    # Misc: (fields not belonging to any player)
    descriptionlbl = ttk.Label(misc, text="Match description")
    description = ttk.Entry(misc, textvariable=state["description"])
    descriptionlbl.grid(column=0, row=0)
    description.grid(column=1, row=0, sticky=(E, W))
    misc.grid_columnconfigure(1, weight=1)

    # Players:
    name1lbl = ttk.Label(players, text="Player 1")
    name2lbl = ttk.Label(players, text="Player 2")
    name1 = ttk.Entry(players, textvariable=state["p1name"])
    name2 = ttk.Entry(players, textvariable=state["p2name"])
    score1 = Spinbox(players, from_=0, to=7777, textvariable=state["p1score"])
    score2 = Spinbox(players, from_=0, to=7777, textvariable=state["p2score"])
    name1lbl.grid(column=0, row=0)
    name1.grid(column=1, row=0)
    score1.grid(column=2, row=0)
    name2lbl.grid(column=0, row=1)
    name2.grid(column=1, row=1)
    score2.grid(column=2, row=1)

    # Actions:
    apply = ttk.Button(actions, text="Apply", command=apply_state)
    reset = ttk.Button(actions, text="Reset scores", command=reset_scores)
    swap = ttk.Button(actions, text="Swap players", command=swap_players)
    apply.grid(column=0, row=0, padx=5)
    reset.grid(column=1, row=0, padx=5)
    swap.grid(column=2, row=0, padx=5)

    root.mainloop()


def init_state():
    state = {
        "description": StringVar(),
        "p1name": StringVar(),
        "p1score": StringVar(),
        "p2name": StringVar(),
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

    return state


def apply_state(state):
    with open(STATE_FILE_PATH, "w") as state_file:
        state_json = {field: var.get() for field, var in state.items()}
        content = json.dumps(state_json, indent=2)
        state_file.write(content)


def reset_scores(state):
    state["p1score"].set("0")
    state["p2score"].set("0")


def swap_players(state):
    score1, score2 = state["p1score"].get(), state["p2score"].get()
    name1, name2 = state["p1name"].get(), state["p2name"].get()
    state["p1score"].set(score2)
    state["p2score"].set(score1)
    state["p1name"].set(name2)
    state["p2name"].set(name1)


if __name__ == "__main__":
    # Need to init Tk before creating any StringVar instance
    root = Tk()
    state = init_state()
    build_ui(
        root,
        state,
        apply_state=partial(apply_state, state),
        reset_scores=partial(reset_scores, state),
        swap_players=partial(swap_players, state),
    )
