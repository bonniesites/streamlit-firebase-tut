SIDEBAR = 'collapsed'
PAGE_HEADER = 'Login'
PAGE_SUBHEADER = ''

from mods.base import *


create_form(login_inputs, 'Log in', 'logins', False )    
st.divider()

'Not a member yet?'
create_form(signup_inputs, 'Sign Up', )

# Check for authenticated/logged in

# If  logged in/auth, go to Home

# Else, not logged in, show login screen with signup button

