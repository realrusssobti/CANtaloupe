# CANWeb: Web application for reading and defining CAN databases
## Installation
### Requirements
* Python 3.6 or higher
* streamlit
* pandas
* cantools
### How to run
* Clone the repository
* Install the requirements
* Run the application with `streamlit run cantools_can.py`
## Usage
### Reading a database
* Select a database file
* Select "Read" mode
* Select a message
* Scroll down to see the message's signals
* It's already human readable, no need to do anything else
### Defining a database
* Select a database file (can be whatever.dbc)
* Select "Write" mode
* Define your frames
* Scroll down and define your signals
* Click "Write" to write the database to a file
## Known issues
* An existing DBC file is required to access the writer (this is just a stupid design choice i will fix later)
* The writer is not functional at this point
* The source code is absolute spaghetti right now, please don't judge lol