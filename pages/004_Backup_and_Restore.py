import streamlit as st
import pymongo
import datetime
import tempfile
import shutil
import os
from zipfile import ZipFile

from mods.header import *
from mods.data_processing import *
# from mods.auth import *
from mods.utils import *
from mods.models import *


# Streamlit UI
st.title("MongoDB Backup and Restore")

# Backup Section
st.header("Backup MongoDB")

db_choice = st.selectbox("Backup which database:", CLIENT.list_database_names())

db = CLIENT[db_choice]

def fetch_collection_names(db):
    """Fetches and returns the list of collection names in the database."""
    return db.list_collection_names()

coll_choice = st.selectbox("Backup which collection: ", fetch_collection_names(db))
    
if st.button("Backup"):
    backup_collection(db.coll_choice)

# Restore Section
st.header("Restore MongoDB")

# File uploader for backup file
uploaded_file = st.file_uploader("Upload a backup ZIP file", type=["zip"])

if uploaded_file:
    # Extract uploaded ZIP file
    temp_dir = tempfile.mkdtemp()
    uploaded_file_path = os.path.join(temp_dir, "uploaded_backup.zip")
    with open(uploaded_file_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    with ZipFile(uploaded_file_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)

    # Restore MongoDB database
    os.system(f"mongorestore --drop --db your_database {temp_dir}")

    st.success("Database restored successfully!")

    # Clean up temporary directory
    shutil.rmtree(temp_dir)
