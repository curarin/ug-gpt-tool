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

### functions from other files
import functions.scrapingfunction as scrapingfunction
import functions.googlesearch as googleapi
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.bigquery as bq

def dict_to_html_list(data):
    html = "<ul>"
    for key, value in data.items():
        html += f"<li>{key}: {value}</li>"
    html += "</ul>"
    return html


def sights_gen(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted):
   st.title("Sights article generation")
   st.subheader("Generate points of interest and/or expand existing articles")
   st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
   st.markdown("""<ul>
               <li>Enter the number of sights required using the number slider.</li>
               <li>Enter the required word count per sight.</li>
               <li>Enter the destination for which new sights should be generated.</li>
               <li>In case of an article update: Insert all currently existing sights in the article. This ensures that these points of interest are <b>not</b> generated explicitly.</li>
               <li>Enter the desired search results, which are searched for current opening times and ticket prices. <b>Recommendation</b>: Top 3 is usually sufficient. (Data source: Bing)</li>
               <li>Click on the <b><u>Generate sights</u></b> button.</li>
               <li>If necessary, all generated content can be downloaded as an Excel document.</li>
               </ul>""", unsafe_allow_html=True)

   #### Building Dataframe
   columns_for_new_sights_df = [
      "name of sight",
      "description of sight",
      "source opening times",
      "source ticket costs",
      "tipp for picture content"
   ]
   df_html_new_sights = pd.DataFrame(columns=columns_for_new_sights_df)

   ###Input Felder
   st.divider()
   st.markdown("<h4>Provide informations:</h4>", unsafe_allow_html=True)

   col1_sights_top_info, col2_sights_top_info = st.columns(2)
   with col1_sights_top_info:
    destination_wanted = st.text_input("Which destination needs additional sights?")
    sights_not_needed = st.text_area("Which sights are currently mentioned? _Note: 1 sight = 1 line_")
    sights_not_needed = [sights_not_needed.strip() for sights_not_needed in sights_not_needed.split("\n")]
    number_of_sights_wanted = st.number_input("Number of additional sights required", min_value=1, max_value=25, value=5, placeholder="Enter number of additional sights...", key = "main number of sights wanted input")    
    content_length_wanted = st.slider("Approximate number of words per sight", 200, 1500, 500, key = "main slider content length per sight")
    
    
   with col2_sights_top_info:
    st.markdown("**Get current data for ticket prizes and opening hours from google:**")
    if lang_wanted == "Deutsch":
       country_wanted = st.selectbox("Choose country for google results", ["Deutschland", "Österreich", "Schweiz"], key = "selectbox country input")
    else:
       country_wanted = ""
    number_of_search_results_wanted = st.number_input("How many top search results should be crawled for opening times & ticket prices?", min_value=1, max_value=5, value=3, placeholder="Enter number of crawling results...", key = "number of sights wanted for upgrading")


   
   ### hier started der API Call

   st.divider()
   if st.button("Generate sights :rocket:"):    
    ###GPT Prompts
    act_as_prompt_sights, structure_prompt_sights = gptprompts.sight_prompts(number_of_sights_wanted, destination_wanted, sights_not_needed, lang_wanted)

    ### API Call
    top_sights, top_sights_cost, top_sights_gtpversion = gptapi.openAI_content(act_as_prompt_sights, structure_prompt_sights, gpt_temp_wanted, gpt_top_p_wanted, gpt_version_wanted)
    try:
        input_list_for_update = json.loads(top_sights)
    
        if isinstance(input_list_for_update, list) and all(isinstance(item, str) for item in input_list_for_update):
            output_list_for_update = input_list_for_update
        else:
            raise ValueError("Invalid JSON list format")

    except (json.JSONDecodeError, ValueError):
        input_list_for_update = [item.strip("' ") for item in top_sights.strip("[]").split(",")]
        output_list_for_update = input_list_for_update
    
    sight_list_for_update = output_list_for_update
    st.subheader("These sights are going to be added:")
    for sight_to_be_added in sight_list_for_update:
        st.write(sight_to_be_added)
    st.divider()

    ### Loop through sights and generate content
    sight_content_cost = []
    serp_results_cost = []
    i = 0
    for new_sight in sight_list_for_update:
       #### Print current state to App
       i += 1
       length_sight_list = len(sight_list_for_update)
       st.subheader(f"{i}/{length_sight_list}: {new_sight}")
       ### Sight GPT Prompts
       content_prompt_new_sight, content_pic_prompt = gptprompts.new_sight_prompt(content_length_wanted, new_sight, destination_wanted, lang_wanted)
   
       ### generate content
       new_sight_content, new_sight_content_cost, new_sight_content_gptversion = gptapi.openAI_content(act_as_prompt_sights, content_prompt_new_sight, gpt_temp_wanted, gpt_top_p_wanted, gpt_version_wanted)
       sight_content_cost.append(new_sight_content_cost)
       new_sight_pic_content, new_sight_pic_content_cost, new_sight_pic_content_gptversion = gptapi.openAI_content(act_as_prompt_sights, content_pic_prompt, gpt_temp_wanted, gpt_top_p_wanted, gpt_version_wanted)
       sight_content_cost.append(new_sight_pic_content_cost)

       
       # build queries for bing and get results 
       if lang_wanted == "Deutsch":
            sight_cost = new_sight + " Eintrittspreise"
            sight_zeiten = new_sight + " Öffnungszeiten"
       elif lang_wanted == "Spanisch":
            sight_cost =  "entrada " + new_sight
            sight_zeiten =  "horario " + new_sight
       elif lang_wanted == "Holländisch":
            sight_cost = "prijzen " + new_sight
            sight_zeiten = new_sight + " openingstijden"
       elif lang_wanted == "Englisch":
            sight_cost = new_sight + " entry fee"
            sight_zeiten = new_sight + " opening hours"

        
        
       links_zeiten_google = googleapi.google_serp(sight_zeiten, number_of_search_results_wanted, lang_wanted, country_wanted)
       links_kosten_google = googleapi.google_serp(sight_cost, number_of_search_results_wanted, lang_wanted, country_wanted)

       
       # ### generate content from bing result pages
       opening_hours_dict = {}
       for link in links_zeiten_google:
           zeiten, zeiten_cost = scrapingfunction.extract_text_from_url(link, "oeffnungszeiten", lang_wanted)
           serp_results_cost.append(zeiten_cost)
           opening_hours_dict[link] = zeiten
       
       ticket_prices_dict = {}
       for link in links_kosten_google:
           kosten, kosten_cost = scrapingfunction.extract_text_from_url(link, "eintrittskosten", lang_wanted)
           serp_results_cost.append(kosten_cost)
           ticket_prices_dict[link] = kosten

       
       #generate HTML
       data_html_for_new_sights = {
          "name of sight": new_sight,
          "description of sight": new_sight_content,
          "source opening times": opening_hours_dict,
          "source ticket costs": ticket_prices_dict,
          "tipp for picture content": new_sight_pic_content
       }
       df_to_append = pd.DataFrame([data_html_for_new_sights])
       df_html_new_sights = pd.concat([df_html_new_sights, df_to_append], ignore_index=True)


       ### print to chat as list for easier copy-paste
       st.write(f"""
                <h4>Description of {new_sight}</h4>
                <p>{new_sight_content}</p>
                <h4>Opening hours for {new_sight}</h4>
                <p>{dict_to_html_list(opening_hours_dict)}</p>
                <h4>Entry fees for {new_sight}</h4>
                <p>{dict_to_html_list(ticket_prices_dict)}</p>
                """, unsafe_allow_html=True)
       st.divider()
    
    
    ### Kosten berechnen
    total_sight_content_cost = sum(sight_content_cost)
    total_serp_cost = sum(serp_results_cost)


    all_cost_sights_update = (
       top_sights_cost +
       total_sight_content_cost +
       total_serp_cost
       )
    all_cost_sights_update = round(all_cost_sights_update, 5)
    
    ### push to google bigquery
    number_of_sights_str = str(number_of_sights_wanted)
    content_length_wanted_str = str(content_length_wanted)
    number_of_search_results_wanted_str = str(number_of_search_results_wanted)
    additional_usage_information = ",".join(filter(None, [number_of_sights_str, content_length_wanted_str, number_of_search_results_wanted_str]))
    bq.to_bigquery("Sights Generator", all_cost_sights_update, destination_wanted, additional_usage_information, lang_wanted)


    #### Implement Download button which caches the data
    st.subheader("Download generated data")
    @st.cache_data
    def convert_df_to_excel(df):
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_data = excel_buffer.getvalue()
        return excel_data
    new_sights_excel = convert_df_to_excel(df_html_new_sights)

    st.download_button(f"Download sight conbtent for {destination_wanted} as Excel-spreadsheet", data=new_sights_excel, file_name=f"{destination_wanted}_new_sights.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.divider()
    #####################
