# from mods.header import *
from mods.data_processing import *
# from mods.auth import *
from mods.utils import *
from mods.models import *

# Streamlit UI
st.title("MongoDB Explorer for Admins")
db_col, coll_col, doc_col = st.columns([1,1,1])
with db_col:
    # Dropdown menu for selecting a database
    db_choice = st.selectbox("Choose a database to explore:", CLIENT.list_database_names(), index=1)
with coll_col:
    if db_choice:
        DB = CLIENT[db_choice]
        # Dropdown menu for choosing a collection of the db
        coll_name = st.selectbox(f"Select a collection in '{db_choice}':", DB.list_collection_names(), index=1)
with doc_col:
    coll_choice = DB.coll_name
    if coll_choice is not None:
        query = {'name': 'Rex Barzee'}
        documents = coll_choice.find(query)
        custom_print(f'\n\n ')
        # Display documents in the selected collection
        st.write(f"Documents in collection: ")
        for document in list(documents):
            st.write(document)
            for key, value in document.items():
                st.write(f"- {key}: {value}")
            
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
