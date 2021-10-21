# pixelflut-clients

Various clients for the [pixelflut server](https://github.com/defnull/pixelflut).

On occasional dates we will sit together at a table and push pixels around on a monitor. The PC connected to the monitor runs a variation of the pixelflus server which everyone can connect to. Don't forget to bring an Ethernet cable.


## How to contribute

Simply create pull requests in this repo to ...

- contribute to the hacktoberfest 2021
- add your own client implementation
- share your work and ieas with others


## Contribution guidelines

- Put your different implementations into dedicated subfolders with the following scheme: `<lang>_<name>`.
- Everything which ends with `_utils` are helpers for this specific language.
- Everything inside the root directory which starts with `_*` is ignored by git.
- For variables like Host, Port, or even font files, please utilize environment variables like the following. You can use [direnv](https://direnv.net/) to export them automatically
  - `PIXELFLUT_HOST`
  - `PIXELFLUT_PORT`
  - `PIXELFLUT_FONT`
