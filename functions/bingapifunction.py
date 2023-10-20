import streamlit as st
import openai
import json
import pandas as pd
import io
from bs4 import BeautifulSoup
import requests
import string
from requests.exceptions import RequestException

#### API KEY
BING_API_KEY = st.secrets["bing_api_key"]
bing_key = BING_API_KEY


### BING FUNCTION ###
@st.cache_data
def bing_top_result(query, top_results_wanted, lang_wanted):
    if lang_wanted == "Deutsch":
        mkt_value = "de-DE"
    elif lang_wanted == "Spanisch":
        mkt_value = "es-ES"
    elif lang_wanted == "Holländisch":
        mkt_value = "nl-NL"
    elif lang_wanted == "Englisch":
        mkt_value = "en-GB"
    params = {
        "q": query,
        "count": 10,
        "mkt": mkt_value
    }
    headers = {
    "Ocp-Apim-Subscription-Key": bing_key
    }
    response = requests.get("https://api.bing.microsoft.com/v7.0/search", params=params, headers=headers)
    if response.status_code == 200:
        # Parse and print the search results
        search_results = response.json()
        
        # Check if "webPages" and "value" are present in the response
        if 'webPages' in search_results and 'value' in search_results['webPages']:
            web_pages = search_results["webPages"]["value"][:top_results_wanted]

            bing_urls = []
            for web_page in web_pages:
                url = web_page["url"]
                bing_urls.append(url)
            return bing_urls
                
        else:
            st.warning("No 'webPages' or 'value' found in the search results.")
    else:
        st.warning(f"Error: {response.status_code} - {response.text}")
        return response
    return bing_urls
