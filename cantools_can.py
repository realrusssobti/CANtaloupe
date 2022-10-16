import cantools
import pprint as pp
# def main():
#     db = cantools.database.load_file('dbc_example.dbc')
#     print(db.messages)
#     pp.pprint(db.messages[0].signals)
    
# if __name__ == '__main__':
#     main()

#Tkinter GUI
import streamlit as st
import pandas as pd
import cantools
import pprint as pp
import os

def signal_to_dict(signal):
    # The keys are :
    '''
    name, start, length, byte_order, is_signed, is_float, scale, offset, minimum, maximum, decimal, unit, choices
    '''
    # The values are from the Signal object
    signal_dict = {
        'name': signal.name,
        'start': signal.start,
        'length': signal.length,
        'byte_order': signal.byte_order,
        'is_signed': signal.is_signed,
        'is_float': signal.is_float,
        'scale': signal.scale,
        'offset': signal.offset,
        'minimum': signal.minimum,
        'maximum': signal.maximum,
        'unit': signal.unit,
        'choices': signal.choices
    }
    return signal_dict
    pass
def render_viewer(db):
    #Frame selector
    st.write("Select a Frame")
    message_dict = {
        message.name: message for message in db.messages
    }
    frame = st.selectbox("Frame", message_dict)
    #Signal viewer as a table
    st.write("Signals")
    for signal in message_dict[frame].signals:
        st.write(signal.name)
        st.write(signal_to_dict(signal))
    pass

def render_editor(db):
    pass
def render_writer(db):
    # create a new message
    message = db.add_message(
    )
    pass
def main():
    
    st.title("DBC Parser")
    st.write("This is a simple DBC parser that will parse a DBC file and display the frames and signals in a table.")
    st.write("The DBC file must be in the same directory as this script.")
    # dbc_file = st.text_input("DBC File Name", "dbc_example.dbc")
    dbc_file = st.file_uploader("Upload DBC File", type="dbc")
    if dbc_file:
        dbc_file = dbc_file.read()
        dbc_file = dbc_file.decode("ISO-8859-1")
    
        if dbc_file:
            db = cantools.database.load_string(dbc_file)
            # select read or write
            st.write("Select a mode")
            mode = st.selectbox("Mode", ["Read", "Write"])
            if mode == "Read":
                render_viewer(db)
            elif mode == "Write":
                st.write("Writer coming soon!")
                pass
            pass
            
        else:
            st.write("DBC file not found.")
    else:
        st.write("Please upload a DBC file.")
    pass

main()