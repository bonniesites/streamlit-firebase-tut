PAGE_HEADER = 'BYU-I PATHWAY STUDY SKILLS'

from mods.base import *

urls = {
    'PDF file': 'https://content.byui.edu/file/d901d815-c4ed-4fd0-a731-3762dc38b846/10/BookofMormon_StudySkills.pdf',
    'Substitution': 'http://www.kaltura.com/tiny/ds27r',
    'Setting': 'http://www.kaltura.com/tiny/f6rue',
    'Principles & Doctrines': 'http://www.kaltura.com/tiny/efy8y',
    'List': 'http://www.kaltura.com/tiny/6tepq',
    'Clustering': 'http://www.kaltura.com/tiny/6ln0z',
    'Flag Phrases': 'http://www.kaltura.com/tiny/had4c',
    'Symbolism': 'http://www.kaltura.com/tiny/813j8',
    'Visualization': 'http://www.kaltura.com/tiny/evnm9',
    'Cause & Effect': 'http://www.kaltura.com/tiny/ez87w'
}

urls2 = '''
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
'''


with st.container():
    for key, value in urls.items():
        st.markdown(f'{key}: {value}', unsafe_allow_html=True)
        

with st.container():
    for key, value in urls2.items():
        st.markdown(urls2, unsafe_allow_html=True)

