from mods.base import *

# MongoDB connection
CLIENT = MongoClient("mongodb://mongodb:27017")

DB = CLIENT.reddit_clone
POSTS = DB.posts
USERS = DB.users
SORT_ORDER = 1


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


    
def change_sort_order():
    global SORT_ORDER    
    if SORT_ORDER == 1:
        SORT_ORDER = -1
    else:
        SORT_ORDER == 1
        

def search_str(file_path, search_term):
    # Open file(s)
    # TODO: check for a file with same name and pull from there instead of searching again
    with open(file_path, 'r') as fp:
        # read all lines in a list
        #st.write(search_term.upper(), 'results:\n')
        lines = fp.readlines()
        count = 0
        file_name = 'pages/textfiles/' + search_term + '.txt'
        # Open text file in write mode, we don't want to append, the results will always be the same for the same search term  
        
        left, right = st.columns(2)
        with left:
            count_box = st.empty()
        with right:
            download_box = st.empty()
        with open(file_name, 'w') as f_out:
            text_content = f'{search_term.upper} results:\n'
            for line in lines:
                # check if string present on a current line
                if search_term in line:
                    # f'{search_term} found!'
                    text_content += f'{line}\n'
                    f_out.write(f'{line}')
                    #st.write(f'(Line Number {lines.index(line)} {line}')
                    st.write(line)
                    #st.write('Book:', line)
                    #st.write(line)
                    count = count + 1
            f_out.write(f'{str(count)} results found')
        if count == 0:
            st.write('No instances found.')
        with left:
            with count_box:
                st.subheader(f'{str(count)} results found for {search_term}')
        with right:            
            with download_box:
                file_name = f'{search_term}.txt'
                st.download_button(
                    label="Download results", 
                    file_name=file_name, 
                    data=text_content,
                    mime='text/plain')
        return text_content, count

    
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
            # if upload:                
            #     uploaded = st.file_uploader('Upload your pic(s) here...', type=['png', 'jpeg', 'jpg'])
            #     image = process_img(uploaded)
            #     st.write(f'image: {image}')
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


def add_post(title, content, author, image, post_url):
    post = {
        "post_timestamp": datetime.utcnow(),
        "post_title": title, 
        "post_content": content, 
        "post_author": author,
        "post_img": image,
        "post_url": post_url
        }
    POSTS.insert_one(post)
    st.write(':tada: Post Added!')
    
from bson import ObjectId

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
        POSTS.update_one({'_id': ObjectId(record_id)}, {'$set': update_data})
        # Reload the list if using Streamlit
        st.experimental_rerun()


def view_posts():    
    query = POSTS.find()# .sort('post_timestamp')
    title, title_sort, date_sort, blank_sort = st.columns(4)
    with title:        
        st.header('Posts')
    with title_sort:
        if st.button('Sort by Title', 'title_sort', on_click=change_sort_order()):            
            query = POSTS.find().sort('post_title', SORT_ORDER)                   
            st.experimental_rerun()
    with date_sort:
        if st.button('Sort by Date', 'date_sort'):      
            query = POSTS.find().sort('post_timestamp')
    with blank_sort:
        if st.button('Sort by Category', 'cat_sort'):
            query = POSTS.find().sort('post_category')
    st.divider()
    
    counter = 0
    for post in POSTS.find():
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
                    st.experimental_rerun()
                    #st.error(':sparkles: Post deleted! :white_check_mark:')
                    #st.balloons()        
            with edit_col:
                if st.button('Edit', 'edit' + str(counter)):
                    edit_record('posts', record_id)
                    st.toast(':sparkles: Post updated! :white_check_mark:')                
                    st.experimental_rerun()
                    #st.balloons()                  
            with title_col:
                st.link_button(title, url)
            with img_col:
                #st.image(img, caption=img, width=200)
                file_path = f'{UPLOAD_FOLDER}/{img}'
                #st.write(f'File path: {file_path}')
                #st.write(f'Image: {img}')
                st.image(img, width=50)  
            st.write(f'{content}')
            st.write(f'By {author}')        
        st.divider() 

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
