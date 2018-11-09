# Overly Repetitive Tedious Software

![screenshot-1][img1]

![screenshot-1][img2]

![screenshot-2][img3]

ORTS is a [StreamControl][1] ripoff with an opionated set of quality-of-life features:

- **Visible diff & easy undo**: Changes not yet applied to stream are highlighted and
  can be discarded with the Discard button (duh).

- **Player name + country import**: Currently supports smash.gg. data is saved as a csv
  file which can then be updated manually using any (decent) spreadsheet editor.

- **Better player name lookup**: Matches names _containing_ your query rather than
  _starting with_.

- **Cross-platform**: Tested on Windows & Linux. Should work on OS X too but I don't use
  it so you're on your own.

# Downloads

- Windows: Get the latest build [from AppVeyor][2].
- Linux: Can already be built on travis but I haven't uploaded the results yet.

I'll properly config appveyor/travis to push built artifacts to GitHub Release sometime
later. Soon. Ish.

# How to use

- Run the **orts** executable
- Open OBS => Add browser source => Point to **web/index.html**
- Browser size must be 1920x1080

# How to develop

Requires python 3.7 because we need the added-in-3.7 `ttk.Spinbox` widget.
I also use [poetry][3], so instead of pip, just run `poetry install` to install dependencies.

Build for Windows: see appveyor config  
Build for Linux: see Makefile

[1]: http://farpnut.net/streamcontrol/
[2]: https://ci.appveyor.com/project/nhanb/orts/build/artifacts
[3]: https://github.com/sdispater/poetry

[img1]: https://user-images.githubusercontent.com/1446315/48240507-93c60e00-e405-11e8-905a-67d33d8c5e43.png
[img2]: https://user-images.githubusercontent.com/1446315/48239575-f7e6d300-e401-11e8-9553-1e1f67a50d23.png
[img3]: https://user-images.githubusercontent.com/1446315/48239574-f7e6d300-e401-11e8-9dce-f41154285aef.png
