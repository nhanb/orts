# Overly Repetitive Tedious Software

![screenshot-1][img1]

![screenshot-1][img2]

![screenshot-2][img3]

ORTS is a [StreamControl][1] ripoff with an opinionated set of quality-of-life features:

- **Visible diff & easy undo**: Changes not yet applied to stream are highlighted and
  can be discarded with the Discard button (duh).

- **Player name + country import**: Currently supports smash.gg. data is saved as a csv
  file which can then be updated manually using any (decent) spreadsheet editor.

- **Better player name lookup**: Matches names _containing_ your query rather than
  _starting with_ (one of my pet peeves about StreamControl).

- **Cross-platform**: Tested on Windows & Linux. Should work on OS X too but I don't use
  it so you're on your own.

# Downloads

Stable builds for 64-bit Windows can be found in [Releases][4].

I used to provide Linux builds but glibc/fontconfig versioning shenanigans put me off.
Also I only run streams on Windows so it's just not worth the effort anymore.
It definitely runs on Linux though, since that's where I primarily develop ORTS on.
Simply pull the code & run `poetry install --no-dev`, then `python orts.py`.

# How to use

- Run the **orts** executable.
- Open OBS => Add browser source => Point to **http://localhost:1337**
- Browser size must be 1920x1080.
- If you want to manually tweak player names after importing from smash.gg, edit
  **data/players.csv** with any text editor (notepad++) or spreadsheet editor (excel or
  [libreoffice calc][5] ~~if you're poor like me~~)
- If you want to customize the look, open up the **web** folder and go wild. You only
  need basic HTML/CSS/JS knowledge to work on it. No fancy frameworks.

# How to develop

Requires python >= 3.7 because we need the added-in-3.7 `ttk.Spinbox` widget.
I also use [poetry][3], so instead of pip, just run `poetry install` to install dependencies.

[1]: http://farpnut.net/streamcontrol/
[2]: https://ci.appveyor.com/project/nhanb/orts/build/artifacts
[3]: https://github.com/sdispater/poetry
[4]: https://github.com/nhanb/orts/releases
[5]: https://www.libreoffice.org/discover/calc/
[6]: https://github.com/nhanb/orts/issues/2

[img1]: https://user-images.githubusercontent.com/1446315/57603111-0f5a7080-758b-11e9-9223-001336e6cd62.png
[img2]: https://user-images.githubusercontent.com/1446315/57602797-52681400-758a-11e9-84a5-14452b4e6581.png
[img3]: https://user-images.githubusercontent.com/1446315/57602761-3c5a5380-758a-11e9-9300-91795a5187e1.png
