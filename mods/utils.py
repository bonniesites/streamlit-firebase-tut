from mods.base import *

    
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
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Only convert image files with extensions .png, .jpg, or .jpeg
                image_path = os.path.join(root, file)
                st.write(image_path)
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

# Adapted from https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
@st.cache_resource
def load_image(image_file):
    img = Image.open(image_file)
    return img


def save_uploadedfile(uploadedfile):
     with open(os.path.join("images",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to images".format(uploadedfile.name))
      

def process_img(uploaded):
    if uploaded is not None:
        file_details = {'FileName':uploaded.name,'FileType':uploaded.type}
        st.write(file_details)
        folder = 'images'
        img = load_image(uploaded)
        st.write(f'img: {img}')
        st.image(img, width=250)
        file_path = os.path.join('images',uploaded.name)
        st.write(f'img: {img}')
        path_exists = os.path.exists(file_path)
        st.write(f'path_exists: {path_exists}')
        if path_exists(file_path):
            save_uploadedfile(uploaded)        
        st.success(':tada:  Saved image!')
        convert_folder_to_webp('images')
                                

def create_form(inputs, prompt, form_name, upload, call_back):
    form_inputs = f'{form_name}_inputs'
    st.write(f'form_inputs: {form_inputs}')
    if form_inputs not in st.session_state:
        st.session_state[form_inputs] = ''
    #form_name = ':female-technologist:' + form_name
    with st.container():
        st.subheader('Enter a new Post:')
        if upload:                
            uploaded = st.file_uploader('Upload your pic(s) here...', type=['png', 'jpeg', 'jpg'])
            image = process_img(uploaded)
            st.write(f'image: {image}')
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
        doc_ref = db.collection(form_name).add(inputs)    
        document_id = doc_ref[-1].id
        st.write(f'document_id: {document_id}')
        new_doc = db.collection(form_name).document            
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
    db.collection(table).document(record_id).delete()
    

def edit_record(table, record_id):
    pass