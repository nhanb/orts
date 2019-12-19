import json
import os

import enaml
from atom.api import Atom, Str
from enaml.qt.qt_application import QtApplication

STATE_FILE_PATH = "./web/state.json"


class State(Atom):
    match_description = Str()

    p1name = Str()
    p1country = Str()
    p1score = Str()
    p1team = Str()

    p2name = Str()
    p2country = Str()
    p2score = Str()
    p2team = Str()

    def to_dict(self):
        return {field: getattr(self, field) for field in self.members()}

    def clone_to(self, other):
        data = self.to_dict()
        for field, value in data.items():
            setattr(other, field, value)

    def persist(self):
        with open(STATE_FILE_PATH, "w") as state_file:
            content = json.dumps(self.to_dict(), indent=2)
            state_file.write(content)


def init_states():
    state = State()
    applied_state = State()

    # Attempt to read existing state from file if available
    if os.path.isfile(STATE_FILE_PATH):
        try:
            with open(STATE_FILE_PATH, "r") as state_file:
                state_json = json.load(state_file)

            state_fields = state.members().keys()

            for field, value in state_json.items():
                if field in state_fields:
                    setattr(state, field, value)
                    setattr(applied_state, field, value)

        except json.decoder.JSONDecodeError:
            print(f"WARNING: {STATE_FILE_PATH} doesn't contain valid json.")
            print("Starting with empty state. The file will be overwritten on Apply.")

    return {"state": state, "applied_state": applied_state}


def main():
    with enaml.imports():
        from main_view import Main

    app = QtApplication()
    view = Main(**init_states())
    view.show()

    app.start()


if __name__ == "__main__":
    main()
