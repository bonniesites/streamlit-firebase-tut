from mods.base import *
from mods.utils import *


# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
# If logged in, show profile dashboard page, else go to login pg
if st.session_state.username == '':
    st.switch_page('pages/010_Login.py')
else:
    st.sidebar.write(f"You are logged in as {st.session_state.username}")

    st.header("My Profile ")

# stats on posting, replying, etc.

# Edit button, goes to Edit Profile Page

# TODO: How to hide page from menu programatically

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #
# MY LIVE APPS
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&& #

# [https://rus19023.github.io/scripturechase/](My Scripture Chase App)

# [https://rus19023.github.io/goalsapp/](My SMART Goals Journal App (Vanilla JavaScript))
# [https://rus19023.github.io/csa_game/](My BYUI CSA Quiz Game App)

# [https://my-reddit.streamlit.app/](My Reddit Clone App)

# [https://drushlopez.streamlit.app/](My Portfolio Site)

# [https://newgoalsapp.streamlit.app/](My New SMART Goals Journal App (Python))

#[https://rushblog.streamlit.app](My Family Social Media App)


#[https://drushlopez.dev/](Need to link to My Portfolio Site when ready)


#[]()


#[]()


#[]()
