#########################
#*  MONGODB Utilities  *#
#########################

import streamlit as st
import pymongo
from pymongo import MongoClient, DESCENDING, ASCENDING
# from pymongo import bson
# from pymongo.server_api import ServerApi
import os
import shutil
import tempfile
from datetime import datetime, timedelta
import zipfile
import pydantic
# from pydantic_settings import BaseSettings
# import streamlit_pydantic as sp


#st.sidebar.error('Initializing search_term...')
if 'search_term' not in st.session_state:
    #st.sidebar.error('search_term not found in session_state. Initializing...')
    st.session_state['search_term'] = ''    
    #st.sidebar.error(f'Current search_term:  {st.session_state.search_term}')
else:    
    st.sidebar.error(f'Current search_term: {st.session_state.search_term}')

if 'filter_option' not in st.session_state:
    st.session_state.filter_option = { 'is_done' : False } 

if 'sort' not in st.session_state:
    st.session_state.sort = 'timestamp'

print(f' \n st.session_state.sort: {st.session_state.sort}')
    
if 'srt_order' not in st.session_state:
    st.session_state.srt_order = -1


def backup_collection(db_name, collection_name):
    # Create a temporary directory to store the backup files
    backup_dir = '/backups/' # tempfile.mkdtemp()
    # Backup MongoDB collection
    st.sidebar.error(f'db_name: {db_name}, collection_name: {collection_name}')
    backup_filepath = os.path.join(backup_dir, f'{db_name}-{collection_name}_backup_' + datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    os.system(f'mongodump --db your_database --collection {collection_name} --out {backup_filepath}.bson')
    # Create a ZIP file containing the backup files
    zip_file = os.path.join(backup_dir, f'{backup_filepath}.zip')
    with zipfile.ZipFile(zip_file, 'w') as zipObj:
        for folderName, _, filenames in os.walk(backup_dir):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.relpath(filePath, backup_dir))
    return zip_file
    

# TODO: remove hard-coded search term

# Set up db connection
@st.cache_resource
def setup_db_conn(conn_string):
    client = MongoClient(conn_string)
    return client

if os.path.exists('/.dockerenv'):
    print(' \n Running in Docker container \n ')
    HOST = st.secrets.mongo.host
else:
    print(' \n Not running in Docker container (assuming it\'s development environment) \n ')
    HOST = st.secrets.mongo.host_dev

# CONN_STRING = os.environ['CONN_STRING']
# SERVER_API = os.environ['SERVER_API']

SERVER_API = st.secrets.mongo.server
PORT = st.secrets.mongo.port

CONN_STRING = f'mongodb://{HOST}:{PORT}'# , {SERVER_API}'
# st.write(f'CONN_STRING: {CONN_STRING}')
CLIENT = setup_db_conn(CONN_STRING)

#st = st.empty()
#SBAR_CONTAINER = st.empty()

# Set up db connection
# @st.cache_resource
def setup_db_conn(conn_string):
    client = MongoClient(conn_string, SERVER_API)
    return client

# Set up db   
# @st.cache_resource
def load_dbs(_client, db):
    return _client.db

# Set up collections
# @st.cache_resource
def load_coll(_db, coll):   
    return _db.coll

# Set up cursors
# @st.cache_resource
def load_cursor(_coll, _filter, _sort, _srt_order):
    cursor = _coll.find(_filter)    
    sorted = cursor.sort(_sort, _srt_order)
    return sorted
    cursor.close()


# TODO: uncomment db-coll line
#st.sidebar.error(f'#1 - st.session_state.sort: {st.session_state.sort}, st.session_state.srt_order: {st.session_state.srt_order}')

GOALS_DB = load_dbs(CLIENT, 'goals')
GOALS_LIST = load_coll(GOALS_DB, 'goals_list')
GOALS_USERS = load_coll(GOALS_DB, 'users')
GOALS_CATEGORIES = load_coll(GOALS_DB, 'categories')
ALL_GOALS = load_cursor(GOALS_LIST, {}, 'timestamp', -1)
DONE_GOALS = load_cursor(GOALS_LIST, {'is_done': True}, 'timestamp', -1)

# TODO: switch to categories table in db
CATEGORIES = ALL_GOALS.distinct('category')
  
def change_sort_order():
    st.session_state.srt_order = st.session_state.srt_order * -1

# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())
        

def add_goal():
    # Create modal (pop up) form
    with st.popover('  \+ &nbsp;&nbsp;  Add &nbsp; :new: &nbsp; goal: &nbsp;&nbsp; \+ '):
        with st.form('add_goal_form'):
            st.write('Add a new goal:')
            category = st.text_input('Category')
            goal_task = st.text_input('Goal Task')
            duedate = date_to_datetime(st.date_input('Due Date', value=datetime.now() + timedelta(days=1)))
            #st.write('Inside the form')
            submitted = st.form_submit_button('Save Goal')
            #submitted = True
            #st.write('Inside the form')
            if submitted:
                #timer = threading.Timer(0.25, close_popover)
                #timer.start()   
                goal_data = {
                    'timestamp': datetime.now(), 
                    'category': category, 
                    'goal_task': goal_task, 
                    'duedate': date_to_datetime(duedate), 
                    'is_done': False 
                }   
                st.write(f'goal_data: {goal_data}')                 
                submit_result = add_new_document(GOALS_LIST, goal_data)  
                st.write(f'submit_result: {submit_result}')   

def add_new_document(_coll, data):
    try:
        st.write('add_new_document() invoked')
        # Attempt to insert the document
        new_id = _coll.insert_one(data)
        # Display success message
        st.success(f'Goal added successfully with id: {new_id.inserted_id}')
        return new_id
        st.rerun()  # Refresh the goal journal
    except Exception as e:
        # Handle any exceptions that occur during the insertion process
        st.warning(f'Failed to save goal: {e}')
        return None

def edit_document_by_id(coll, document_id, new_data):
    try:
        # Attempt to update the document
        update_result = coll.update_one({'_id': document_id}, {'$set': new_data})        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Document updated successfully
            st.success(f'Document with ID {document_id} updated successfully.')
            st.rerun()  # Refresh the goal journal
            return True
        else:
            # Document not updated (no matching document found)
            st.warning(f'No document found with ID {document_id}.')
            return False
    except Exception as e:
        # Handle any exceptions that occur during the update process
        st.error(f'Failed to update document with ID {document_id}: {e}')
        sleep(3)
        return False

def delete_document_by_id(coll, document_id):
    try:
        # Attempt to delete the document
        delete_result = coll.delete_one({'_id': document_id})
        if delete_result.deleted_count == 1:
            st.rerun()       
            st.success(f'Document with ID {document_id} deleted successfully.')
        else:        
            st.warning(f'No document found with ID {document_id}.')
    except Exception as e:
        # Handle any exceptions that occur during the deletion process
        st.error(f'Failed to delete document with ID {document_id}: {e}')
        # sleep(3)

def delete_all_documents(coll):
    delete_all_result = coll.delete_many({})
    # Update the content of the container with your message
    st.success(f'Deleted {delete_all_result.deleted_count} documents from the collection.')
    
def update_specific_string_many(coll, filter, update):
    update_result = coll.update_many(filter, update)
    st.success(f'Updated {update_result.modified_count} documents in the collection.')
    
    query['$text'] = {'$search': search_term} 

# Function to list documents in a collection
def list_documents(db_name, coll_name):
    db = CLIENT[db_name]
    coll = db[coll_name]
    doc = coll.find()
    return doc

def check_existing_doc(coll, new_data):    
    # Check if the new data already exists in the collection
    existing_data = coll.find_one(new_data)
    if existing_data:
        st.warning('Data already exists in the collection, not saved.')
    else:
        st.success('Data does not exist in the collection. Data saved!')
       
def toggle_bool(coll, document_id, bool_field):
    # Retrieve the current document
    current_document = coll.find_one({'_id': document_id})
    if current_document:
        # Toggle the value of the 'is_done' field
        new_value = not current_document.get(bool_field, False)
        # Update the document in the collection
        coll.update_one({'_id': document_id}, {'$set': {bool_field: new_value}})
        return new_value  # Return the new value of bool_field
    else:
        return None  # Document not found


