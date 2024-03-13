import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta 


# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['goals']
GOALS = db['goals']

sidebar_form_container = st.sidebar.empty()

# Function to open sidebar when button is clicked
def open_sidebar_on_button_click(button_text):
    if st.button(button_text):        
        show_add_new_goal_form()


def show_add_new_goal_form():
    with sidebar_form_container.form(key='new_goal_form'):
        st.write('Add a new goal:')        
        timestamp = datetime.now()
        #st.write('timestamp: ', timestamp)   
        # Calculate tomorrow's date to use as default value for duedate 
        tomorrow = datetime.now() + timedelta(days=1)
        duedate = st.date_input('Due Date', value=tomorrow)                
        #st.write('duedate: ', duedate)
        duedatetime = datetime.combine(duedate, datetime.min.time())              
        #st.write('duedatetime: ', duedatetime) 
        # Ensure both timestamp and duedatetime are datetime objects
        # assert isinstance(timestamp, datetime), "timestamp is not a datetime.datetime object"
        # assert isinstance(duedatetime, datetime), "duedatetime is not a datetime.datetime object"
     
        category = st.text_input('Category')
        goal = st.text_input('Goal Task')        

        goal_data = { 'timestamp' : timestamp, 'category' : category, 'goal' : goal, 'duedate' : duedatetime, 'is_done' : False }        
        save_goal_button = st.form_submit_button(label='Save Goal')
        
        if save_goal_button:
            # Save the new goal to the database
            try:
                message_container.warning('Invoked save goal button')
                result = add_new_document(goal_data)
                
                # saved_id = GOALS.insert_one(test_data)
                #st.write('saved_id: ', saved_id)
                if result:                            
                    message_container.success("Document inserted successfully with id:", result.inserted_id)
                    return True
                else:                            
                    message_container.warning("Failed to insert document.")
                    return False
            except Exception as e:
                message_container.warning("Error occurred while inserting document:", e)
                return False
            #st.experimental_rerun()  # Rerun the app to reflect changes

# documents = list(GOALS.find())
# # Display the documents in a Streamlit component
# if documents:
#     st.write("List of Documents:")
#     for doc in documents:
#         st.write(doc)
# else:
#     st.write("No documents found in the collection.")
    
# GOALS.delete_many({})
#duedatetime1 = datetime.combine(duedate1, datetime.min.time())
# Check for datetime instance
#assert isinstance(duedatetime1, datetime), "duedatetime is not a datetime.datetime object"


st.title('SMART Goals Journal App')
# Create a button that opens the add goal form when clicked
open_sidebar_on_button_click("Add a new goal")

# Create an empty container at the top of the screen
message_container = st.empty()

# duedate1 = datetime.now() + timedelta(days=1)        
# test_data = {'timestamp' : datetime.now(), 'category' : 'goals', 'goal' : 'add db', 'duedate' : duedate1, 'is_done' : False}
# saved_id = GOALS.insert_one(test_data)
#st.write('saved_id: ', saved_id)


def add_new_document(collection, data):
    saved_id = collection.insert_one(data)
    message_container.success('saved_id: ', saved_id)
    return saved_id

    
def delete_all_documents(collection):
    result = collection.delete_many({})
    # Update the content of the container with your message
    message_container.success(f"Deleted {result.deleted_count} documents from the collection.")
    
    
def delete_document_by_id(collection, document_id):
    result = collection.delete_one({"_id": document_id})
    if result.deleted_count == 1:        
        message_container.success(f"Document with ID {document_id} deleted successfully.")
    else:        
        message_container.warning(f"No document found with ID {document_id}.")
        
            
def edit_document(document_id):
    # Fetch the document to edit
    document = GOALS.find_one({"_id": document_id})
    with sidebar_form_container:
        # Display the document data in an editable form
        new_data = {}
        for field, value in document.items():
            if field != "_id":
                if isinstance(value, bool):
                    new_data[field] = st.checkbox(field, value)
                elif isinstance(value, str):
                    new_data[field] = st.text_input(field, value)
                elif isinstance(value, int):
                    new_data[field] = st.number_input(field, value=value)
                elif isinstance(value, float):
                    new_data[field] = st.number_input(field, value=value)
                elif isinstance(value, list):
                    new_data[field] = st.multiselect(field, value)
                elif isinstance(value, dict):
                    message_container.warning(f"Skipping field '{field}' of type 'dict'.")
                else:
                    message_container.warning(f"Skipping field '{field}' of unknown type.")

        # Update the document in the collection
        if st.button("Save Changes"):
            update_query = {"_id": document_id}
            update_operation = {"$set": new_data}
            GOALS.update_one(update_query, update_operation)
            message_container.success("Document updated successfully.")
        
def mark_as_done(collection, document_id):
    # Update the document where _id matches the provided document_id
    result = collection.update_one(
        {"_id": document_id},
        {"$set": {"is_done": True}}
    )    
    if result.modified_count == 1:
        message_container.warning(f"Document with ID {document_id} marked as done.")
    else:
        message_container.warning(f"No document found with ID {document_id}.")

    
# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())


def render_goal(goal):
    # Create separate columns for each field and button
    col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])

    # Add buttons for editing, deleting, and marking as done
    with col_markdone:
        if st.button(":white_check_mark:", key=f"mark_as_done_button_{goal['_id']}"):
            # Implement mark as done functionality
            mark_as_done(collection, goal['_id'])
    with col_edit:
        if st.button(":pencil2:", key=f"edit_button_{goal['_id']}"):
            # Implement edit functionality
            st.write("Edit Goal")
            edit_document(goal['_id'])        
    with col_delgoal:
        if st.button(":wastebasket:", key=f"delete_button_{goal['_id']}"):
            # Implement delete functionality
            delete_document_by_id(GOALS, goal['_id'])
    
    # Display goal information in separate columns
    with col_cat:
        st.write(goal['category'])
    with col_goal:
        st.write(goal['goal'])
    with col_due:
        st.write(goal['duedate'].date())
    with col_timestamp:
        st.write(goal['timestamp'].date())


# Main function
def main():        
    # Implement search functionality
    with st.sidebar:
        # # Emergency button to delete all goals, for debugging only
        # if st.button("Delete All Documents"):
        #     delete_all_documents(GOALS)
        search_term = st.text_input("Search goals")
        # Create a button that clears search form when clicked
        open_sidebar_on_button_click("Clear")
         # Query MongoDB for unique values of the "category" field
        # Query MongoDB for unique values of the "category" field
        categories = GOALS.distinct("category")
        # Add "All" option to the list of categories
        categories.insert(0, "All")

        # Display filter buttons with checkboxes for categories
        selected_categories = []
        st.text_input("Filter by Category")
        for category in categories:
            selected = st.sidebar.checkbox(category, key=category)
            if selected:
                selected_categories.append(category)
        # If "All" is selected or no category is selected, use all categories
        if "All" in selected_categories or not selected_categories:
            selected_categories = categories
        duedate_filter = st.date_input("Filter by Due Date", value=None)
        duedate_filter = date_to_datetime(duedate_filter)        
        timestamp_filter = st.date_input("Filter by Timestamp", value=None)
        timestamp_filter = date_to_datetime(timestamp_filter)
        # Display sort buttons in one line
        col1, col2 = st.columns(2)
        with col1:
            sort_by = st.selectbox("Sort by", ["Category", "goal", "Due Date", "Date Entered"])
        with col2:
            sort_order = st.radio("Sort Order", ["Ascending", "Descending"], horizontal=True)
    
    st.subheader('My SMART Goals Journal')
    # Fetch goals based on filters, search, and sort criteria
    filter_query = {}

    # Apply filters
    if selected_categories and "All" not in selected_categories:
        filter_query["category"] = {"$in": selected_categories}
    if duedate_filter:
        filter_query["duedate"] = {"$eq": duedate_filter}
    if timestamp_filter:
        filter_query["timestamp"] = {"$eq": timestamp_filter}
    
        
    # Create a text index on the 'goal' field, only need to execute once (supposedly)
    # GOALS.create_index([('goal', 'text')])
        
    # Apply search
    if search_term:
        filter_query["$text"] = {"$search": search_term}
    # st.write('filter_query: ', filter_query)
    # Fetch goals from MongoDB based on the filter query
    fields = {'_id': 1, 'category':1, 'goal': 1, 'is_done': 1, 'timestamp': 1, 'duedate': 1}
    filtered_goals = GOALS.find(filter_query, fields)
    # filtered_goals

    # Apply sorting
    if sort_by == "Category":
        sort_field = "category"
    elif sort_by == "goal":
        sort_field = "goal"
    elif sort_by == "Due Date":
        sort_field = "duedate"
    elif sort_by == "Date Entered":
        sort_field = "timestamp"
        
    sort_field = sort_by.lower().replace(" ", "_") 

    sort_direction = -1 if sort_order == "Descending" else 1

    # Sort goals based on the selected field and direction
    goal_list = filtered_goals.sort(sort_field, sort_direction)
    #goal_list
    
    # # Convert MongoDB cursor to list of dictionaries
    goal_list = list(goal_list)
    # goal_list

    # # Display the data table
    # if len(goal_list) > 0:
    #     st.dataframe(goal_list)  # Display the data table
    # else:
    #     st.write("No goals found in database.")

    col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])
    with col_markdone:
        'Done'
    with col_edit:
        'Edit'
    with col_delgoal:
        'Trash'
    with col_cat:
        'Category'
    with col_goal:
        'Goal Text'
    with col_due:
        'Due Date'
    with col_timestamp:
        'Set Date'   
    for goal in goal_list:
        render_goal(goal)

if __name__ == "__main__":
    main()
