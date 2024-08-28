
import streamlit as st
import pymongo
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import PyMongoError, BulkWriteError



PORT_STRING = st.secrets.mongo.port
PORT = int(PORT_STRING)

# Set up db connection
@st.cache_resource
def setup_conn(host, port):
    client = MongoClient(host, port)
    return client
    
CLIENT = setup_conn(HOST, PORT)

old_db = CLIENT.new_db_name
old_coll = old_db.new_collection_name

new_db = CLIENT.goals
new_coll = new_db.goals_list

st.write('Available databases:', CLIENT.list_database_names())

st.write('Colls in old_db:', old_db.list_collection_names())
st.write('old_coll:', old_coll)

st.write('Colls in new_db:', new_db.list_collection_names())
st.write('new_coll:', new_coll)

def transfer_data(old_coll, new_coll, overwrite=False):
    try:
        if overwrite:
            new_coll.delete_many({})
        
        documents = list(old_coll.find())
        if documents:
            result = new_coll.insert_many(documents)
            st.write(f"Inserted {len(result.inserted_ids)} documents.")
        else:
            st.write("No documents found in the old coll.")
    except BulkWriteError as bwe:
        st.write(f"Error during bulk write: {bwe.details}")
    except PyMongoError as e:
        st.write(f"An error occurred: {e}")

try:
    transfer_data(old_coll, new_coll) 
    # Check if new coll already has documents
    new_doc_count = new_coll.count_documents({})
    
    if new_doc_count > 0:
        st.write(f"The new coll '{new_coll}' already contains {new_doc_count} documents.")
        choice = input("Do you want to (a) overwrite existing data, (b) skip transfer, or (c) abort? (a/b/c): ").lower()
        
        if choice == 'a':
            transfer_data(old_coll, new_coll, overwrite=True)
        elif choice == 'b':
            st.write('Skipping data transfer.')
        else:
            st.write('Operation aborted.')
    else:
        transfer_data(old_coll, new_coll)

    # Verify transfer
    old_count = old_coll.count_documents({})
    new_count = new_coll.count_documents({})
    st.write(f'Old coll count: {old_count}')
    st.write(f'New coll count: {new_count}')

except PyMongoError as e:
    st.write(f'An error occurred: {e}')
