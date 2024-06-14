#######################
#  Utility Functions  #
#######################
import streamlit as st
from time import sleep

# Create an empty container at the top of the screen for messages
MSG_CONTAINER = st.empty()
SIDEBAR_MSG = st.sidebar.empty()
FORM_CONTAINER = st.sidebar.empty()

def close_popover():
    st.session_state.popover = False

def sxor(s1, s2):
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1, s2))

def select_signup():
    st.session_state.form = 'signup_form'

def user_update(name):
    st.session_state.username = name

def logout():        
    logout = st.sidebar.button(label='Log Out')
    if logout:
        user_update('')
        st.session_state.form = ''        

def get_files_in_folder(folder):
    files = []
    if os.path.exists(folder):
        files = os.listdir(folder)
    return files

def list_files_in_folder(folder):
    if folder:
        for file in folder:
            st.write(file)
    else:
        st.write(f"No files found.")
        
def search_in_file(file_path, search_term):
    try:
        with open(file_path, "r") as file:
            lines = file.readlines()
            lines_with_search_term = [line.strip() for line in lines if search_term.lower() in line.lower()]
        return lines_with_search_term
    except FileNotFoundError:
        return []
        
# Function to find close matches
def find_similar(search_term, data):
    # Get close matches; you can adjust the cutoff for similarity (0 to 1)
    matches = get_close_matches(search_term, data, n=5, cutoff=0.5)
    #st.write("Similar terms found:", matches)
    return matches

def read_file(file_path):# Open file(s)
    with open(file_path, 'r') as fp:
        # return all lines in a list
        return fp.readlines()    
    
def write_file(file_path, content):
    with open(file_path, 'w') as fp:
        fp.write(content)        
        return True    
    
def append_file(file_path, content):
    with open(file_path, 'a') as fp:
        fp.write(content)        
        return True    

def search_str(file_path, search_term, choice):
    # New function to check for a file with same name as search term and pull from there instead of searching again
    count = 1
    text_content = 'No instances found.'   
    file_name = f'pages/textfiles/{choice}-{search_term}.txt'

    lines = read_file(file_path)
    # Open text file in write mode, if we append, the results will always be added to the file, if it exists, for the same search term so the file will get huge!
    with open(file_name, 'w') as f_out:
        f_out.write(f'{search_term.upper} results:\n')        
        # check if string or similar exists in current line
        term_found_list = search_in_file(file_path, search_term)
        for line in term_found_list:
            st.write(f'{count} - {line}')
            f_out.write(f'{count} - {line}')
            count = count + 1
        if count != 0:
            f_out.write(f'\n{str(count)} results found')
            #f_out.write(f'{text_content}')               
    return file_name, count
    
def create_button(link, ltext):
    st.markdown(f'''
            <a 
            href="{link}" 
            style="
                border:1px solid chartreuse; 
                color: chartreuse; 
                border-radius:4px; 
                padding:.5rem;
                text-decoration:None;
                ">{ltext}</a>''', unsafe_allow_html=True)

# From https://github.com/dhanukaShamen/Image-Converter/blob/master/image_converter.py
def convert_folder_to_webp(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            st.write(file)
            # Only convert image files with extensions .png, .jpg, or .jpeg
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(root, file)
                st.write('image_path', image_path)
                output_folder = os.path.join(root, 'webp')
                st.write(output_folder)
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.webp')
                im = Image.open(image_path)
                st.write(output_path)
                st.write(f'im: {im}')
                if im.save(output_path, 'webp'):
                    st.success('Files converted successfully!')
                    st.write(f'im: {im}')

# Example usage
#convert_folder_to_webp(img_folder)

def convert_file_to_webp(file):
    # Only convert image files with extensions .png, .jpg, or .jpeg
    if file.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(root, file)
        st.write('image_path', image_path)
        output_folder = os.path.join(root, 'webp')
        st.write(output_folder)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.webp')
        im = Image.open(image_path)
        st.write(output_path)
        st.write(f'im: {im}')
        if im.save(output_path, 'webp'):
            st.success('Files converted successfully!')
            st.write(f'im: {im}')
    
    
# Adapted from https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-folder-in-streamlit-apps/
@st.cache_resource
def load_image(image_file):
    img = Image.open(image_file)
    return img

def process_img(uploaded, folder):
    file_details = {'FileName':uploaded.name,'FileType':uploaded.type}
    #st.write('file_details: ', file_details)
    img = load_image(uploaded)
    #st.write(f'img: {img}')
    st.image(img, width=50)
    file_path = os.path.join(UPLOAD_FOLDER,uploaded.name)
    #st.write(f'file_path: {file_path}')
    #st.write(f'img: {img}')
    # Create the upload folder if it doesn't exist
    if not os.path.exists(folder):
        os.makedirs(folder)
    # Define the file path
    file_path = os.path.join(folder, uploaded.name)
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploaded.getbuffer())
        path_exists = os.path.exists(file_path)
        #st.write(f'file_path: {file_path}')
        #st.write(f'path_exists: {path_exists}')
        if path_exists:
            st.success(f":tada:  Saved File:{uploaded.name} to folder")
            convert_folder_to_webp('img')                                

def create_form(inputs, prompt, form_name, upload, call_back):
    form_inputs = f'{form_name}_inputs'
    #st.write(f'form_inputs: {form_inputs}')
    if form_inputs not in st.session_state:
        st.session_state[form_inputs] = ''
    #form_name = ':female-technologist:' + form_name
    with st.container():
        st.subheader('Enter a new Post:')
        # Create a form using a for loop
        # TODO: Input sanitization and validation, required fields from mods import dbconnect
        with st.form(form_name):
            counter = 0
            for key, value in inputs.items():
                counter += 1
                if key == 'post_image':
                    # inputs.post_image = image
                    pass
                elif key == 'post_title':
                    document_title = key
                value_type = type(value)
                if value_type == int:
                    inputs[key] = st.slider(f'{value}:', 0, 100, 0)                    
                elif value_type == str:
                    inputs[key] = st.text_input(f'{value}:', key='text' + str(counter),)
                elif key == 'post_content':
                    inputs[key] = st.text_area(f'{value}:', key='text_area' + str(counter))
                # Add more conditions for other value types as needed
            submitted = st.form_submit_button(label=prompt, on_click=call_back)
            # Once the user has submitted, upload it to the database
            if submitted:
                st.write(inputs)
                # Display the submitted data
                if st.session_state[form_inputs] == '':                    
                    st.write(f'form_inputs: Blank, adding them now.')
                    st.session_state[form_inputs] = inputs     
                else:
                    st.write(f'form_inputs: {form_inputs}')            
                st.write(f'You entered the following information: {st.session_state[form_inputs]}')
                            
def save_record(inputs, form_name):
    #st.write(inputs)
    # TODO: set up authentication/login
    # TODO: sanitize and verify inputs
    # TODO: escape outputs(document_id)     
    #st.toast(':sparkles: Record saved! :white_check_mark:')
    #st.write(doc_ref)
    try:
        doc_ref = DB.collection(form_name).add(inputs)    
        document_id = doc_ref[-1].id
        st.write(f'document_id: {document_id}')
        new_doc = DB.collection(form_name).document            
        doc_ref.document(document_id).add({'entered' : datetime.datetime.now(tz=datetime.timezone.utc)})
        if form_name == 'posts':
            doc_ref.document(document_id).add({'img' : image_})          
        st.toast(':sparkles: Record saved! :white_check_mark:')
        st.balloons()
    except:
        st.toast(f':fire: Record not saved! :fire:')    
    # finally:        
    #     st.balloons()
    


# Define a function to toggle the sort order
def toggle_sort_order():
        st.session_state.sort_order *= -1
    
def delete_record(table, record_id):
    collection = DB[table]  # Access the collection using dictionary-style access
    collection.delete_one({'_id': record_id})
    # Reload the list
    st.experimental_rerun()   
    

def edit_record(table, record_id):    
    collection = DB[table]  # Access the collection using dictionary-style access
    pass


def find_similar_fuzzy(search_term, text, threshold=80):
    # Split the text into words
    words = text.split()
    
    # Use fuzzy matching to find words that are similar to the search term
    matches = process.extractBests(search_term, words, score_cutoff=threshold)
    
    return matches


def find_similar_fuzzy_in_file(search_term, file_path, threshold=80):
    # Read the file contents
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        # Split the text into words
        words = text.split()    
        # Use fuzzy matching to find words that are similar to the search term
        matches = process.extractBests(search_term, words, score_cutoff=threshold)    
        return matches


def check_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
        st.write(f"Created folder: {folder}")
        st.write("Full path to uploaded files:", os.path.abspath(folder))
        return True
    else:
        st.write("Folder already exists:", os.path.abspath(folder))
        return True
    #return os.path.abspath(folder)


def save_uploaded(uploadedfile, folder):
    try:
        if uploadedfile is not None:
            st.write("File name:", uploadedfile.name)
            # Create the upload folder if it doesn't exist
            check_folder(folder)
            # Save the file
            st.write(f"Saving file: {uploadedfile.name}, File size: {uploadedfile.size} bytes, File type: {uploadedfile.type}")
            file_path = os.path.join(folder, uploadedfile.name)
            if os.path.exists(file_path):
                # add a suffix to the filename
                base, extension = os.path.splitext(uploadedfile.name)
                counter = 1
                new_file_name = f"{base}_{counter}{extension}"
                new_file_path = os.path.join(folder, new_file_name)
                while os.path.exists(new_file_path):
                    counter += 1
                    new_file_name = f"{base}_{counter}{extension}"
                    file_path = os.path.join(folder, new_file_name)
                    st.write(f'new file_path: {new_file_path}')
                save_file(uploadedfile, new_file_path)
            else:
                save_file(uploadedfile, file_path)
            return True
    except Exception as e:
        st.error(f"Error saving file: {e}")
        return False

    
def save_file(uploadedfile, file_path):
    # Save the file
    with open(file_path, "wb") as f:
        f.write(uploadedfile.getbuffer())
    st.write(f"File saved to {file_path}")

def get_field_names(record):
    # Set to store unique field names
    fields = list(record.keys())
    print(fields)
    return(fields)
    
def display_message(text, display_time=.25):
    MSG_CONTAINER.warning(text)
    sleep(display_time)

# Function to fetch all records from MongoDB
def get_records(table, search_term):
    records = table.find({search_term})
    return list(records)

# Display records in Streamlit
def display_records(table, search_term):
    records = records = list(table.find({search_term}))
    # Display field names in the first row
    keys = records[0].keys()
    cols = st.columns(len(keys) + 2) # Extra columns for Edit/Delete buttons
    for i, key in enumerate(keys):
        cols[i].write(key.title())
    cols[-2].write("Edit")
    cols[-1].write("Delete")

    # Display each record
    for record in records:
        cols = st.columns(len(keys) + 2)
        for i, key in enumerate(keys):
            cols[i].write(record.get(key, ''))
        edit_button, delete_button = cols[-2].button("Edit", key=f"edit_{record['_id']}"), cols[-1].button("Delete", key=f"del_{record['_id']}")
        
        # Placeholder for edit functionality
        if edit_button:
            st.session_state['edit_id'] = str(record['_id'])
            # Redirect to an edit page or show edit form here
        
        # Handle delete (with confirmation)
        if delete_button:
            if st.confirm(f"Are you sure you want to delete record {record['_id']}?"):
                collection.delete_one({"_id": ObjectId(record['_id'])})
                st.experimental_rerun()


def view_all_records(table, title):
    st.divider()   
    query = f'{table}.find()'# .sort('post_timestamp')
    title, title_sort, date_sort, blank_sort = st.columns(4)
    with title:        
        st.header(title)
    with title_sort:
        if st.button('Sort by Title', 'title_sort', on_click=change_sort_order()):            
            query = f'{table}.find()'#.sort(f'{prefix}_title', SORT_ORDER)                   
            st.experimental_rerun()
    with date_sort:
        if st.button('Sort by Date', 'date_sort'):      
            query = f'{table}.find()'#.sort(f'{prefix}_timestamp')
        if st.button('Sort by Duedate', 'date_sort'):      
            query = f'{table}.find()'#.sort(f'{prefix}_duedate')
    with blank_sort:
        if st.button('Sort by Category', 'cat_sort'):
            query = f'{table}.find()'#.sort(f'{prefix}_category')
    st.divider()    
    counter = 0
    for record in f'{table}.find()':
        record_id = record["_id"]
        counter += 1
        with st.container():
            title_col, img_col, reply_col, del_col, edit_col = st.columns(len(fields))                  
            with reply_col: 
                if st.button('Reply', 'reply' + str(counter)):
                    with st.form():
                        create_form(record_inputs, ':scroll:  Send Reply', 'replies', True)
            with del_col:
                if st.button('Delete', 'del' + str(counter)):
                    delete_record(table, record_id)
                    st.toast(':sparkles:  Record deleted!  :white_check_mark:')                
                    st.experimental_rerun()
                    st.balloons()        
            with edit_col:
                if st.button('Edit', 'edit' + str(counter)):
                    edit_record(table, record_id)
                    st.toast(':sparkles: record updated! :white_check_mark:')                
                    st.experimental_rerun()
                    st.balloons()                  
            with title_col:
                st.link_button(title, url)
            with img_col:
                st.write(f'Image: {img}')
                st.image(img, width=150)  
            st.write(f'{content}')
            st.write(f'By {st.session}')        
        st.divider() 


def save_to_mongodb(table, data):
    collection = db[table]
    collection.insert_one(data)
    
    
def dynamic_form(form_inputs, table, form_name):
    pass

# def dynamic_form(form_inputs, table, form_name):
#     with st.form(form_name, clear_on_submit=False):
#         # Dynamically create form fields based on the form_inputs dictionary
#         user_inputs = {}
#         st.write(form_inputs.items())
#         for field, label in form_inputs.items():
#             # Customize this part for different types of inputs if necessary
#             # For example, you might use st.file_uploader for file fields
#             st.write(label, field)
#             #user_inputs[field] = st.text_input(label, key=field)
        
#         submitted = st.form_submit_button("Submit", type='primary')
#         if submitted:
#             # Filter out empty values if necessary
#             data_to_save = {field: value for field, value in user_inputs.items() if value}
#             save_to_mongodb(table, data_to_save)
#             st.success(":tada: Record saved!")
#             st.balloons()
            
# # Function to validate input based on the form definition
# def validate_input(input_value, min_length, max_length, regex_pattern):
#     if min_length is not None and len(input_value) < min_length:
#         return False
#     if max_length is not None and len(input_value) > max_length:
#         return False
#     if regex_pattern and not re.match(regex_pattern, input_value):
#         return False
#     return True

# # Initialize a dictionary to hold form responses
# form_responses = {}

# # Start a form
# with st.form("my_form"):
#     # Dynamically create form fields based on the structure
#     for field_key, field_info in goal_form_inputs.items():
#         field_type = field_info['type']
#         field_name = field_info['label']
        
#         if field_type == 'text':
#             input_value = st.text_input(field_name)
#         elif field_type == 'checkbox':
#             input_value = st.checkbox(field_name)
#         elif field_type == 'date':
#             input_value = st.date_input(field_name)
#         elif field_type == 'select':
#             input_value = st.selectbox(field_name)
#         # Add more field types as necessary
        
#         # Validate and collect input
#         if field_type in ['text', 'date']:  # Types that require validation
#             if validate_input(str(input_value), field_info.get('min_length'), field_info.get('max_length'), field_info.get('regex_pattern')):
#                 form_responses[field_key] = input_value
#             else:
#                 st.error(f"Validation failed for {field_name}")
#         else:
#             form_responses[field_key] = input_value
            
#     # Form submission
#     submitted = st.form_submit_button("Submit")
#     if submitted:
#         # Here you can add the logic to save form_responses to MongoDB
#         st.success("Form submitted successfully!")










      
        

# def save_uploaded_file(uploadedfile):
#     if uploadedfile is not None:
#         # Create the upload folder if it doesn't exist
#         if not os.path.exists(UPLOAD_FOLDER):
#             os.makedirs(UPLOAD_FOLDER)
#         # Define the file path
#         file_path = os.path.join(UPLOAD_FOLDER, uploadedfile.name)
#         # Save the file
#         with open(file_path, "wb") as f:
#             f.write(uploadedfile.getbuffer())
#         # Return the path or filename for storing in the database
#         return file_path  # or return uploadedfile.name if you only want the filename
#     return None
