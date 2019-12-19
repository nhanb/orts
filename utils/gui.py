import enaml


# TODO investigate what dimensions we'll need for multi-size icons
def load_icon(filename):
    with open(filename, "rb") as f:
        data = f.read()
        image = enaml.image.Image(data=data)
        return enaml.icon.Icon(images=[enaml.icon.IconImage(image=image)])


def swap_players(state):
    state.p1name, state.p2name = state.p2name, state.p1name
    state.p1country, state.p2country = state.p2country, state.p1country
    state.p1score, state.p2score = state.p2score, state.p1score
    state.p1team, state.p2team = state.p2team, state.p1team
