import streamlit as st
import openai
import json
import pandas as pd
import io
from bs4 import BeautifulSoup
import requests
import string
from requests.exceptions import RequestException
import functions.gptapi as gptapi
import prompts.prompts as gptprompts


# SCRAPING FUNCTION #
@st.cache_data
def extract_text_from_url(link, choice, lang_wanted):
    try:
        page_response = requests.get(link, timeout=5)
        page_response.raise_for_status()  # Raise an exception for non-200 status codes
        if page_response.status_code == 200:
            soup = BeautifulSoup(page_response.text, "html.parser")
            soup = soup.find_all(["p", "table", "tr", "td"])

            extracted_text = []
            for tag in soup:
                extracted_text.append(tag.get_text())
                extracted_text = [text.replace("\n", " ") for text in extracted_text]
                extracted_text = [text.replace("\t", " ") for text in extracted_text]
                extracted_text = [text.replace("xa", " ") for text in extracted_text]
                extracted_text = [text.replace("xa0", " ") for text in extracted_text]
            
            current_sight_text = ' '.join(extracted_text)

            
            # Call your openAI_content function here with current_sight_text
            if choice == "oeffnungszeiten":
                oeffnungszeiten_prompt = gptprompts.oeffnungszeiten_prompt(lang_wanted)
                zeiten, zeiten_cost, zeiten_gpt_version = gptapi.openAI_content(oeffnungszeiten_prompt, current_sight_text, 0.1, 0.5, "gpt-3.5-turbo-16k")
                return zeiten, zeiten_cost
            elif choice == "eintrittskosten":
                eintrittskosten_prompt = gptprompts.eintrittskosten_prompt(lang_wanted)
                kosten, kosten_cost, kosten_gpt_version = gptapi.openAI_content(eintrittskosten_prompt, current_sight_text, 0.1, 0.5, "gpt-3.5-turbo-16k")
                return kosten, kosten_cost   
            elif choice == "summary":
                return current_sight_text         
            
    except requests.exceptions.RequestException as e:
        #st.warning(f"Error requesting URL '{link}': {e}")
        if choice == "oeffnungszeiten":
            zeiten = "🍜 was not able to crawl the provided URL."
            zeiten_cost = 0.0
            return zeiten, zeiten_cost
        if choice == "eintrittskosten":
            kosten = "🍜 was not able to crawl the provided URL."
            kosten_cost = 0.0
            return kosten, kosten_cost
    except requests.exceptions.Timeout:
        #st.warning(f"Timeout for {link}")
        if choice == "oeffnungszeiten":
            zeiten = "Timeout for Crawling-Request."
            zeiten_cost = 0.0
            return zeiten, zeiten_cost
        if choice == "eintrittskosten":
            kosten = "Timeout for Crawling-Requests."
            kosten_cost = 0.0
            return kosten, kosten_cost

    except Exception as e:
        #st.warning(f"An unexpected error occurred: {e}")
        if choice == "oeffnungszeiten":
            zeiten = "🍜 was not able to crawl the provided URL."
            zeiten_cost = 0.0
            return zeiten, zeiten_cost
        if choice == "eintrittskosten":
            kosten = "🍜 was not able to crawl the provided URL."
            kosten_cost = 0.0
            return kosten, kosten_cost

    
