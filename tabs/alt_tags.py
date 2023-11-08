import streamlit as st
from bs4 import BeautifulSoup
import requests

#functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.gptapi as gptapi
import functions.bigquery as bq


def generate_alt_text(gpt_version_wanted, gpt_temp_wanted, gpt_top_p_wanted, lang_wanted):
    st.title("Alt Text Generator")
    st.subheader("Inspiration for alternative text for any given picture")
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("""<ul>
                <li>Right-Click the uploaded picture and copy the picture URL.</li>
                <li>Paste the image URL in the given input field.</li>
                <li>Provide context in form of the focus keyword: In which topic is this picture embedded?</li>
                <li>Click on the button "Generate Alt Text" to generate the respective tags via GPT.</li>
               </ul>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("<h4>Provide informations</h4>", unsafe_allow_html=True)

    col1_alt_text, col2_alt_text = st.columns(2)

    with col1_alt_text:
        alt_text_generation_method_choice = st.radio("Choose the alt text generation method:", ["Single image", "Bulk image"])
    
    with col2_alt_text:
        if alt_text_generation_method_choice == "Single image":
            url = st.text_input("Paste image URL here...", key="alt_text_image_url_inputfield")
        elif alt_text_generation_method_choice == "Bulk image":
            url = st.text_input("Paste article URL here...", key="alt_text_image_url_inputfield")
        image_context = st.text_input("Whats the main topic of the content piece, where the picture is embedded?", key="input_field_focus_keyword_alt_text")

    st.divider()    

    if st.button("Generate alt text for image"):
        if alt_text_generation_method_choice == "Bulk image":
            r = requests.get(url)
            soup = BeautifulSoup(r.text, "lxml")
            soup = BeautifulSoup(r.text, 'html.parser')
            figure_tags = soup.find_all('figure')
            href_urls = []
            for figure_tag in figure_tags:
                a_tag = figure_tag.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    href_url = a_tag['href']
                    href_urls.append(href_url)
                else:
                    st.warning("No images found.")

            # Print the extracted href URLs
            alt_text_generated_cost_list = []
            for image_url in href_urls:
                #prompt generation
                content_prompt_alt = gptprompts.alt_tag_prompts(lang_wanted, image_url, image_context)
                #generate content
                alt_text_generated, alt_text_generated_cost, alt_text_generated_gptversion = gptapi.openAI_vision(content_prompt_alt, image_url)
                st.markdown("**Image URL**")
                st.write(image_url)
                st.markdown("**Alt Text:**")
                st.write(alt_text_generated)
                alt_text_generated_cost_list.append(alt_text_generated_cost)
                st.divider()
            alt_text_generated_cost_total = sum(alt_text_generated_cost_list)
            bq.to_bigquery("Alt Text Generator", alt_text_generated_cost_total, alt_text_generation_method_choice, image_context, lang_wanted)

        elif alt_text_generation_method_choice == "Single image":
            image_url = url
            content_prompt_alt = gptprompts.alt_tag_prompts(lang_wanted, image_url, image_context)
            alt_text_generated, alt_text_generated_cost, alt_text_generated_gptversion = gptapi.openAI_vision(content_prompt_alt, image_url)
            st.markdown("**Image URL:**")
            st.write(image_url)
            st.markdown("**Alt Text:**")
            st.write(alt_text_generated)
            st.divider()
            bq.to_bigquery("Alt Text Generator", alt_text_generated_cost, alt_text_generation_method_choice, image_context, lang_wanted)





