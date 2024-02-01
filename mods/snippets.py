with st.expander('Add a user:'):
        # Streamlit widgets to let a user create a new post
        username = st.text_input("User name")
        firstname = st.text_input("First name")
        lastname = st.text_input("Last name")
        streetaddress = st.text_input("Street address")
        postalcode = st.text_input("Postal code/Zip code")
        email = st.text_input("Email")
        phone = st.text_input("Phone number")
        submit = st.button("Submit User", 'user')
        
        # Add a new user to the database
        #db = firestore.Client()
        doc_ref = db.collection('users').document('alovelace')
        doc_ref.set({
            'username': 'aluvlace',
            'first': 'Ada',
            'last': 'Lovelace',
            'month': 'April',
            'day': 17
        })

        # Once the post has submitted, upload it to the database
        if username and firstname and lastname and email and phone and streetaddress and postalcode and submit:
            try:
                # TODO: if username and first and last and phone and email not found
                doc_ref = db.collection("users").document(username)
                doc_ref.set({
                    "title": title,
                    "url": url,
                    "content": content
                })         
                st.balloons()       
                st.error("Post saved!", "")
            except:
                st.error("That didn't work! Sorry about that!", "🔥")    
            # finally:        
            #     st.balloons()
        
        
with st.expander('Process a marriages image:'):
        # TODO: get username from session
        #username = st.text_input("User name")
        firstname = st.text_input("First name")
        lastname = st.text_input("Last name")
        birthplace = st.text_input("Birth place")
        birthyear = st.text_input("Birth year")
        birthmonth = st.text_input("Birth month")
        birthday = st.text_input("Birth day of month")
        father = st.text_input("Father")
        mother = st.text_input("Mother")
        submit = st.button(":image_url: Submit Marriage", 'marriages')
        
        # Add a new user to the database
        #db = firestore.Client()
        doc_ref = db.collection('users').document('alovelace')
        doc_ref.set({
            'username': 'aluvlace',
            'first': 'Ada',
            'last': 'Lovelace',
            'month': 'April',
            'day': 17
        })

        # Once the post has submitted, upload it to the database
        if username and firstname and lastname and email and phone and streetaddress and postalcode and submit:
            try:
                # TODO: if username and first and last and phone and email not found
                doc_ref = db.collection("users").document(username)
                doc_ref.set({
                    "title": title,
                    "url": url,
                    "content": content
                })         
                st.balloons()       
                st.error("Post saved!", "")
            except:
                st.error("That didn't work! Sorry about that!", "🔥")    
            # finally:        
            #     st.balloons()


# Create a reference to the Google post.
doc_ref = db.collection("posts").document("Google")

# Then get the data at that reference.
doc = doc_ref.get()

# Let's see what we got!
st.write("The id is: ", doc.id)
st.write("The contents are: ", doc.to_dict())

# This time, we're creating a NEW post reference for Apple
doc_ref = db.collection("posts").document("Apple")

#And then uploading some data to that reference
doc_ref.set({
	"title": "Apple",
	"url": "www.apple.com"
})

# Now let's make a reference to ALL of the posts
posts_ref = db.collection("posts")

# For a reference to a collection, we use .stream() instead of .get()
for doc in posts_ref.stream():
	st.write("The id is: ", doc.id)
	st.write("The contents are: ", doc.to_dict())

if st.button('Balloons?'):
    st.balloons()
    
######
    
if "is_logged_in" not in st.session_state:
    st.session_state["is_logged_in"] = False


def login():
    if "btn_login" in st.session_state:
        st.session_state["is_logged_in"] = True


if not st.session_state["is_logged_in"]:
    st.button("Login", key="btn_login", on_click=login)
else:
    st.write("Logged in!")