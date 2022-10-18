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
* Needs a refactor tbh
* Must click confirm frames before adding signals
* Must click confirm signals before writing to file
* No input validation
* Some UI tweaks needed
* the state of the app is visible to the user, which is not ideal