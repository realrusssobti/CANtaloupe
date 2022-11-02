# CANtaloupe
## _Define CAN Frames, seamlessly_



CANtaloupe is a Python-powered web application that creates CAN DBC files using a simple web form. 
- Define your frames
- Define your signals for each frame
- ✨Magic ✨

## Features

- Import a DBC file and watch it magically convert to something more readable
- Export your created DBC file
- Create a fully custom DBC - choose your own adventure!

## Quickstart

> Basically, all you have to do is ensure you have the requirements, then run the following command:

```
streamlit run cantools_can.py
```
Eventually, I'll package this nicely into an executable file for you Windows users, but for now you can deal with it
## How this works!

Dillinger uses a Streamlit to render its UI, and cantools to read DBC files.

## Installation

CANtaloupe requires Python 3.7 or higher to run. 
Install the dependencies and devDependencies and start the server.

```sh
pip3 install -r requirements.txt
```

When you're done...

```sh
streamlit run cantools_can.py
```

## TODO

Lots of things! Make things not suck! 
Extend the functionality such that signals can be validated
Edit an existing CAN DBC file instead of having to either read it or write it from scratch. 
| Feature | Status |
| ------ | ------ |
| Refactor | in progress |
| Form Validation | todo |
| UX improvements | todo |
| Remove need to confirm frames and signals | todo |

## Development

Want to contribute? Great!

Edit the source code, and create a branch! I'd love to see your code and merge it to master if you build something cool!

## License

MIT

**Free Software, Hell Yeah!**
