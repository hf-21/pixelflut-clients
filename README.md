# pixelflut-clients

Various clients for the [pixelflut server].

On the next meeting in person we will start the pixelnuke server (C implementation) on a central PC connected to a beamer and every client can and will be used to modify the shown image. Feel free to contribute!


## How to contribute

Simply create pull requests in this repo to ...

- contribute to the hacktoberfest 2021
- add your own client implementation for the [pixelflut server]


## Contribution guidelines

- Put your different implementations into dedicated subfolders with the following scheme: `<lang>_<name>`.
- Everything which ends with `_utils` are helpers for this specific language.
- Everything inside the root directory which starts with `_*` is ignored by git.

**Examples:**

- `python_utils`
- `go_spraycan`
- `java_snake`
- `rust_tictactoe`


[pixelflut server]: https://github.com/defnull/pixelflut
