import streamlit as st
# from mods.header import *

import os
import shutil
import streamlit as st

def organize_files(source_dir, destination_dir):
    # Create destination directories if they don't exist
    for ext in extensions:
        directory = os.path.join(destination_dir, ext)
        os.makedirs(directory, exist_ok=True)

    # Organize files based on their extensions
    for file in os.listdir(source_dir):
        if os.path.isfile(os.path.join(source_dir, file)):
            _, file_extension = os.path.splitext(file)
            if file_extension.lower() in extensions:
                shutil.move(os.path.join(source_dir, file), os.path.join(destination_dir, file_extension.lower(), file))

def main():
    st.title("File Organizer")

    # Sidebar inputs
    st.sidebar.header("Settings")
    source_dir = st.sidebar.text_input("Source Directory", "/path/to/source")
    destination_dir = st.sidebar.text_input("Destination Directory", "/path/to/destination")

    # Select extensions to organize
    st.sidebar.subheader("Extensions to Organize")
    extensions = st.sidebar.multiselect("Select Extensions", ['.pdf', '.txt', '.jpg', '.png'])

    # Button to organize files
    if st.sidebar.button("Organize Files"):
        organize_files(source_dir, destination_dir)
        st.success("Files organized successfully!")

if __name__ == "__main__":
    main()
