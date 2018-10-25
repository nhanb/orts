import json
from functools import partial
from tkinter import Tk, N, S, E, W, Spinbox, StringVar
from tkinter import ttk


def build_ui(root, state, apply_state, reset_scores, swap_scores):

    # 2 main frames:
    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    actions = ttk.Frame(root, padding=(3, 3, 12, 12))
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    actions.grid(column=0, row=1, sticky=(N, S, E, W))

    # Content:
    name1lbl = ttk.Label(content, text="Player 1")
    name2lbl = ttk.Label(content, text="Player 2")
    name1 = ttk.Entry(content, textvariable=state["p1name"])
    name2 = ttk.Entry(content, textvariable=state["p2name"])
    score1 = Spinbox(content, from_=0, to=7777, textvariable=state["p1score"])
    score2 = Spinbox(content, from_=0, to=7777, textvariable=state["p2score"])
    name1lbl.grid(column=0, row=0)
    name1.grid(column=1, row=0)
    score1.grid(column=2, row=0)
    name2lbl.grid(column=0, row=1)
    name2.grid(column=1, row=1)
    score2.grid(column=2, row=1)

    # Actions:
    apply = ttk.Button(actions, text="Apply", command=apply_state)
    reset = ttk.Button(actions, text="Reset", command=reset_scores)
    swap = ttk.Button(actions, text="Swap", command=swap_scores)
    apply.grid(column=0, row=0, padx=5)
    reset.grid(column=1, row=0, padx=5)
    swap.grid(column=2, row=0, padx=5)

    root.mainloop()


def apply_state(state):
    with open("./html/state.json", "w") as state_file:
        state_json = {field: var.get() for field, var in state.items()}
        content = json.dumps(state_json, indent=2)
        state_file.write(content)


def reset_scores(state):
    state["p1score"].set("0")
    state["p2score"].set("0")


def swap_scores(state):
    score1, score2 = state["p1score"].get(), state["p2score"].get()
    state["p1score"].set(score2)
    state["p2score"].set(score1)


if __name__ == "__main__":
    # Need to init Tk before creating any StringVar instance
    root = Tk()

    state = {
        "p1name": StringVar(),
        "p1score": StringVar(),
        "p2name": StringVar(),
        "p2score": StringVar(),
    }

    build_ui(
        root,
        state,
        apply_state=partial(apply_state, state),
        reset_scores=partial(reset_scores, state),
        swap_scores=partial(swap_scores, state),
    )
