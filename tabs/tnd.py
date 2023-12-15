#modules
import streamlit as st


#functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.gptapi as gptapi
import functions.bigquery as bq

#main part of tnd tab
def tnd(gpt_version_wanted, gpt_temp_wanted, lang_wanted):
    st.title("Title & Description Generator")
    st.subheader("Inspiration for meta tags of your current article")
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("""<ul>
                <li>Select a content template.</li>
                <li>Depending on the selected template, further selection options are now available.</li>
                <li>Select the destination.</li>
                <li>Select from the check boxes whether the title or description tag should contain additional information (year, month, emoji,...).</li>
                <li>Click on the button "Generate Title and Description Tag" to generate the respective tags via GPT.</li>
               </ul>""", unsafe_allow_html=True)
    st.divider()

    ### leere fehler erzeugen, die anschließend durch Multiple Choice befüllt werden
    title_tag_generated_gptversion = ""
    number_of_elements_for_listicle = 0
    total_cost_tnd = 0.0
    title_tag_generated_cost = 0.0
    descr_tag_generated_cost = 0.0
    focus_keyword_input = ""
    title_tag_generated = ""
    title_tag_generated_length = ""
    title_tag_length_ok = 0
    descr_tag_generated = ""
    descr_tag_generated_length = ""
    descr_tag_length_ok = ""
    special_info_template = ""



    ### hier folgen die Input Felder
    st.markdown("### Provide information")
    tnd_template_choice = st.selectbox("Choose template", ["Transactional: Destination", "Inspirational: Sights-Article"])

    col1_overview, col2_overview = st.columns(2)
    with col1_overview:
        st.markdown("#### Add year / month / emojis")
        st.markdown("**Title Tag**")
        selected_year_number_title = st.checkbox("year", key = "title_checkbox_year")
        selected_month_number_title = st.checkbox("name of month", key = "title_checkbox_month")
        selected_emoji_title = st.checkbox("emoji", key = "title_checkbox_emoji")

        

    with col2_overview:
        st.markdown("**Description Tag**", unsafe_allow_html=True)
        selected_year_number_descr = st.checkbox("year", key = "descr_checkbox_year")
        selected_month_number_descr = st.checkbox("name of month", key = "descr_checkbox_month")
        selected_emoji_descr = st.checkbox("emoji", key = "descr_checkbox_emoji")

    st.divider()
    with st.form(key="titles & description input form"):
        col1_generic_info, col2_generic_info = st.columns(2)
        with col1_generic_info:
            focus_keyword_input = st.text_input("Destination:", key = "generic_input_fokus_kw")
            if tnd_template_choice == "Transactional: Destination":
                urlaubsart_input = st.text_input("Enter type of holiday: (holiday, wellness weekend, weekend trip, all-inclusive, last minute,...)", key = "urlaubsart_input")
            elif tnd_template_choice == "Inspirational: Sights-Article":
                urlaubsart_input = st.text_input("Enter top 10 article type: (sights, restaurants, activities,...)", key = "sights_urlaubsart_input")
                number_of_elements_for_listicle = st.slider("Number of elements in the top X article", 6, 30, key = "generic_listicle_number_of_elements_input")
                special_info_template = st.text_area("Which top sights/activities/... are the most important? Name 3:", key = "generic_listicle_must_have_input")
                special_info_template = [special_info_template.strip() for special_info_template in special_info_template.split("\n")]
            
        with col2_generic_info:
            if any([selected_year_number_title, selected_month_number_title, selected_emoji_title, selected_year_number_descr, selected_month_number_descr, selected_emoji_descr]):
                st.markdown("**Input for additional informations:**", unsafe_allow_html=True)
                if selected_year_number_title == True:
                    selected_year_number_title = st.text_input("Title Tag: Waiting for year...", key = "title_input_year")
                else:
                    selected_year_number_title = ""
                if selected_month_number_title == True:
                    selected_month_number_title = st.text_input("Title Tag: Waiting for name of month(s)...", key = "title_input_month")
                else:
                    selected_month_number_title = ""
                if selected_emoji_title == True:
                    selected_emoji_title = st.selectbox("Title Tag: Choose emoji", ["❤️", "🔥", "🌎", "✨", "🚀", "✅", "🥰", "🫶", "🎉", "👌", "🌴", "☀️", "✈️", "🏨", "➡️", "⬇️", "⬅", "⬆️"], key = "emoji_input_list_title")
                else:
                    selected_emoji_title = ""
                if selected_year_number_descr == True:
                    selected_year_number_descr = st.text_input("Descr. Tag: Waiting for year...", key = "descre_input_year")
                else:
                    selected_year_number_descr = ""
                if selected_month_number_descr == True:
                    selected_month_number_descr = st.text_input("Descr. Tag: Waiting for name of month(s)...", key = "descr_input_month")
                else:
                    selected_month_number_descr = ""
                if selected_emoji_descr == True:
                    selected_emoji_descr = st.selectbox("Descr. Tag: Choose emoji", ["❤️", "🔥", "🌎", "✨", "🚀", "✅", "🥰", "🫶", "🎉", "👌", "🌴", "☀️", "✈️", "🏨", "➡️", "⬇️", "⬅", "⬆️"], key = "emoji_input_list_descr")
                else:
                    selected_emoji_descr = ""
        
        #logic to determine which finetuned gpt models are used
        if tnd_template_choice == "Transactional: Destination":
            gpt_version_wanted_title = "ft:gpt-3.5-turbo-1106:urlaubsguru-gmbh::8Uat3tmq"
            gpt_version_wanted_descr = "ft:gpt-3.5-turbo-1106:urlaubsguru-gmbh::8UayOp16"
            gpt_version_wanted_h1 = "ft:gpt-3.5-turbo-1106:urlaubsguru-gmbh::8UbLqj0V"
        elif tnd_template_choice == "Inspirational: Sights-Article":
            gpt_version_wanted_title = gpt_version_wanted
            gpt_version_wanted_descr = gpt_version_wanted
            gpt_version_wanted_h1 = gpt_version_wanted
        
        ####
        form_submit_tnd_input_values = st.form_submit_button(label="Generate content")

    if form_submit_tnd_input_values:
        #gpt prompts
        act_as_prompt_title, content_prompt_title = gptprompts.title_tag_prompt(tnd_template_choice, number_of_elements_for_listicle, focus_keyword_input, selected_year_number_title, selected_month_number_title, selected_emoji_title, special_info_template, urlaubsart_input, lang_wanted)
        act_as_prompt_descr, content_prompt_descr = gptprompts.meta_description_prompt(tnd_template_choice, number_of_elements_for_listicle, focus_keyword_input, selected_year_number_descr, selected_month_number_descr, selected_emoji_descr, special_info_template, urlaubsart_input, lang_wanted)
        act_as_prompt_h1, content_prompt_h1 = gptprompts.h1_prompt(tnd_template_choice, number_of_elements_for_listicle, focus_keyword_input, selected_year_number_descr, selected_month_number_descr, special_info_template, urlaubsart_input, lang_wanted)
        #generate title tag
        title_tag_generated, title_tag_generated_cost, title_tag_generated_gptversion = gptapi.openAI_content(act_as_prompt_title, content_prompt_title, gpt_temp_wanted, gpt_version_wanted_title)

        title_tag_generated_length = len(title_tag_generated)
        if 40 < title_tag_generated_length < 50:
            title_tag_length_ok = "⚠️ - A bit too short. One could manually add another word here."
        elif 60 < title_tag_generated_length < 70:
            title_tag_length_ok = "⚠️ - may not be displayed in its entirety. No make-or-break issue."
        elif 51 < title_tag_generated_length < 61:
            title_tag_length_ok = "✅ - Length works perfectly fine."
        else:
            title_tag_length_ok = "❌ - too long/short. Please clear the cache (press 'C') and regenerate."
        
        #generate meta description
        descr_tag_generated, descr_tag_generated_cost, descr_tag_generated_gptversion = gptapi.openAI_content(act_as_prompt_descr, content_prompt_descr, gpt_temp_wanted, gpt_version_wanted_descr)

        descr_tag_generated_length = len(descr_tag_generated)
        if 130 < descr_tag_generated_length < 150:
            descr_tag_length_ok = "⚠️ - A bit too short. One could manually add another word here."
        elif 160 < descr_tag_generated_length < 165:
            descr_tag_length_ok = "⚠️ - may not be displayed in its entirety. No make-or-break issue."
        elif 151 < descr_tag_generated_length < 161:
            descr_tag_length_ok = "✅ - Length works perfectly fine."
        else:
            descr_tag_length_ok = "❌ - too long/short. Please clear the cache (press 'C') and regenerate."

        #generate h1 heading
        h1_tag_generated, h1_tag_generated_cost, h1_tag_generated_gptversion = gptapi.openAI_content(act_as_prompt_h1, content_prompt_h1, gpt_temp_wanted, gpt_version_wanted_h1)

        st.divider()
        st.subheader("Results")
        st.markdown(f"""<h4>Title Tag for {focus_keyword_input}</h4>
                    <ul>
                    <li>{title_tag_generated}</li>
                    <li><b>Length:</b> {title_tag_generated_length}</li>
                    <li><b>Length-Check:</b> {title_tag_length_ok}</li>
                    </ul>
                    <h4>Meta Description for {focus_keyword_input}</h4>
                    <ul>
                    <li>{descr_tag_generated}</li>
                    <li><b>Length:</b> {descr_tag_generated_length}</li>
                    <li><b>Length-Check:</b> {descr_tag_length_ok}</li>
                    </ul>         
                    <h4>H1 Headline for {focus_keyword_input}</h4>
                    <ul>
                    <li>{h1_tag_generated}</li>
                    </ul>
       
                    """, unsafe_allow_html=True)
        st.divider()

        #####################
        total_cost_tnd = (
            title_tag_generated_cost +
            descr_tag_generated_cost +
            h1_tag_generated_cost
        )
        total_cost_tnd = round(total_cost_tnd, 5)

        additional_infos_title_tag =  " ".join(filter(None, [selected_year_number_title, selected_month_number_title, selected_emoji_title]))
        additional_infos_descr_tag =  " ".join(filter(None, [selected_year_number_descr, selected_month_number_descr, selected_emoji_descr]))
        
        special_info_template_str = str(special_info_template)
        additional_usage_information = ",".join(filter(None, [tnd_template_choice, special_info_template_str]))

        bq.to_bigquery("TND Generator", total_cost_tnd, focus_keyword_input, additional_usage_information, lang_wanted)

    ## Template Input - z.B. "Sehenswürdigkeiten" hat ne eigene Struktur, "Urlaubsziele Seite" hat ne eigene Struktur etc.
    ## Hier Input zum Fokus Keyword / Main Keyword, z.B. "Aktivitäten Amsterdam", steht dann ganz vorne im Title
    # Input für Jahreszahl - falls leer nicht berücksichtigen
    # Input für Monat - falls leer nicht berücksichtigen
    # Gewünschtes Emoji im Title - wenn leer, dann nicht berücksichtigen
    # Gewünschtes Emoji in der Meta Descrption - wenn leer, nicht berücksichtigen

    ### Hier folgen die Generation Felder

    ### Hier werden die Informationen angezeigt

    
