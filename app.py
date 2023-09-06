# From https://discuss.streamlit.io/t/streamlit-firestore/9224
# From https://blog.streamlit.io/streamlit-firestore/

import streamlit as st
import mods.base
from mods.dbconnect import db

st.title('I Read It!')

def create_form(inputs, prompt, form_name):
    #form_name = ":female-technologist:" + form_name
    with st.expander(prompt):
        # Create a form using a for loop
        # TODO: Input sanitization and validation, required fields
        fields = {}
        for key, value in inputs.items():
            print('key:', key)
            if key == 'username':
                document_title = key
            elif key == 'post_title':
                document_title = key
            value_type = type(value)
            if value_type == int:
                inputs[key] = st.slider(f'{value}', 0, 100, 0)
            elif value_type == str:
                inputs[key] = st.text_input(f'{value}', '')
            # Add more conditions for other value types as needed
        
        submit = st.button(prompt, form_name)
        # Once the user has submitted, upload it to the database
        
        if submit:
            # Display the submitted data
            st.write('You entered the following information:')
            st.write(inputs)
            #TODO: SET AND GET USERNAME TO AND FROM SESSION
            try:
                # Get document title from which fields/keys?
                #document_title = 
                if login_username:
                    pass
                doc_ref = db.collection(form_name).document()
                # TODO: if title and url not found
                for input in inputs:
                    doc_ref.add({input[key] : input[value]}) 
                    doc_ref.add({'entered' : datetime.datetime.now(tz=datetime.timezone.utc)})        
                st.balloons()       
                st.error("Post saved!", "")
            except:
                st.error("That didn't work! Sorry about that!", "🔥")    
            # finally:        
            #     st.balloons()

with st.sidebar:
    login_inputs = {
        'login_username': 'Username or email',
        'password': 'Password'
    }
    
    post_inputs = {
        'post_title': 'Post title:',
        'post_content': 'Post content:',
        'post_url': 'Link URL:',
        'post_author': 'username-from-login-session'
    }
    
    user_inputs = {
        'username': 'Username',
        'first': 'First name',
        'last': 'Last name',
        'email': 'Email',
        'street_address': 'Street address',
        'postal_code': 'Postal/zip code',
        'phone': 'Phone number',
        'month': 'Birthday month',
        'day': 'Birthday day'
        }    
    
    create_form(login_inputs, 'Log in', 'logins')    
    st.divider()
        
    create_form(post_inputs, ':scroll: Add a Post:', 'posts')    
    st.divider()
        
    create_form(user_inputs, 'Add a user', 'users')
    
        
    

# Then query to list all users
users_ref = db.collection('users')
users = users_ref.stream()

for user in users:
    print('{} => {}'.format(user.id, user.to_dict()))
    
# And then render each post, using some light Markdown
posts_ref = db.collection("posts")
posts = posts_ref.stream()

for post in posts:
	post = post.to_dict()
	title = post["post_title"] 
	url = post["post_url"]
	author = post["post_author"]  
	content = post["post_content"]
	st.subheader(f"Post: {title}")
	st.write(f":link: [{url}]({url})")
	st.write(content, f'&nbsp;&nbsp;Author: {author}')
 
 
 

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

# st.header('Hello 🌎!')
# if st.button('Balloons?'):
#     st.balloons()