# From https://discuss.streamlit.io/t/streamlit-firestore/9224
# From https://blog.streamlit.io/streamlit-firestore/

import streamlit as st
from google.cloud import firestore
import os

# Authenticate to Firestore with the JSON account key.
db = firestore.Client.from_service_account_json("mods/firestore-key.json")

st.set_page_config(page_title="My Reddit App ")

# # Create a reference to the Google post.
# doc_ref = db.collection("posts").document("Google")

# # Then get the data at that reference.
# doc = doc_ref.get()

# # Let's see what we got!
# st.write("The id is: ", doc.id)
# st.write("The contents are: ", doc.to_dict())

# # This time, we're creating a NEW post reference for Apple
# doc_ref = db.collection("posts").document("Apple")

# And then uploading some data to that reference
# doc_ref.set({
# 	"title": "Apple",
# 	"url": "www.apple.com"
# })

# # Now let's make a reference to ALL of the posts
# posts_ref = db.collection("posts")

# # For a reference to a collection, we use .stream() instead of .get()
# for doc in posts_ref.stream():
# 	st.write("The id is: ", doc.id)
# 	st.write("The contents are: ", doc.to_dict())
 
# Streamlit widgets to let a user create a new post
title = st.text_input("Post title")
url = st.text_input("Post url")
submit = st.button("Submit new post", ":female-technologist:")

# Once the user has submitted, upload it to the database
if title and url and submit:
    try:
        doc_ref = db.collection("posts").document(title)
        doc_ref.set({
            "title": title,
            "url": url
        })        
        st.error("Post saved!", "")
    except:
        st.error("That didn't work! Sorry about that!", "🔥")
    
    finally:        
        st.balloons()
    
# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
for doc in posts_ref.stream():
	post = doc.to_dict()
	title = post["title"]
	url = post["url"]

	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")

# st.header('Hello 🌎!')
# if st.button('Balloons?'):
#     st.balloons()