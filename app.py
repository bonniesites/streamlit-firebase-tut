# From https://discuss.streamlit.io/t/streamlit-firestore/9224
# From https://blog.streamlit.io/streamlit-firestore/

import streamlit as st
from google.cloud import firestore

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("mods/firestore-key.json")

st.set_page_config(page_title="Firebase Reddit App Tutorial")

# Create a reference to the Google post.
doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())

st.header('Hello 🌎!')
if st.button('Balloons?'):
    st.balloons()