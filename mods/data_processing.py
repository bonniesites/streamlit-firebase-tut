#########################
#*  MONGODB Utilities  *#
#########################

import streamlit as st
from pymongo import MongoClient
#from pymongo.server_api import ServerApi
import os
from datetime import datetime, timedelta
from mods.models import *

# st.write("Initializing search_term...")
if not 'search_term' in st.session_state:
    # st.write("search_term not found in session_state. Initializing...")
    st.session_state.search_term = 'goals'    
    # st.write("Current search_term: ", st.session_state.search_term)
# else:    
    # st.write("Current search_term: ", st.session_state.search_term)

if not 'filter_option' in st.session_state:
    st.session_state.filter_option = { 'is_done' : False } 

if not 'sort' in st.session_state:
    st.session_state.sort = 'post_timestamp' 
    
if not 'sort_order' in st.session_state:
    st.session_state.sort_order = -1


# Set up db connection
@st.cache_resource
def setup_db_conn(conn_string):
    # st.write('setup_db_conn() invoked')
    client = MongoClient(conn_string)
    # st.write(f'\t\t client: {client}')
    return client

# Set up db   
@st.cache_resource
def load_dbs(_client, db):
    # st.write('load_dbs() invoked')
    # st.write(f'_client[db]: {_client[db]}')
    return _client[db]

# Set up collections for CRUD
@st.cache_resource
def load_coll(_db, coll): 
    # st.write('load_coll() invoked')
    # st.write(f'_db[coll]: {_db[coll]}')  
    return _db[coll]

# Set up cursors for iteration/reports/display/printing
@st.cache_resource
def load_cursor(_coll, _filter, _sort): 
    # st.write('load_cursor() invoked')
    cursor = _coll.find(_filter)    
    sorted = cursor.sort(_sort, st.session_state.sort_order)
    # st.write(f'sorted [cursor]: {sorted}')
    return sorted

if os.path.exists("/.dockerenv"):
    print("Running in Docker container")
    HOST = st.secrets.mongo.host
else:
    print("Not running in Docker container (assuming development environment)")
    HOST = st.secrets.mongo.host_dev

SERVER_API = st.secrets.mongo.server
PORT = st.secrets.mongo.port

CONN_STRING = f'mongodb://{HOST}:{PORT}'# , {SERVER_API}'
# st.write(f'CONN_STRING: {CONN_STRING}')
CLIENT = setup_db_conn(CONN_STRING)

# st.write(f'  CLIENT: {CLIENT}')

MSG_CONTAINER = st.empty()
SBAR_CONTAINER = st.empty()


# LIST = load_coll(load_dbs(CLIENT, 'goals'), 'list')

# ALL_GOALS = load_cursor(LIST, st.session_state.filter_option, st.session_state.sort)
  
def change_sort_order():
    pass
    # st.session_state.sort_order = st.session_state.sort_order * -1

def backup_collection(db_name, collection_name):
    # Create a temporary directory to store the backup files
    temp_dir = tempfile.mkdtemp()
    # Backup MongoDB collection
    backup_file = os.path.join(temp_dir, f"{db_name}-{collection_name}_backup_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".bson")
    os.system(f"mongodump --db your_database --collection {collection_name} --out {temp_dir}")
    # Create a ZIP file containing the backup files
    zip_file = os.path.join(temp_dir, f"{collection_name}_backup.zip")
    with ZipFile(zip_file, 'w') as zipObj:
        for folderName, _, filenames in os.walk(temp_dir):
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                zipObj.write(filePath, os.path.relpath(filePath, temp_dir))
    return zip_file

# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())

def add_new_document(_coll, data):
    try:
        # Attempt to insert the document
        new_id = _coll.insert_one(data)
        # Display success message
        MSG_CONTAINER.success(f'Document added successfully with id: {new_id.inserted_id}')
        return new_id
        st.rerun()  # Refresh the goal journal
    except Exception as e:
        # Handle any exceptions that occur during the insertion process
        MSG_CONTAINER.warning(f'Failed to save document: {e}')
        return None

def edit_document_by_id(coll, document_id, new_data):
    try:
        # Attempt to update the document
        update_result = coll.update_one({"_id": document_id}, {"$set": new_data})        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Document updated successfully
            MSG_CONTAINER.success(f"Document with ID {document_id} updated successfully.")
            st.rerun()  # Refresh the goal journal
            return True
        else:
            # Document not updated (no matching document found)
            MSG_CONTAINER.warning(f"No document found with ID {document_id}.")
            return False
    except Exception as e:
        # Handle any exceptions that occur during the update process
        MSG_CONTAINER.error(f"Failed to update document with ID {document_id}: {e}")
        sleep(3)
        return False

def delete_document_by_id(coll, document_id):
    try:
        # Attempt to delete the document
        delete_result = coll.delete_one({"_id": document_id})
        if delete_result.deleted_count == 1:
            st.rerun()       
            MSG_CONTAINER.success(f"Document with ID {document_id} deleted successfully.")
        else:        
            MSG_CONTAINER.warning(f"No document found with ID {document_id}.")
    except Exception as e:
        # Handle any exceptions that occur during the deletion process
        MSG_CONTAINER.error(f"Failed to delete document with ID {document_id}: {e}")
        sleep(3)

def delete_all_documents(coll):
    delete_all_result = coll.delete_many({})
    # Update the content of the container with your message
    MSG_CONTAINER.success(f"Deleted {delete_all_result.deleted_count} documents from the collection.")
    
def update_specific_string_many(coll, filter, update):
    update_result = coll.update_many(filter, update)
    MSG_CONTAINER.success(f"Updated {update_result.modified_count} documents in the collection.")    
    query['$text'] = {'$search': search_term} 

# Function to list documents in a collection
def list_documents(db_name, coll_name):
    db = CLIENT[db_name]
    coll = db[coll_name]
    docs = coll.find()
    return doc

    
def check_existing_doc(coll, new_data):    
    # Check if the new data already exists in the collection
    existing_data = coll.find_one(new_data)
    if existing_data:
        MSG_CONTAINER.success("Data already exists in the collection")
    else:
        MSG_CONTAINER.warning("Data does not exist in the collection")

       
def toggle_bool(coll, document_id, bool_field):
    # Retrieve the current document
    current_document = coll.find_one({"_id": document_id})
    if current_document:
        # Toggle the value of the "is_done" field
        new_value = not current_document.get(bool_field, False)
        # Update the document in the collection
        coll.update_one({"_id": document_id}, {"$set": {bool_field: new_value}})
        return new_value  # Return the new value of bool_field
    else:
        return None  # Document not found


REDDIT_DB = load_dbs(CLIENT, 'reddit_clone')
REDDIT_POSTS = load_coll(REDDIT_DB, 'posts')
REDDIT_USERS = load_coll(REDDIT_DB, 'users')
REDDIT_COMMENTS = load_coll(REDDIT_DB, 'comments')
REDDIT_LIKES = load_coll(REDDIT_DB, 'likes')
REDDIT_DISLIKES = load_coll(REDDIT_DB, 'dislikes')
REDDIT_FLAGS = load_coll(REDDIT_DB, 'flags')

# Sorted Cursors for reports/displays
ALL_REDDIT_POSTS = load_cursor(REDDIT_POSTS, {}, st.session_state.sort)
ALL_REDDIT_USERS = load_cursor(REDDIT_USERS, {}, st.session_state.sort)
ALL_REDDIT_COMMENTS = load_cursor(REDDIT_COMMENTS, {}, st.session_state.sort)
ALL_REDDIT_LIKES = load_cursor(REDDIT_LIKES, {}, st.session_state.sort)
ALL_REDDIT_POSTS = load_cursor(REDDIT_POSTS, {}, st.session_state.sort)
ALL_REDDIT_DISLIKES = load_cursor(REDDIT_DISLIKES, {}, st.session_state.sort)
ALL_REDDIT_FLAGS = load_cursor(REDDIT_FLAGS, {}, st.session_state.sort)


def add_post(data):    
        new_id = REDDIT_POSTS.insert_one(data)
        if new_id:
            st.write(f':tada: Post Added with id of {new_id}!')
            st.balloons()
            st.rerun()    
            title, content, file_path, url
        

def edit_post(record_id, title=None, content=None, author=None, image=None, post_url=None):
    # Create an update object
    update_data = {}    
    if title is not None:
        update_data['post_title'] = title
    if content is not None:
        update_data['post_content'] = content
    if author is not None:
        update_data['post_author'] = author
    if image is not None:
        update_data['post_img'] = image
    if post_url is not None:
        update_data['post_url'] = post_url
    # Only proceed if there's something to update
    if update_data:
        REDDIT_POSTS.update_one({'_id': ObjectId(record_id)}, {'$set': update_data})
        # Reload the list if using Streamlit
        st.rerun()

def view_posts(filter, sort, sort_order):
    if REDDIT_POSTS.count_documents({}) > 0:    
        query = load_cursor(REDDIT_POSTS, filter, sort)
        title, title_sort, date_sort, blank_sort = st.columns(4)
        with title:        
            st.header('Posts')
        with title_sort:
            if st.button('Sort by Title', 'title_sort', on_click=change_sort_order()):            
                query = REDDIT_POSTS.sort('post_title', st.session_state.sort_order)                   
                st.rerun()
        with date_sort:
            if st.button('Sort by Date', 'date_sort'):      
                query = REDDIT_POSTS.sort('post_timestamp')
        with blank_sort:
            if st.button('Sort by Category', 'cat_sort'):
                query = REDDIT_POSTS.sort('post_category')
        st.divider()
        
        counter = 0
        if REDDIT_POSTS.count_documents({}) > 0:
            st.write(f'REDDIT_POSTS.count_documents(): {REDDIT_POSTS.count_documents({})}')
            for post in load_cursor(REDDIT_POSTS, {}, 'post_title'):
                record_id = post["_id"]
                counter += 1
                title = post["post_title"]
                url = post["post_url"]
                author = post["post_author"]
                content = post["post_content"]
                img = post["post_img"]
                with st.container():
                    title_col, img_col, reply_col, del_col, edit_col = st.columns([2,2,1,1,1])                  
                    with reply_col: 
                        if st.button('Reply', 'reply' + str(counter)):
                            with st.form():
                                create_form(post_inputs, ':scroll:  Send Reply', 'replies', True)
                    with del_col:
                        if st.button('Delete', 'del' + str(counter)):
                            delete_record('posts', record_id)
                            st.toast(':sparkles:  Post deleted!  :white_check_mark:')                
                            st.rerun()
                            #st.error(':sparkles: Post deleted! :white_check_mark:')
                            #st.balloons()        
                    with edit_col:
                        if st.button('Edit', 'edit' + str(counter)):
                            edit_record('posts', record_id)
                            st.toast(':sparkles: Post updated! :white_check_mark:')                
                            st.rerun()
                            #st.balloons()                  
                    with title_col:
                        st.write(url)
                        st.write(title)
                        st.link_button(title, url)
                    with img_col:
                        if img:
                            #st.write(f'Image: {img}')
                            st.image(img, width=200)  
                    st.write(f'{content}')
                    st.write(f'By {author}')        
                st.divider()    
    else:
        st.write('No posts found, did you want to add one?')
        st.switch_page('pages/020_Add_Post.py')