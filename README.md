# random-xkcd
Python script that displays a random comic from xkcd. Currently only works on Windows however Linux and MacOS users only need to change a few lines (msg and TEMP_ICON_PATH).

## Prerequisites
- Tkinter
  - In Windows and MacOS, Tkinter comes with Python unless you uncheck Tk/Tcl during installation **or** you are using the portable zip.
  - In Linux, depending on your distribution, you will have to install an additional package `python3-tk` or `python3-tkinter`.
- Requests
  - In Windows and MacOS, this package can be installed by running the following command: `python -m pip install requests`
  - In Linux, you will have to install an additional package `python3-requests`.
- Pillow
  - In Windows and MacOS, this package can be installed by running the following command: `python -m pip install pillow`
  - In Linux, you will have to install an additional package `python3-pillow`.
