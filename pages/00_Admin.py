from mods.base import *

SIDEBAR = 'collapsed'

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Admin Utilities'

st.title(SITE_TITLE)
st.divider()      
st.subheader(PAGE_SUBHEADER)
    

uploaded_file = st.file_uploader("Choose an image file to upload", type=["jpg", "jpeg", "png", "webp"])
if uploaded_file is not None:
    save_uploaded(uploaded_file, UPLOAD_FOLDER)

# List uploaded files
st.divider()
st.subheader('Uploaded Files')
list_files_in_folder(get_files_in_folder(UPLOAD_FOLDER))

# # from picoCFT - "Bases"
# import base64

# encoded_str = "bDNhcm5fdGgzX3IwcDM1"
# decoded_bytes = base64.b64decode(encoded_str)
# decoded_str = decoded_bytes.decode('utf-8')  

# # Assuming the original content is a UTF-8 string

# st.write()
# st.write('picoCTF{' + decoded_str + '}')
# st.write()
