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
signals = []

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
    if not frames in st.session_state:
        st.session_state.frames = []
    if not "n_frames" in st.session_state:
        st.session_state.n_frames = 0
    frame_creator = st.container()
    add_remove_frames = st.container()
    with frame_creator:
        with st.form("frameBuilder"):
            c1 = st.container()
            c2 = st.container()
            with c2:
                submit = st.form_submit_button("Confirm Frames")
    with add_remove_frames:
        st.write("Add or remove Frames")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Frame"):
                st.session_state['n_frames'] += 1
        with col2:
            if st.button("Remove Frame"):
                st.session_state['n_frames'] -= 1
                st.session_state.pop(f"frame{st.session_state.n_frames}")
    for x in range(st.session_state['n_frames']):
        with c1:
            st.write(f"Frame {x}")
            if not f"frame{x}" in st.session_state:
                st.session_state[f"frame{x}"] = {}
            create_frame(f"{x}")
    # handle the frames
    if submit:
        for x in range(st.session_state['n_frames']):
            if f"frame{x}" in st.session_state:
                st.write(st.session_state[f"frame{x}"])
            else:
                st.write(st.session_state)
    # signal maker section

def signal_creator():
    # get a list of all the frame names
    frame_names = []
    for x in range(st.session_state['n_frames']):
        frame_names.append(st.session_state[f"frame{x}"]["name"])
    # get the frame name
    frame_name = st.selectbox("Frame", frame_names)
    # get the frame id
    # frame_id = st.session_state[f"frame{frame_names.index(frame_name)}"]["id"]
    if not signals in st.session_state:
        st.session_state.signals = []
    if not "n_signals" in st.session_state:
        st.session_state.n_signals = 0
    signals_creator = st.container()
    add_remove_signals = st.container()
    with signals_creator:
        with st.form("signalBuilder"):
            c3 = st.container()
            c4 = st.container()
            with c4:
                submit = st.form_submit_button("Confirm Signals")
    with add_remove_signals:
        st.write("Add or remove Signals")
        sigcol1, sigcol2, sigcol3 = st.columns(3)

        with sigcol1:
            if st.button("Add Signal"):
                st.session_state['n_signals'] += 1
        with sigcol2:    
            if st.button("Remove Signal") and st.session_state['n_signals'] > 0:
                st.session_state['n_signals'] -= 1
                st.session_state.pop(f"{st.session_state.n_signals}")
        with sigcol3:
            if st.button("clear signals"):
                while st.session_state['n_signals'] > 0:
                    st.session_state['n_signals'] -= 1
                    st.session_state.pop(f"{st.session_state.n_signals}")
        # subheader for confirming signals
        st.subheader("Click the button to confirm signals")
        if st.button("confirm signals"):
            # clear the signals if they exist
            if f"frame{frame_names.index(frame_name)}" in st.session_state:
                st.session_state[f"frame{frame_names.index(frame_name)}"].pop("signals")
                st.session_state[f"frame{frame_names.index(frame_name)}"]["signals"] = []
            # bind the signals to the frame
            for i in range(st.session_state['n_signals']):
                st.session_state[f"frame{frame_names.index(frame_name)}"]['signals'].append(st.session_state[f"{i}"])
            pass
    for x in range(st.session_state['n_signals']):
        with c3:
            st.write(f"Signal {x}")
            create_signal(f"{x}")
    # handle the frames
    if submit:
        for x in range(st.session_state['n_frames']):
            if f"frame{x}" in st.session_state:
                st.write(st.session_state[f"frame{x}"])
            else:
                st.write(st.session_state)
    # signal maker section


def write_dbc(dbc_name,state,mode):
    info = []
    for x in range(state['n_frames']):
        info.append(state[f"frame{x}"])
    # represent each frame as a string with signals under it
    dbc_strings = []
    for frame in info:
        dbc_strings.append(f"BO_ {frame['id']} {frame['name']}: {frame['length']} {frame['node']}\n")
        for signal in frame['signals']:
            dbc_strings.append(f" SG_ {signal['name']} : {signal['start']}|{signal['length']}@{signal['byte_order']}+ ({signal['scale']},{signal['offset']}) [{signal['minimum']}|{signal['maximum']}] \"{signal['unit']}\" {signal['choices']}\n")
    # write the database
    # db_file = open(f"{dbc_name}.dbc", "w")
    # db_file.write("VERSION \"\"\n\n")
    # db_file.write("NS_ :\n\n")
    # db_file.write("BS_:\n\n")
    # for dbc_string in dbc_strings:
    #     db_file.write(dbc_string)
    # db_file.close()

    # create the list of strings to output
    dbc_strings.insert(0, "VERSION \"\"\n\n")
    dbc_strings.insert(1, "NS_ :\n\n")
    dbc_strings.insert(2, "BS_:\n\n")
    if mode == "write":
        db_file = open(f"{dbc_name}.dbc", "w")
        for dbc_string in dbc_strings:
            db_file.write(dbc_string)
        db_file.close()
    else:
        return dbc_strings
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
    try:
        signals = st.session_state[f"frame{frame_number}"]['signals']
    except:
        signals = ['theres an error']
    # add the frame to the session state
    add_frame = True
    if add_frame:
        st.session_state[f"frame{frame_number}"] = {
            'name': frame_name,
            'id': frame_id,
            'length': frame_length,
            'node': frame_node,
            'signals': signals
        }
        st.write("Frame added")
    
def create_signal(signal_number):
    # get a signal name
    signal_name = st.text_input("Enter a signal name", "Signal1",key=f"Signal_name_{signal_number}")
    # get a signal start
    signal_start = st.text_input("Enter a signal start", "0", key=f"Signal_start_{signal_number}")
    # get a signal length
    signal_length = st.text_input("Enter a signal length", "8", key=f"Signal_length_{signal_number}")
    # get a signal byte order
    signal_byte_order = st.text_input("Enter a signal byte order", "0", key=f"Signal_byte_order_{signal_number}")
    # get a signal is signed
    signal_is_signed = st.text_input("Enter a signal is signed", "0", key=f"Signal_is_signed_{signal_number}")
    # get a signal is float
    signal_is_float = st.text_input("Enter a signal is float", "0", key=f"Signal_is_float_{signal_number}")
    # get a signal scale
    signal_scale = st.text_input("Enter a signal scale", "1", key=f"Signal_scale_{signal_number}")
    # get a signal offset
    signal_offset = st.text_input("Enter a signal offset", "0", key=f"Signal_offset_{signal_number}")
    # get a signal minimum
    signal_minimum = st.text_input("Enter a signal minimum", "0", key=f"Signal_minimum_{signal_number}")
    # get a signal maximum
    signal_maximum = st.text_input("Enter a signal maximum", "0", key=f"Signal_maximum_{signal_number}")
    # get a signal unit
    signal_unit = st.text_input("Enter a signal unit", "None", key=f"Signal_unit_{signal_number}")
    # get a signal choices
    signal_choices = st.text_input("Enter a signal Node", "Vector_XXX", key=f"Signal_choices_{signal_number}")
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
    
    st.session_state[signal_number] = {
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
    st.write("Frame added")
    pass
def main():
    
    st.title("DBC Parser")
    st.write("This is a simple DBC parser that will parse a DBC file and display the frames and signals in a table.")
    st.write("The DBC file must be in the same directory as this script.")
    # dbc_file = st.text_input("DBC File Name", "dbc_example.dbc")


    # select read or write
    st.write("Select a mode")
    mode = st.selectbox("Mode", ["Read", "Write"])
    if mode == "Read":
        dbc_file = st.file_uploader("Upload DBC File", type="dbc")
        # read the dbc file
        if dbc_file:
            db = cantools.database.load_string(dbc_file)
            render_viewer(db)
        else:
            st.write("No DBC file selected")
        
    elif mode == "Write":
        st.write("Writer coming soon!")
        st.session_state['signals']= []
        returned_info = render_frame_writer()
        signal_info = signal_creator()
        # show frames
        st.write("state dump")
        st.write(st.session_state)
        # file writer
        dbc_name = st.text_input("DBC File Name", "dbc_example.dbc")
        file_write_button = st.button("Write DBC File")
        if file_write_button:
            write_dbc(dbc_name, st.session_state,"write")
            st.write('Hello World!')
    pass
    
if __name__ == "__main__":
    main()