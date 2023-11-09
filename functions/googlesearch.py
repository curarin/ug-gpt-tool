import streamlit as st
import advertools as adv

cse_id = st.secrets["cse_id"]
api_key = st.secrets["google_api_key"]

@st.cache_data
def google_serp(query, top_results_wanted, lang_wanted, country_wanted):
    if lang_wanted == "Deutsch":
        cse_language = "de"
        if country_wanted == "Deutschland":
            cse_country = "countryDE"
        elif country_wanted == "Österreich":
            cse_country = "countryAT"
        elif country_wanted == "Schweiz":
            cse_country = "countryCH"
    elif lang_wanted == "Spanisch":
        cse_language = "es"
        cse_country = ""
    elif lang_wanted == "Holländisch":
        cse_language = "nl"
        cse_country = ""
    elif lang_wanted == "Englisch":
        cse_language = "en"
        cse_country = ""
    
    df = adv.serp_goog(
        q=query, key=api_key, cx=cse_id, gl=cse_language, cr=cse_country)
    
    top_links = df.head(top_results_wanted)["link"].tolist()
    return top_links