# Overly Repetitive Tedious Software

ORTS is a [StreamControl][1] ripoff.

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
