#### import libraries
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup

from requests.exceptions import RequestException
import yaml
import hmac

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
import tabs.alt_tags as alt


########################################################################################################################
# Set the page configuration
st.set_page_config(
    layout="wide",
    page_title="GPT Tool | Urlaubsguru",
    initial_sidebar_state="expanded", #collapsed
    page_icon="🤖"
)

########################################################################################################################
#### Sidebar
with st.sidebar:
    gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted = sidebar.sidebar()
########################################################################################################################
def check_password():
    """Returns `True` if the user had a correct password."""

    def login_form():
        """Form with widgets to collect user information"""
        with st.form("Credentials"):
            st.text_input("Username", key="username")
            st.text_input("Password", type="password", key="password")
            st.form_submit_button("Log in", on_click=password_entered)

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["username"] in st.secrets[
            "passwords"
        ] and hmac.compare_digest(
            st.session_state["password"],
            st.secrets.passwords[st.session_state["username"]],
        ):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the username or password.
            del st.session_state["username"]
        else:
            st.session_state["password_correct"] = False

    # Return True if the username + password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show inputs for username + password.
    login_form()
    if "password_correct" in st.session_state:
        st.error("😕 User not known or password incorrect")
    return False
if not check_password():
    st.stop()
########################################################################
tab1, tab2, tab5, tab4, tab6, tab7, tab3 = st.tabs([
      "🧙‍♂️ Title & Description |",
      "🏞️ Sights |",
      "🏖️ Beaches |",
      "🦄 Headlines + Content |",
      "🟰 Summaries |",
      "📸 Alt Texts |",
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

with tab7:
     alt.generate_alt_text(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted)
