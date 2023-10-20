#modules
import streamlit as st
from datetime import datetime
import json
import pandas as pd
import re
from bs4 import BeautifulSoup
import requests


#functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.gptapi as gptapi
import functions.bigquery as bq
import functions.scrapingfunction as scraping

def get_summary(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted):
    st.title("Receive summaries from content")
    st.subheader("Generate summaries of any given content")
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("""<ul>
                <li>Choose what kind of summary you need.</li>
                <li>Depending on the summary type you can get more facts or broader concepts of your source.</li>
               </ul>""", unsafe_allow_html=True)
    st.divider()
       ### Input Fields
    
    st.subheader("Summary from webpages")
    col1_get_content_summary, col2_get_content_summary = st.columns(2)
    with col1_get_content_summary:
        url_for_scraping = st.text_input("URL")

    with col2_get_content_summary:
        kind_of_summary = st.selectbox("What kind of summary do you want?", ["Most important informations", "Very short with key aspects", "Focus on broader topics", "Chronological summary", "Facts focused"])
        if kind_of_summary == "Most important informations":
            kind_of_summary_todo = "Fasse mir den Text als Informative Zusammenfassung zusammen und konzentriere dich auf die Übertragung der wichtigsten Informationen aus dem Text. Sei sachlich und stelle die Fakten klar dar. Kommuniziere mir Daten und Fakten."
        if kind_of_summary == "Very short with key aspects":
            kind_of_summary_todo = "Fasse mir den Text kurz und knapp als Kurze Zusammenfassung zusammen. Konzetriere dich auf das absolute Minimum an Informationen, um den Hauptpunkt des Textes zu vermitteln. Kommuniziere mir Daten und Fakten."
        if kind_of_summary == "Focus on broader topics":
            kind_of_summary_todo = "Hebe die Hauptthemen und Konzepte des Textes hervor. Ignoriere dabei die Details. Ich möchte mich auf die großen Ideen konzentrieren."
        if kind_of_summary == "Chronological summary":
            kind_of_summary_todo = "Fasse die Reihenfolge von Ereignissen oder Informationen im Text zusammen mittels Chronologischer Zusammenfassung.  Kommuniziere mir Daten und Fakten."         
        if kind_of_summary == "Facts focused":
            kind_of_summary_todo = "Fasse den Text mittels Statistischer Zusammenfassung zusammen. Hebe statistische Daten oder Fakten aus dem Text hervor.  Kommuniziere mir Daten und Fakten." 
   
    if st.button("Give me a summary :rocket:"):
        scraping_result = scraping.extract_text_from_url(url_for_scraping, "summary", lang_wanted)
        word_count_scraped_result = len(scraping_result.split())
        
        if word_count_scraped_result < 6000:
            summary_webpage, summary_webpage_cost, summary_webpage_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung. Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {scraping_result}", 0.1, 0.5, "gpt-4")
            st.subheader(f"Summary: {url_for_scraping}")
            st.write(summary_webpage)
            bq.to_bigquery("Summary Generator: Webpage", summary_webpage_cost, kind_of_summary, url_for_scraping, lang_wanted)

        if 6000 <= word_count_scraped_result <= 13000:
            st.info(f"Long word count detected ({word_count_scraped_result:,d}). Splitting in half...")
            first_half = scraping_result[:len(scraping_result)//2]
            second_half = scraping_result[len(scraping_result)//2:]
            summary_webpage_first_half, summary_webpage_first_half_cost, summary_webpage_first_half_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung.  Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {first_half}", 0.1, 0.5, "gpt-3.5-turbo-16k")
            summary_webpage_second_half, summary_webpage_second_half_cost, summary_webpage_second_half_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung.  Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {second_half}", 0.1, 0.5, "gpt-3.5-turbo-16k")
            summary_webpage_cost = summary_webpage_first_half_cost + summary_webpage_second_half_cost
            st.subheader(f"Summary 1/2 for: {url_for_scraping}")
            st.write(summary_webpage_first_half)
            st.subheader(f"Summary 2/2 for: {url_for_scraping}")
            st.write(summary_webpage_second_half)
            bq.to_bigquery("Summary Generator: Webpage", summary_webpage_cost, kind_of_summary, url_for_scraping, lang_wanted)

        if 13001 <= word_count_scraped_result <= 19000:
            st.info(f"Long word count detected ({word_count_scraped_result:,d}). Splitting in triple...")
            parth_length = len(scraping_result) // 3
            first_triple = scraping_result[:parth_length]
            second_triple = scraping_result[parth_length:2 * parth_length]
            third_triple = scraping_result[2 * parth_length:]
            summary_webpage_first_half, summary_webpage_first_half_cost, summary_webpage_first_half_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung. Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {first_triple}", 0.1, 0.5, "gpt-3.5-turbo-16k")
            summary_webpage_second_half, summary_webpage_second_half_cost, summary_webpage_second_half_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung.  Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {second_triple}", 0.1, 0.5, "gpt-3.5-turbo-16k")
            summary_webpage_third_half, summary_webpage_third_half_cost, summary_webpage_second_half_gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung.  Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {third_triple}", 0.1, 0.5, "gpt-3.5-turbo-16k")
            summary_webpage_cost = summary_webpage_first_half_cost + summary_webpage_second_half_cost + summary_webpage_third_half_cost
            st.subheader(f"Summary 1/3 for: {url_for_scraping}")
            st.write(summary_webpage_first_half)
            st.subheader(f"Summary 2/3 for: {url_for_scraping}")
            st.write(summary_webpage_second_half)
            st.subheader(f"Summary 3/3 for: {url_for_scraping}")
            st.write(summary_webpage_third_half)
            bq.to_bigquery("Summary Generator: Webpage", summary_webpage_cost, kind_of_summary, url_for_scraping, lang_wanted)

        if 19000 < word_count_scraped_result < 26000:
            st.info(f"Long word count detected ({word_count_scraped_result:,d}). Splitting into quarters...")
            part_length = len(scraping_result) // 4
            first_quarter = scraping_result[:part_length]
            second_quarter = scraping_result[part_length:2 * part_length]
            third_quarter = scraping_result[2 * part_length:3 * part_length]
            fourth_quarter = scraping_result[3 * part_length:]
            
            # Generate summaries for each quarter
            summary_webpage_cost = []
            for i, quarter in enumerate([first_quarter, second_quarter, third_quarter, fourth_quarter], start=1):
                summary, cost, gpt_version = gptapi.openAI_content("", f"Antworte mir {lang_wanted }. Erstelle mir eine Zusammenfassung. Nutze diese Art der Zusammenfassung: {kind_of_summary_todo}. Inhalt: {quarter}", 0.1, 0.5, "gpt-3.5-turbo-16k")
                st.subheader(f"Summary {i}/4 for: {url_for_scraping}")
                st.write(summary)
                summary_webpage_cost.append(cost)
            
            summary_webpage_cost = sum(summary_webpage_cost)
            summary_webpage_cost = summary_webpage_first_half_cost + summary_webpage_second_half_cost + summary_webpage_third_half_cost
            bq.to_bigquery("Summary Generator: Webpage", summary_webpage_cost, kind_of_summary, url_for_scraping, lang_wanted)

        #
    #choose if url, then take url and scrape the content, push to gpt and get summary
    #choose if youtube video, take url, get mp3, transcript it and push to gpt to get summary
    #choose if instagram video, take url, get mp3, transcript it and push to gpt to get summary
    #choose if tiktok video, take url, get mp3, transcript it and push to get summary