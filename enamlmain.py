import enaml
from atom.api import Atom, Range, Str, Value
from enaml.qt.qt_application import QtApplication


class Player(Atom):
    name = Str()
    country = Str()
    team = Str()
    score = Range(low=0)


class Game(Atom):
    match_description = Str()
    player1 = Value(Player)
    player2 = Value(Player)


def init_state() -> Game:
    return Game(
        match_description="Poverty Cup Grand Finals",
        player1=Player(name="Daigo", country="jp", score=1, team="Team One"),
        player2=Player(name="Infiltration", country="kr", score=0, team="Team Two"),
    )


def main():
    with enaml.imports():
        from enamlview import Main

    app = QtApplication()
    view = Main(state=init_state())
    view.show()

    app.start()


if __name__ == "__main__":
    main()
