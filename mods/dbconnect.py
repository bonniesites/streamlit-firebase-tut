import streamlit as st
from google.cloud import firestore
from google.oauth2 import service_account
import os 
import json

# Authenticate to Firestore
key_dict = json.loads(st.secrets["textkey"])
creds = service_account.Credentials.from_service_account_info(key_dict)


@st.cache_resource
def get_db():
    db = firestore.Client(credentials=creds, project="streamlit-reddit-5b36c")
    return db