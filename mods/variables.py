from mods.imports import *


PAGE_HEADER = 'My SMART Goals Journal'



# ENVIRONMENT VARIABLES

if os.path.exists('/.dockerenv'):
    custom_print(' \n Running in Docker container, assuming production environment \n ')
    HOST = os.environ['HOST']
    SERVER_API = os.environ['SERVER_API']
    PORT = os.environ['PORT']
    DB_NAME = os.environ['DB']
    COLL_NAME = os.environ['COLL']
    USERS_COLL = os.environ['USERS']
else:
    #custom_print('Not running in Docker container (assuming development environment)')
    HOST = st.secrets.mongo.host_dev
    SERVER_API = st.secrets.mongo.server
    USERS_COLL_NAME = st.secrets.mongo.users_coll
    OLD_DB_NAME = st.secrets.mongo.old_db
    OLD_COLL_NAME = st.secrets.mongo.old_coll
    PORT_STRING = st.secrets.mongo.port_string
    DB_NAME = st.secrets.mongo.goals_db
    COLL_NAME = st.secrets.mongo.goals_coll


PORT = int(PORT_STRING)

FILTER_ALL = {}
SORT_TIMESTAMP = 'timestamp'
DEFAULT_SORT_ORDER = pymongo.DESCENDING




search_box = st.sidebar.empty()
counter_box = st.sidebar.empty()
MSG_CONTAINER = st.sidebar.empty()