from mods.header import *
from mods.data_processing import *
# from mods.auth import *
from mods.utils import *
from mods.models import *

from mods.admin import *

SIDEBAR = 'collapsed'

PAGE_HEADER = 'Reddit Clone App'
SITE_TITLE = f'My Multi App | {PAGE_HEADER}'
PAGE_SUBHEADER = 'Admin Utilities'

st.title(SITE_TITLE)
st.subheader(PAGE_SUBHEADER)

# Get the last modified time of the current file
file_path = __file__
last_modified_timestamp = os.path.getmtime(file_path)

# Convert the timestamp to a human-readable format
last_modified_date = datetime.datetime.fromtimestamp(last_modified_timestamp)

# Format the date to display only time and date without milliseconds
formatted_date = last_modified_date.strftime("%m/%d/%Y %I:%M:%S %p")

# Display the formatted last modified date
st.write(f'This file was last modified on: {formatted_date}')


# Sample data to search in
data = ["apple", "banana", "grape", "orange", "berry", "mango", "blueberry"]

st.title("Search for Similar Terms")

# User input for search term
search_term = st.text_input("Enter search term:")

# Function to find close matches
def find_similar(search_term, data):
    # Get close matches; you can adjust the cutoff for similarity (0 to 1)
    matches = get_close_matches(search_term, data, n=5, cutoff=0.5)
    return matches

if search_term:
    matches = find_similar(search_term, data)
    if matches:
        st.write("Similar terms found:", matches)
    else:
        st.write("No similar terms found.")


# Encode plaintext
plaintext = 'H'
print(plaintext)
key = 'b'
ciphertext = sxor(plaintext, key)
plaintext = ''
print(plaintext)


# Decode ciphertext
plaintext = sxor(ciphertext, key)

print(plaintext)
print(key)
print(ciphertext)

# Example usage for the 'post_form_inputs' model
# TODO: sync with pydantic
#dynamic_form(goal_form_inputs, 'goals', 'Goals Form')

# Call dynamic_form with different models and collection names as needed
# dynamic_form(user_form_inputs, "users")
# dynamic_form(cfv_form_inputs, "cfvs")
# dynamic_form(vendor_form_inputs, "vendors")
# dynamic_form(cost_form_inputs, "costs")


# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''  
# Check for logged in
if st.session_state.username != 'drushlopez':
    st.switch_page('pages/010_Login.py')

else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")    
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