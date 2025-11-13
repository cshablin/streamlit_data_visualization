import streamlit as st
import pandas as pd


global_df = None


def folder_picker():
    import streamlit as st
    import tkinter as tk
    from tkinter import filedialog

    # Set up tkinter
    root = tk.Tk()
    root.withdraw()

    # Make folder picker dialog appear on top of other windows
    root.wm_attributes('-topmost', 1)

    # Folder picker button
    # st.write('Please select a data folder:')
    clicked = st.button('Folder Picker')
    global dir_path
    if clicked:
        dir_path = st.text_input('Selected folder:', filedialog.askdirectory(master=root))
        from streamlit import caching
        caching.MemoAPI.clear()  # we have caching so if data folder changed we clear
    return dir_path


def dataframe_picker():
    global global_df
    if global_df is None:
        uploaded_file = st.file_uploader("")
        if uploaded_file is not None:
            st.caching.MemoAPI.clear()  # we have caching so we clear
            dataframe = pd.read_csv(uploaded_file)
            global_df = dataframe
        else:
            st.info(f"""👆 select csv file """)
            st.stop()
    return global_df
