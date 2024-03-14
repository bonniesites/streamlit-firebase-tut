import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timedelta 
from streamlit_extras.stylable_container import stylable_container
from time import sleep

# Connect to MongoDB
client = MongoClient('mongodb://mongodb:27017/')
db = client['goals']
GOALS = db['goals']
COUNT = 0

# # Define custom CSS style for the buttons
# button_style = """
#     <style>
#         div.stButton > button:first-child {
#             color: hotpink;
#             border-color: hotpink;
#             border-width: 2px;
#         }
#         div.stButton > button:first-child:hover {
#             color: pink;  
#             border-color: pink;  
#         }
#     </style>
# """
# # Display custom buttons
# st.markdown(button_style, unsafe_allow_html=True)

# Initialize session states
if 'selected_categories' not in st.session_state:
    st.session_state.selected_categories = []    

st.title('SMART Goals Journal App')

# Create an empty container at the top of the screen
message_container = st.empty()
sidebar_msg = st.sidebar.empty()
addgoal_form_container = st.sidebar.empty()
editgoal_form_container = st.sidebar.empty()

# Function to open sidebar when button is clicked
def open_sidebar_on_button_click(button_text, help_text):
    with stylable_container(key="unique", css_styles="""
    { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
    """):
        #COUNT += 1
        #count_str = str(COUNT)
        if st.button(button_text, key="custom_button" + button_text + '_', help=help_text):        
            show_add_new_goal_form()


def show_add_new_goal_form():
    with addgoal_form_container.form(key='new_goal_form'):
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
        save_goal_button = st.form_submit_button(label='Save Goal',help="Save the new goal")
        goal_data        
        if save_goal_button:
            # Save the new goal to the database
            try:
                message_container.warning('Invoked save goal button')
                sleep(3)
                result = add_new_document(goal_data)
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

    
# Convert date to datetime object
def date_to_datetime(date):
    if date is None:
        return None
    return datetime.combine(date, datetime.min.time())


# Create a button that opens the add goal form when clicked
open_sidebar_on_button_click("Add a new goal", "Add a new goal")
    
test_data = [
    [ 'goals', 'fix update not working']
    ,
    [ 'goals', 'add scratchout for done goals' ]
    ,
    [ 'goals', 'add undo button if done' ]
    ,
    [ 'calls', 'fred appt' ]
    ,
    [ 'calls', 'schedule surgery' ]
    ,
    [ 'calls', 'dentist appt me' ]
    ,
    [ 'calls', 'dentist appt charlie' ]
    ,
    [ 'goals', 'fix save goal button not working' ]
    ,
    [ 'goals', 'change button style' ]
    ,
    [ 'goals', 'default' ]
    ,
    [ 'goals', 'default' ]
    ,
    [ 'goals', 'default' ]
    ,
    [ 'goals', 'default' ]
    ,
    [ 'cat', 'default' ]
    ,
    [ 'cat', 'default' ]
    ,
    [ 'cat', 'default' ]
    ,
    [ 'cat', 'default' ]
    ]
# for info in test_data:
#     newgoal = {'timestamp' : datetime.now(), 'category' : info[0], 'goal' : info[1], 'duedate' : date_to_datetime(datetime.now().date() + timedelta(days=1)) , 'is_done' : False }
#     saved_id = GOALS.insert_one(newgoal)
#     message_container.success(f'saved_id: {saved_id}')


def add_new_document(collection, data):
    saved_id = collection.insert_one(data)
    message_container.success(f'saved_id: {saved_id}')
    return saved_id

    
def delete_all_documents(collection):
    result = collection.delete_many({})
    # Update the content of the container with your message
    message_container.success(f"Deleted {result.deleted_count} documents from the collection.")
    st.experimental_rerun()  # Rerun the app to reflect changes
    
    
def delete_document_by_id(collection, document_id):
    result = collection.delete_one({"_id": document_id})
    if result.deleted_count == 1:        
        message_container.success(f"Document with ID {document_id} deleted successfully.")
    else:        
        message_container.warning(f"No document found with ID {document_id}.")
        
            
def edit_document(document_id):                    
    sidebar_msg.warning('edit_document function invoked!')
    sleep(3)
    # Fetch the document to edit
    document = GOALS.find_one({"_id": document_id})
    sidebar_msg.warning(document)
    sleep(3)
    with addgoal_form_container:
        # Display the document data in an editable form
        update_data = {}
        placeholders = {}  # Placeholder dictionary to store st.empty() objects
        with st.form(key="edit_form"):
            for field, value in document.items():
                if field != "_id":
                    sidebar_msg.warning(f'field: {field}')
                    sleep(3)
                    if isinstance(value, bool):
                        update_data[field] = st.checkbox(field, value)
                    elif isinstance(value, str):
                        update_data[field] = st.text_input(field, value)
                    elif isinstance(value, int):
                        update_data[field] = st.number_input(field, value=value)
                    elif isinstance(value, float):
                        update_data[field] = st.number_input(field, value=value)
                    elif isinstance(value, list):
                        update_data[field] = st.multiselect(field, value)
                    elif isinstance(value, dict):
                        sidebar_msg.warning(f"Skipping field '{field}' of type 'dict'.")
                        sleep(3)
                    else:
                        sidebar_msg.warning(f"Skipping field '{field}' of unknown type.")
                        sleep(3)
                        
            with stylable_container(key="unique-edit", css_styles="""
                { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
                """):
                # Update the document in the collection
                if st.form_submit_button(label='Save Changes', help="Save the edits you made"):               
                    sidebar_msg.warning(update_data)
                    sleep(3)
                    update_query = {"_id": document_id}
                    update_operation = {"$set": update_data}
                    GOALS.update_one(update_query, update_operation)
                    sidebar_msg.success("Document updated successfully.")
                    sleep(3)

        
def toggle_mark_as_done(collection, document_id):
    # Retrieve the current document
    current_document = collection.find_one({"_id": document_id})
    if current_document:
        # Toggle the value of the "is_done" field
        new_value = not current_document.get("is_done", False)
        # Update the document in the collection
        collection.update_one({"_id": document_id}, {"$set": {"is_done": new_value}})
        return new_value  # Return the new value of "is_done"
    else:
        return None  # Document not found


# Define a function to format the goal text based on is_done value
def format_goal_text(goal):
    if goal['is_done']:
        return f"<del>{goal['goal']}</del>"
    else:
        return goal['goal']


def render_goal(goal):
    # Create separate columns for each field and button
    col_markdone, col_edit, col_delgoal, col_cat, col_goal, col_due, col_timestamp = st.columns([1, 1, 1, 2, 3, 2, 2])

    # Add buttons for editing, deleting, and marking as done
    with col_markdone:
        if goal['is_done']:
            icon = ":repeat_one:"
            help_text = "Undo goal achievement"
        else:
            icon = ":white_check_mark:"
            help_text = "Mark the goal as achieved"
        with stylable_container(key="unique-done", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):    
            if st.button(icon, key=f"mark_done_{goal['_id']}", help=help_text, use_container_width=True):
                # Toggle mark as done
                toggle_mark_as_done(GOALS, goal['_id'])
                st.experimental_rerun()  # Rerun the app to reflect changes
    with col_edit:
        with stylable_container(key="unique-edit", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):
            if st.button(":pencil2:", key=f"edit_{goal['_id']}", help="Edit the goal", use_container_width=True):                    
                sidebar_msg.warning('edit_document button invoked!')
                sleep(3)
                # Implement edit functionality
                st.write("Edit Goal")
                edit_document(goal['_id'])
                st.experimental_rerun()  # Rerun the app to reflect changes        
    with col_delgoal:
        with stylable_container(key="unique-delete", css_styles="""
            { [data-testid="baseButton-secondary"] { color: prussian; border-color: prussian; border-width: 2px; } }
            """):
            if st.button(":wastebasket:", key=f"delete_{goal['_id']}", help="Delete the goal", use_container_width=True):
                # Implement delete functionality
                delete_document_by_id(GOALS, goal['_id'])
                st.experimental_rerun()  # Rerun the app to reflect changes
    # Display goal information in separate columns
    with col_cat:
        st.write(goal['category'])
    with col_goal:         
        # Use the function to format the goal text
        formatted_goal_text = format_goal_text(goal)# Display the formatted goal text using st.markdown
        st.markdown(formatted_goal_text, unsafe_allow_html=True) 
        #st.write(formatted_goal_text)
    with col_due:
        st.write(str(goal['duedate'].date()))
    with col_timestamp:
        st.write(str(goal['timestamp'].date()))


# Main function
def main():        
    # Implement search functionality
    with st.sidebar:
        # # Emergency button to delete all goals, for debugging only
        with stylable_container(key="unique-delete-all", css_styles="""
            { [data-testid="baseButton-secondary"] { color: hotpink; border-color: hotpink; border-width: 2px; } }
            """):
            if st.button("Delete All Documents", key="delete_all_docs"):
                delete_all_documents(GOALS)
            
        search_term = st.text_input("Search goals")
        # Create a button that clears search form when clicked
        open_sidebar_on_button_click("Clear", "Clear the search box")
         # Query MongoDB for unique values of the "category" field
        # Query MongoDB for unique values of the "category" field
        categories = GOALS.distinct("category")
        # Add "All" option to the list of categories
        categories.insert(0, "All")

        # Display filter dropdown for categories
        selected_categories = []
        st.write("Filter by Category")
        for category in categories:
            selected = st.selectbox(category, key=category, options=categories)
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
            sort_by = st.selectbox("Sort by", ["Category", "Goal task", "Due Date", "Date Entered"])
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
    elif sort_by == "Goal Task":
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
        ''
    with col_edit:
        ''
    with col_delgoal:
        ''
    with col_cat:
        'Category'
    with col_goal:
        'Goal Task'
    with col_due:
        'Due Date'
    with col_timestamp:
        'Set Date'   
    for goal in goal_list:
        render_goal(goal)

if __name__ == "__main__":
    main()
