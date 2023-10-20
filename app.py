#### import libraries
import streamlit as st
import openai
import json
import pandas as pd
import io
from bs4 import BeautifulSoup
import requests
import string
from requests.exceptions import RequestException
import xlsxwriter
import streamlit_authenticator as stauth
import yaml

### functions from other files
import functions.bingapifunction as bingapi
import functions.gptapi as gptapi

import tabs.about as about_tab
import tabs.tnd as tnd_tab
import tabs.sights_generation as sights_tab
import tabs.sidebar as sidebar
import tabs.headline_structure as headlines
import tabs.beach_generation as beach
import tabs.summary as summary


########################################################################################################################
# Set the page configuration
st.set_page_config(
    layout="wide",
    page_title="GPT Tool | Urlaubsguru",
    initial_sidebar_state="expanded", #collapsed
    page_icon="🤖"
)

#creating login widget
from yaml.loader import SafeLoader
with open("credentials.yaml") as file:
   config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)
name, authentication_status, username = authenticator.login("Login", "main")
#######
########################################################################################################################
#### Sidebar
with st.sidebar:
    gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted = sidebar.sidebar(authentication_status, authenticator)
########################################################################################################################
if authentication_status:
   tab1, tab2, tab5, tab4, tab6, tab3 = st.tabs([
      "🧙‍♂️ Title & Description |",
      "🏞️ Sights |",
      "🏖️ Beaches |",
      "🦄 Headlines + Content |",
      "🟰 Summaries |",
      #"📸 Alt Texts |",
      "❓ Prompts"
      ])

   with tab1:
      tnd_tab.tnd(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)

   with tab2:
      sights_tab.sights_gen(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)
      
   with tab3:
      about_tab.about()

   with tab4:
      headlines.structure(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)

   with tab5:
      beach.beach_gen(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)

   with tab6:
      summary.get_summary(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)
elif authentication_status == False:
   st.error("Username/password is incorrect")
elif authentication_status == None:
   st.warning("Please enter your username and password")
   st.divider()
   st.subheader("Additional options")

   login_col1, login_col2 = st.columns(2)
   with login_col1:
      try:
         if authenticator.register_user("Register user", preauthorization=True):
            st.success("User registered successfully")
            with open("credentials.yaml", "w") as file:
               yaml.dump(config, file, default_flow_style=False)
      except Exception as e:
         st.error(e)

   with login_col2:
      try:
         username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password('Forgot password')
         if username_of_forgotten_password:
            st.success(f'New password sent to {email_of_forgotten_password}') # update to be sent via EMAIL
            with open("credentials.yaml", "w") as file:
               yaml.dump(config, file, default_flow_style=False)
         else:
            st.error('Username not found')
      except Exception as e:
         st.error(e)

