#modules
import streamlit as st
from datetime import datetime
import json
import pandas as pd
import re


#functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.gptapi as gptapi
import functions.bigquery as bq

def list_to_html_list(lst):
    return "<ul>" + "".join(f"<li>{item}</li>" for item in lst) + "</ul>"


def clean_list_string(input_string):
    # Remove unnecessary formatting characters
    cleaned_string = re.sub(r'\\n', '\n', input_string)
    cleaned_string = re.sub(r'```python\n\[|\]\n```', '', cleaned_string)
    return cleaned_string


#main part of tnd tab
def structure(gpt_version_wanted, gpt_temp_wanted, lang_wanted):
    st.title("Headline structure & content generator")
    st.subheader("Inspiration for new headlines as well as content")
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("""<ul>
                <li>Provide generic informations about the article you need headlines for. You can provide marketing goals, page type informations and additional details about the page and target audience.</li>
                <li>Click "Generate Headlines" in order to request n-amount of headlines.</li>
                <li>You can choose each headline from the drop-down-menu and request additional content for this headline.</li>
               </ul>""", unsafe_allow_html=True)
    st.divider()

 ### Initialize session state variables
    if "goal_choice" not in st.session_state:
        st.session_state.goal_choice = ""
    if "target_audience" not in st.session_state:
        st.session_state.target_audience = ""
    if "target_topic" not in st.session_state:
        st.session_state.target_topic = ""
    if "nr_of_headlines_wanted" not in st.session_state:
        st.session_state.nr_of_headlines_wanted = 0
    if "headlines_gpt" not in st.session_state:
        st.session_state.headlines_gpt = []
    if "heading_chosen" not in st.session_state:
        st.session_state.heading_chosen = ""
    if "headings_generated" not in st.session_state:
        st.session_state.headings_generated = False
    if "list_count_chosen_headings" not in st.session_state:
        st.session_state.list_count_chosen_headings = 0
    if "nr_of_words_per_heading" not in st.session_state:
        st.session_state.nr_of_words_per_heading = 100
    if "content_for_headings_generated" not in st.session_state:
        st.session_state.content_for_headings_generated = False
    if "heading" not in st.session_state:
        st.session_state.heading = ""
    if "page_type" not in st.session_state:
        st.session_state.page_type = ""
    if "headline_content_generated" not in st.session_state:
        st.session_state.headline_content_generated = ""
    if "headline_content_generated_cost" not in st.session_state:
        st.session_state.headline_content_generated_cost = 0
    if "act_as_prompt_headline_content" not in st.session_state:
        st.session_state.act_as_prompt_headline_content = ""
    if "content_prompt_headline_content" not in st.session_state:
        st.session_state.content_prompt_headline_content = ""
    if "keep_in_mind_for_heading_content" not in st.session_state:
        st.session_state.keep_in_mind_for_heading_content = ""
    if "headlines_gpt_as_html" not in st.session_state:
        st.session_state.headlines_gpt_as_html = ""
    if "headline_content_stored_for_summary" not in st.session_state:
        st.session_state.headline_content_stored_for_summary = []
    if "headlines_stored_for_sumnmary" not in st.session_state:
        st.session_state.headlines_stored_for_sumnmary = []
    if "nr_of_words_for_summary" not in st.session_state:
        st.session_state.nr_of_words_for_summary = 100
    
    ### Input Fields
    with st.form(key = "headlines and content input fields form"):
        st.markdown("<h4>Provide generic information:</h4>", unsafe_allow_html=True)
        col1_generic_info, col2_generic_info = st.columns(2)
        with col1_generic_info:
            st.session_state.goal_choice = st.selectbox("What's the marketing goal of the page?", ["Brand Awareness", "Bookings", "After Sales / Service"], key="goal_of_page_for_headlines")
            st.session_state.page_type = st.selectbox("What's the page type?", ["Inspirational", "Informational", "Transactional"], key="page_type_for_headlines")
            st.session_state.nr_of_headlines_wanted = st.slider("How many headlines do you need?", 1, 50, key="nr_of_headlines_wanted_slider")

        with col2_generic_info:
            st.session_state.target_topic = st.text_area("What is this page all about?", key="target_topic_for_headlines")
            st.session_state.target_audience = st.text_area("What's the target audience of this article?", key="target_audience_for_headlines")
        form_submit_headlines_and_content_input_values = st.form_submit_button(label="Generate content")


    ### generate headings from here on
    if form_submit_headlines_and_content_input_values:
        st.session_state.act_as_prompt_headlines, st.session_state.content_prompt_headlines = gptprompts.headline_structure_prompt(lang_wanted, st.session_state.nr_of_headlines_wanted, st.session_state.goal_choice, st.session_state.target_audience, st.session_state.target_topic, st.session_state.page_type)
        st.session_state.headlines_generated, st.session_state.headlines_generated_cost, st.session_state.headlines_generated_gptversion = gptapi.openAI_content(st.session_state.act_as_prompt_headlines, st.session_state.content_prompt_headlines, gpt_temp_wanted, gpt_version_wanted)
        bq.to_bigquery("Headline Generator", st.session_state.headlines_generated_cost, "Headlines", st.session_state.target_topic, lang_wanted)

        try:
            headlines_list = json.loads(st.session_state.headlines_generated)
            if isinstance(headlines_list, list) and all(isinstance(item, str) for item in headlines_list):
                st.session_state.headlines_gpt = headlines_list
            else:
                raise ValueError("Invalid JSON list format")
        except (json.JSONDecodeError, ValueError):
            # Assuming st.session_state.headlines_generated is a string in the given format
            headlines_list = [item.strip(' "') for item in st.session_state.headlines_generated.strip("[]").split('",')]
            st.session_state.headlines_gpt = headlines_list

        # Displaying the cleaned Python list
        st.session_state.headlines_gpt_as_html = [clean_list_string(item) for item in st.session_state.headlines_gpt]
        # hier wird dann session state gesetzt, dass headings jetzt vorhanden sind
        st.markdown(f"### Following headlines were created:")
        st.write(st.session_state.headlines_gpt_as_html)
        st.session_state.headings_generated = True

    
    ###generate content for headings from here on
    if st.session_state.headings_generated == True:
        with st.form(key = "content for specific headlines"):
            st.markdown("<h4>Do you want to create content for the headlines?</h4>", unsafe_allow_html=True)
            st.session_state.heading_chosen = st.multiselect("Multi-Select: Choose a heading...", st.session_state.headlines_gpt_as_html)
            st.session_state.list_count_chosen_headings = len(st.session_state.heading_chosen)
            st.session_state.nr_of_words_per_heading = st.slider("Choose number of words per heading", 100, 2000, key = "heading_content_creation_nr_of_words")
            st.session_state.keep_in_mind_for_heading_content = st.text_area("Please keep the following informations in mind...", key = "heading_content_additional_infos_text_area")
            form_submit_content_for_specific_headlines_input_values = st.form_submit_button(label = "Generate content")

        if form_submit_content_for_specific_headlines_input_values:

            headline_content_generated_cost_list = []
            st.session_state.headlines_stored_for_summary = []
            st.session_state.headline_content_stored_for_summary = []
            for st.session_state.heading in st.session_state.heading_chosen:
                st.session_state.act_as_prompt_headline_content, st.session_state.content_prompt_headline_content = gptprompts.content_for_headline_prompt(lang_wanted, st.session_state.heading, st.session_state.nr_of_words_per_heading, st.session_state.keep_in_mind_for_heading_content)
                st.session_state.headline_content_generated, st.session_state.headline_content_generated_cost, st.session_state.headline_content_generated_gptversion = gptapi.openAI_content(st.session_state.act_as_prompt_headline_content, st.session_state.content_prompt_headline_content, gpt_temp_wanted, gpt_version_wanted)
                headline_content_generated_cost_list.append(st.session_state.headline_content_generated_cost)
                st.session_state.headlines_stored_for_summary.append(st.session_state.heading)
                st.session_state.headline_content_stored_for_summary.append(st.session_state.headline_content_generated)
                st.markdown(f"""
                            <h5>{st.session_state.heading}</h5>
                            <p>{st.session_state.headline_content_generated}</p>
                            """, unsafe_allow_html=True)
            total_cost_content_for_headlines = sum(headline_content_generated_cost_list)
            st.session_state.content_for_headings_generated = True
            bq.to_bigquery("Headline Generator", total_cost_content_for_headlines, "Content for Headlines", st.session_state.target_topic, lang_wanted)
        st.divider()

    #### generate conclusion / summary
    if st.session_state.content_for_headings_generated == True and st.session_state.headings_generated == True:
        with st.form(key = "create summary for this"):
            st.markdown("<h4>Do you want to create a summary for this content piece as well?</h4>", unsafe_allow_html=True)
            form_submit_generate_summary = st.form_submit_button(label = "Generate content")

            if form_submit_generate_summary:
                headline_content_stored_for_summary = "".join(st.session_state.headline_content_stored_for_summary)
                act_as_prompt_summary, content_prompt_summary = gptprompts.create_summary(lang_wanted, headline_content_stored_for_summary)
                summary_content_created, summary_content_created_cost, summary_content_created_gptversion = gptapi.openAI_content(act_as_prompt_summary, content_prompt_summary, gpt_temp_wanted, "gpt-3.5-turbo-1106")
                df_headline_content = pd.DataFrame()
                df_headline_content["Headlines"] = st.session_state.headlines_stored_for_summary
                df_headline_content["Content"] = st.session_state.headline_content_stored_for_summary
                for row in df_headline_content.itertuples(index=False):
                    st.markdown(f"""
                                <h5>{row.Headlines}</h5>
                                <p>{row.Content}</p>""", unsafe_allow_html=True)
                st.markdown(f"""<h5>Summary for {st.session_state.target_topic}</h5>
                        {summary_content_created}
                            """, unsafe_allow_html=True)
                bq.to_bigquery("Headline Generator", summary_content_created_cost, "Summary for Headlines", st.session_state.target_topic, lang_wanted)