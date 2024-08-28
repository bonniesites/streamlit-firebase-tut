from mods.variables import *


# Set up db connection
@st.cache_resource
def setup_conn(host, port):
  # custom_print('inside mods.db.setup_conn()')
    client = MongoClient(host, port)
    return client



CLIENT = setup_conn(HOST, PORT)
#custom_print(f' CLIENT: {CLIENT}')

def custom_print(*args, **kwargs):
    # Get the caller's frame
    caller_frame = inspect.currentframe().f_back
    # Get the file name and line number
    file_name = os.path.basename(caller_frame.f_code.co_filename)
    line_number = caller_frame.f_lineno
    # Create the prefix with file name and line number
    prefix = f'[{file_name}, {line_number}]'
    # print the message with the prefix
    print(f" \n {prefix} : {' '.join(map(str, args))}")
    # Also display in Streamlit
    #st.text(f" \n {prefix}, {' '.join(map(str, args))}")

def edit_document_by_id(coll, document_id, new_data):
    try:
        # Attempt to update the document
        update_result = coll.update_one({"_id": document_id}, {"$set": new_data})        
        # Check if the update was successful
        if update_result.modified_count == 1:
            # Document updated successfully
            MSG_CONTAINER.empty()
            MSG_CONTAINER.success(f"Document with ID {document_id} updated successfully.")
            #st.rerun()  # Refresh the goal journal
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
            #st.rerun()       
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
    
def update_specific_string_many(coll, original, updated, field):
    update_result = coll.update_many({field: original}, {'$set':  {field: updated}})
    MSG_CONTAINER.success(f"Updated {update_result.modified_count} documents in the collection.")    
    #query['$text'] = {'$search': original} 
    query = {'$text': {'$search': original}}
    st.write(update_result)

# Function to list documents in a collection
def list_documents(db_name, coll_name):
    db = CLIENT[db_name]
    coll = db[coll_name]
    docs = coll.find()
    return doc

def sorted_records_list(coll, filter_query, srt_by, srt_ord):
    return list(coll.find(filter_query).sort([(srt_by, srt_ord)]))

#####

class Role(str, Enum):
    admin = 'Admin'
    user = 'User'
    guest = 'Guest'

class UserForm(BaseModel):
    name: str = Field(..., title="Name", description="Your full name")
    age: int = Field(..., title="Age", description="Your age in years")
    email: Optional[str] = Field(None, title="Email", description="Your email address")

class SearchForm(BaseModel):
    search_terms: str = Field(..., title="Search term", description='What are you searching for?')
    filter_choice: str = Field(..., title="Search term", description='What are you searching for?')


def build_form(schema: BaseModel):
    form_data = {}
    for field_name, field in schema.__fields__.items():
        field_type = field.type_
        field_info = field.field_info
        
        if field_type == str:
            form_data[field_name] = st.text_input(field_info.title or field_name, help=field_info.description)
        elif field_type == int:
            form_data[field_name] = st.number_input(field_info.title or field_name, min_value=0, help=field_info.description)
        elif field_type == float:
            form_data[field_name] = st.number_input(field_info.title or field_name, help=field_info.description)
        elif field_type == bool:
            form_data[field_name] = st.checkbox(field_info.title or field_name, help=field_info.description)
        else:
            st.warning(f"Field type {field_type} for {field_name} not supported")
    
    return schema(**form_data)

#####

def set_filter_query(filter_option, search_terms):
    # Add the filter option condition
    if filter_option == 'Done':
        query = {'is_done': True}
    elif filter_option == 'Pending':
        query = {'is_done': False}
    else:
        query = {}

    # Create a list of regex conditions for each search term
    search_conditions = []
    for term in search_terms:
        search_conditions.append({
            '$or': [
                {'category': {'$regex': term, '$options': 'i'}},
                {'subcategory': {'$regex': term, '$options': 'i'}},
                {'subsubcategory': {'$regex': term, '$options': 'i'}},
                {'goal_task': {'$regex': term, '$options': 'i'}},
            ]
        })

    # Add the search conditions to the query
    if search_conditions:
        if filter_option in ['Done', 'Pending']:
            query = {'$and': [query] + search_conditions}
        else:
            query = {'$and': search_conditions}
    # custom_print the query for debugging
  # custom_print(f"\nConstructed Query: {query}\n")
    
    return query

def build_search_box(form_data):
  # custom_print(f' \n st.session_state.filter_choice: {st.session_state.filter_choice}')
  # custom_print(f' \n st.session_state.search_terms: {st.session_state.search_terms}')  
  # custom_print(f' \n st.session_state.srt_by: {st.session_state.srt_by}')    
  # custom_print(f' \n st.session_state.srt_ord: {st.session_state.srt_ord}')
    with search_box:
        with st.form(form_data['form_key']):
            for i, (field_name, field_info) in enumerate(form_data['fields'].items()):
                unique_key = f"search_input_{i}"  # Generate a unique key for each input
                
                if field_info['type'] == 'text':
                    search_terms = st.text_input(label=field_info['label'], key=unique_key)
                elif field_info['type'] == 'selectbox':
                    filter_choice = st.selectbox(label=field_info['label'], options=field_info['options'], key=unique_key)
            
            submitted = st.form_submit_button(form_data['form_button_label'])
            if submitted:
                st.session_state.search_terms = search_terms 
                st.session_state.filter_choice = filter_choice
              # custom_print(f' \n st.session_state.filter_choice: {st.session_state.filter_choice}')
              # custom_print(f' \n st.session_state.search_terms: {st.session_state.search_terms}') 
              # custom_print(f' \n st.session_state.srt_by: {st.session_state.srt_by}')    
              # custom_print(f' \n st.session_state.srt_ord: {st.session_state.srt_ord}')
