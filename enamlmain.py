import enaml
from atom.api import Atom, Bool, Range, Str, observe
from enaml.qt.qt_application import QtApplication


class Player(Atom):
    name = Str()
    country = Str()
    team = Str()
    score = Range(low=0)

    debug = Bool(False)

    @observe("score")
    def debug_print(self, change):
        """ Prints out a debug message whenever the player's score changes.

        """
        if self.debug:
            print(f"{self.name} from {self.country} has {self.score} points.")


def main():
    with enaml.imports():
        from enamlview import Main

    p1 = Player(name="Daigo", country="jp", score=1, team="Team One", debug=True)
    p2 = Player(name="Infiltration", country="kr", score=0, team="Team Two", debug=True)

    app = QtApplication()
    view = Main(p1=p1, p2=p2)
    view.show()

    app.start()


if __name__ == "__main__":
    main()
