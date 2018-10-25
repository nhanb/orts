import json
from tkinter import Tk, N, S, E, W, Spinbox
from tkinter import ttk


def apply_state(state={"hello": "world"}):
    with open("./html/state.json", "w") as state_file:
        content = json.dumps(state, indent=2)
        state_file.write(content)


def build_ui():
    # 2 main frames:
    root = Tk()
    content = ttk.Frame(root, padding=(3, 3, 12, 12))
    actions = ttk.Frame(root, padding=(3, 3, 12, 12))
    content.grid(column=0, row=0, sticky=(N, S, E, W))
    actions.grid(column=0, row=1, sticky=(N, S, E, W))

    # Content:
    name1lbl = ttk.Label(content, text="Player 1")
    name2lbl = ttk.Label(content, text="Player 2")
    name1 = ttk.Entry(content)
    name2 = ttk.Entry(content)
    score1 = Spinbox(content, from_=0, to=7777)
    score2 = Spinbox(content, from_=0, to=7777)
    name1lbl.grid(column=0, row=0)
    name1.grid(column=1, row=0)
    score1.grid(column=2, row=0)
    name2lbl.grid(column=0, row=1)
    name2.grid(column=1, row=1)
    score2.grid(column=2, row=1)

    # Actions:
    apply = ttk.Button(actions, text="Apply", command=apply_state)
    reset = ttk.Button(actions, text="Reset")
    apply.grid(column=0, row=0, padx=5)
    reset.grid(column=1, row=0, padx=5)

    root.mainloop()


if __name__ == "__main__":
    build_ui()
