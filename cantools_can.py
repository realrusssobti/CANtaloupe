from ast import arg
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

#globals
filename = ""
frames = []
def update_frames(frame):
    global frames
    frames.append(frame)
    pass
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
def render_frame_writer():
    if not "n_frames" in st.session_state:
        st.session_state.n_frames = 0
    frame_creator = st.container()
    add_remove_frames = st.container()
    with frame_creator:
        with st.form("frameBuilder"):
            c1 = st.container()
            c2 = st.container()
            with c2:
                st.form_submit_button("Confirm Frame")
    with add_remove_frames:
        st.write("Add or remove frames")
        if st.button("Add Frame"):
            st.session_state['n_frames'] += 1
        if st.button("Remove Frame"):
            st.session_state['n_frames'] -= 1
            st.session_state.pop(f"frame{st.session_state.n_frames}")
    for x in range(st.session_state['n_frames']):
        with c1:
            st.write(f"Frame {x}")
            create_frame(f"frame{x}")
    
def create_frame(frame_number):
    # get a frame name
    frame_name = st.text_input("Enter a frame name", key=f"Frame_name_{frame_number}")
    # get a frame ID
    frame_id = frame_number
    # get a frame length
    frame_length = st.text_input("Enter a frame length", key=f"Frame_length_{frame_number}")
    # get a frame node
    frame_node = st.text_input("Enter a frame node", "Vector__XXX", key=f"Frame_node_{frame_number}")
    # signals
    signals = []
    
def create_signal():
    # get a signal name
    signal_name = st.text_input("Enter a signal name", "Signal1")
    # get a signal start
    signal_start = st.text_input("Enter a signal start", "0")
    # get a signal length
    signal_length = st.text_input("Enter a signal length", "8")
    # get a signal byte order
    signal_byte_order = st.text_input("Enter a signal byte order", "0")
    # get a signal is signed
    signal_is_signed = st.text_input("Enter a signal is signed", "0")
    # get a signal is float
    signal_is_float = st.text_input("Enter a signal is float", "0")
    # get a signal scale
    signal_scale = st.text_input("Enter a signal scale", "1")
    # get a signal offset
    signal_offset = st.text_input("Enter a signal offset", "0")
    # get a signal minimum
    signal_minimum = st.text_input("Enter a signal minimum", "0")
    # get a signal maximum
    signal_maximum = st.text_input("Enter a signal maximum", "0")
    # get a signal unit
    signal_unit = st.text_input("Enter a signal unit", "None")
    # get a signal choices
    signal_choices = st.text_input("Enter a signal choices", "None")
    # create a signal
    signal = {
        'name': signal_name,
        'start': signal_start,
        'length': signal_length,
        'byte_order': signal_byte_order,
        'is_signed': signal_is_signed,
        'is_float': signal_is_float,
        'scale': signal_scale,
        'offset': signal_offset,
        'minimum': signal_minimum,
        'maximum': signal_maximum,
        'unit': signal_unit,
        'choices': signal_choices
    }
    # return signal
    return {"signal": signal}
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
                frames = []
                returned_info = render_frame_writer()
                if returned_info:
                    filename = returned_info["filename"]
                    if returned_info["frame"]:
                        frames.append(returned_info["frame"])
                # show frames
                st.write("Frames")
                if frames == []:
                    st.write("No frames")
                for frame in frames:
                    st.write(frame)

                pass
            pass
            
        else:
            st.write("DBC file not found.")
    else:
        st.write("Please upload a DBC file.")
    pass

main()