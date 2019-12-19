import enaml


# TODO investigate what dimensions we'll need for multi-size icons
def load_icon(filename):
    with open(filename, "rb") as f:
        data = f.read()
        image = enaml.image.Image(data=data)
        return enaml.icon.Icon(images=[enaml.icon.IconImage(image=image)])
