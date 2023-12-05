import streamlit as st
from bs4 import BeautifulSoup
import requests

#functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.gptapi as gptapi
import functions.bigquery as bq

###
travel_deals_list = [
    "Exclusive Offer",
    "Discount Promotion",
    "Flash Sale",
    "Voucher / Multi-voucher",
    "Price Buster",
    "Swim Up Room",
    "Family Offer",
    "with Admission Ticket (Musical, Event, etc.)",
    "Round Trip",
    "with Ski Pass",
    "Villa",
    "Chalet",
    "Junior Suite",
    "Grand Opening",
    "New Year's Eve",
    "Many Dates",
    "During the Holidays",
    "Wellness",
    "Sea View",
    "Luxury",
    "Directly by the Lake",
    "Award-winning Hotel",
    "Weekend Getaway",
    "Castle Hotel",
    "with Direct Flights"
]


def generate_product_description(gpt_version_wanted, gpt_temp_wanted, lang_wanted):
    st.title("Deal* intro text generation")
    st.subheader("Generate content for any given deal page.")
    st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
    st.markdown("""<ul>
                <li>Fill in the boxes below and provide additional informations.</li>
                <li>Click on the button "Generate deal content" to generate content via GPT.</li>
                <li><i>*We are well aware, that deal is not the correct wording.</i></li>
               </ul>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("**Do you want to include a voucher?**")
    voucher_selected = st.checkbox("Include voucher", key = "checkbox_voucher_selected")
    with st.form(key = "input fields for deal content generation"):
        st.markdown("<h4>Provide informations</h4>", unsafe_allow_html=True)
        

        col1_deal_content, col2_deal_content = st.columns(2)
        with col1_deal_content:
            st.markdown("**Tone of voice**")
            headline = st.text_input("Whats the overall topic of the deal? (E.g. Wellness in Dutch)", key = "headline_deals")
            vorteilskommunikation = st.text_input("Communication of benefits (e.g. New Openings, Last Minute Offer, Luxury Hotel,...)", key = "deals_comm_of_benefits_input")
            exlusiv_angebot = st.selectbox("Select special exclusive offers", travel_deals_list, key = "deals_special_offers_input")
            angebotsdetails = st.text_area("Provide details about the offer (e.g. how many nights etc.)")
            emojis_wanted = st.checkbox("Include Emojis in content", key = "checkbox_emojis")
            
        with col2_deal_content:
            if voucher_selected == True:
                st.markdown("**Voucher Informations**")
                gutscheincode = st.text_input("Voucher Code", key = "deals_voucher_code")
                einloesezeitraum_start = st.date_input("Start redemption period", key = "deals_start_zeitraum")
                einloesezeitraum_ende = st.date_input("End redemption period", key = "deals_ende_zeitraum")
                mindestbestellwert = st.text_input("Minimum order value", key = "deals_min_value")
                gueltig_bis = st.text_input("Validity", key = "deals_gueltig_bis")
        form_submit_input_field_for_deal_content = st.form_submit_button(label="Generate content")

    st.divider()


    if form_submit_input_field_for_deal_content:
        # gpt prompt generation
        if voucher_selected == True:
            product_content_prompt, product_act_as_prompt, product_headline_prompt, product_description_prompt, product_h1_prompt, product_subheader_prompt = gptprompts.product_text_prompt_with_voucher(lang_wanted, angebotsdetails, emojis_wanted, headline, vorteilskommunikation, exlusiv_angebot, gutscheincode, einloesezeitraum_start, einloesezeitraum_ende, mindestbestellwert, gueltig_bis)
        
        elif voucher_selected == False:
            product_content_prompt, product_act_as_prompt, product_headline_prompt, product_description_prompt, product_h1_prompt, product_subheader_prompt= gptprompts.product_text_prompt(lang_wanted, angebotsdetails, emojis_wanted, headline, vorteilskommunikation, exlusiv_angebot)


        # gpt api calling
        product_content, product_content_cost, product_content__gptversion = gptapi.openAI_content(product_act_as_prompt, product_content_prompt, gpt_temp_wanted, gpt_version_wanted)
        product_headline, product_headline_cost, product_headline_gptversion = gptapi.openAI_content(product_act_as_prompt, product_headline_prompt, gpt_temp_wanted, gpt_version_wanted)
        product_description, product_description_cost, product_description_gptversion = gptapi.openAI_content(product_act_as_prompt, product_description_prompt, gpt_temp_wanted, gpt_version_wanted)
        product_h1, product_h1_cost, product_h1__gptversion = gptapi.openAI_content(product_act_as_prompt, product_h1_prompt, gpt_temp_wanted, gpt_version_wanted)
        product_subheader, product_subheader_cost, product_subheader_gptversion = gptapi.openAI_content(product_act_as_prompt, product_subheader_prompt, gpt_temp_wanted, gpt_version_wanted)


        col1_result, col2_result = st.columns(2)
        with col1_result:

            st.subheader("Headline")
            st.write(product_h1)

            st.subheader("Sub-Headline")
            st.write(product_subheader)

        with col2_result:
            st.subheader("Google Title & Description Tag")
            st.markdown("**Google Title Tag**")
            st.write(product_headline)
            st.markdown("**Google Meta Description**")
            st.write(product_description)
        
        st.divider()
        st.subheader("Deal Description")
        st.write(product_content)
        st.divider()
        
        ### push cost to google big query
        total_cost_product_content_generator = product_content_cost + product_headline_cost + product_description_cost + product_h1_cost + product_subheader_cost
        bq.to_bigquery("Product Content Generator", total_cost_product_content_generator, headline, vorteilskommunikation, lang_wanted)



