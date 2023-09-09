import streamlit as st
import os


# From https://github.com/dhanukaShamen/Image-Converter/blob/master/image_converter.py
def convert_folder_to_webp(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Only convert image files with extensions .png, .jpg, or .jpeg
                image_path = os.path.join(root, file)
                output_folder = os.path.join(root, 'webp')
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)
                output_path = os.path.join(output_folder, os.path.splitext(file)[0] + '.webp')
                im = Image.open(image_path)
                im.save(output_path, 'webp')

# Example usage
#convert_folder_to_webp(img_folder) 
 

# Adapted from https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
@st.cache_resource
def load_image(image_file):
    img = Image.open(image_file)
    return img

     
def process_img(uploaded):
    if uploaded is not None:
        file_details = {'FileName':uploaded.name,'FileType':uploaded.type}
        st.write(file_details)
        img = load_image(uploaded)
        st.image(img,height=250,width=250)
        with open(os.path.join('tempDir',uploaded.name),'wb') as f: 
            f.write(uploaded.getbuffer())         
        st.success(':tada:  Saved image!')
        convert_folder_to_webp('tempDir')
                        

def create_form(inputs, prompt, form_name):
    #form_name = ':female-technologist:' + form_name
    with st.expander(prompt):
        # Create a form using a for loop
        # TODO: Input sanitization and validation, required fieldsfrom mods import dbconnect
        with st.form(form_name):
            counter = 0
            for key, value in inputs.items():
                counter += 1
                if key == 'username':
                    document_title = key
                elif key == 'post_title':
                    document_title = key
                value_type = type(value)
                if value_type == int:
                    inputs[key] = st.slider(f'{value}', 0, 100, 0)                    
                elif value_type == str:
                    # https://rus19023.github.io/csa_game/
                    inputs[key] = st.text_input(f'{value}', 'text' + str(counter))
                elif key == 'post_content':
                    inputs[key] = st.text_area('text_area' + str(counter), f'{value}')
                # Add more conditions for other value types as needed
                
            uploaded = st.file_uploader('Upload your pic(s) here...', type=['png', 'jpeg', 'jpg'])

            process_img(uploaded)
            
            submitted = st.form_submit_button(prompt)
            # Once the user has submitted, upload it to the database
            if submitted:
                # Display the submitted data
                st.write('You entered the following information:', inputs)
                save_record(inputs, form_name)
                
            
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