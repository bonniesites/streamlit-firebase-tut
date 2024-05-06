from mods.header import *
from mods.data_processing import *
# from mods.auth import *
from mods.utils import *
from mods.models import *

# Streamlit UI
st.title("DB Admin: MongoDB Explorer")
db_col, coll_col, doc_col = st.columns([1,1,1])
with db_col:
    db_choice = st.selectbox("Choose a database to explore:", CLIENT.list_database_names(), index=1)
if db_choice:
    DB = CLIENT[db_choice]
    with coll_col:
        if DB.list_collection_names():  # Check if there are any collections
            coll_name = st.selectbox(f"Select a collection in '{db_choice}':", DB.list_collection_names(), index=0)
        else:
            st.write("No collections found in this database.")
    if 'coll_name' in locals() and coll_name:
        with doc_col:
            # Correctly access the collection using its name
            coll_choice = DB[coll_name]
            query = {}
            documents = coll_choice.find(query)
            documents_count = coll_choice.count_documents(query)
            # Display documents in the selected collection
            doc_list = list(documents)  # Convert cursor to list
            if doc_list:
                st.write(f"{documents_count} Documents in collection '{coll_choice}':")
                for document in doc_list:
                    st.json(document)  # Using st.json for better formatting
            else:
                st.write("No documents found with the given query.")
            
filter = st.text_input('Replace this:')
update = st.text_input('With this:')
if st.button('Bulk String Replace (every instance in each document in the collection)'):
    update_specific_string_many(coll_choice, filter, update)

# # Function to list databases
# def list_databases():
#     databases = CONN.list_database_names()
#     st.write("Databases:")
#     for db in databases:
#         st.write(f"- {db}")

# # Function to list collections in a database
# def list_collections(database_name):
#     db = CONN[database_name]
#     collections = db.list_collection_names()
#     st.write(f"Collections in '{database_name}':")
#     for collection in collections:
#         st.write(f"- {collection}")

# # Function to list documents in a collection
# def list_documents(database_name, collection_name):
#     db = CONN[database_name]
#     collection = db[collection_name]
#     documents = collection.find()
#     st.write(f"Documents in '{collection_name}':")
#     for document in documents:
#         st.write(document)

# # Streamlit UI
# st.title("MongoDB Explorer")

# # List databases
# list_databases()

# # Select a database
# db_choice = st.selectbox("Select a database:", CONN.list_database_names())

# if db_choice:
#     # List collections in the selected database
#     list_collections(db_choice)

#     # Select a collection
#     selected_collection = st.selectbox(f"Select a collection in '{db_choice}':",
#                                        CONN[db_choice].list_collection_names())

#     if selected_collection:
#         # List documents in the selected collection
#         list_documents(db_choice, selected_collection)
