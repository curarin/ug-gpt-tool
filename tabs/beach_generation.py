#### import libraries
import streamlit as st
import json
import pandas as pd
import io

### functions from other files
import functions.gptapi as gptapi
import prompts.prompts as gptprompts
import functions.bigquery as bq

def dict_to_html_list(data):
    html = "<ul>"
    for key, value in data.items():
        html += f"<li>{key}: {value}</li>"
    html += "</ul>"
    return html


def beach_gen(gpt_version_wanted, gpt_temp_wanted, lang_wanted):
   st.title("Beach article generation")
   st.subheader("Generate an inspirational article about the top beaches")
   st.markdown("<h4>Instructions:</h4>", unsafe_allow_html=True)
   st.markdown("""<ul>
               <li>Enter the number of beaches you need information using the number slider.</li>
               <li>Enter the required word count per beach.</li>
               <li>Enter the destination for which beaches should be generated.</li>
               <li>Insert all currently existing beaches incase you already have an article about that. This ensures that these beaches are <b>not</b> generated explicitly.</li>
               <li>Click on the <b><u>Generate beaches</u></b> button.</li>
               <li>If necessary, all generated content can be downloaded as an Excel document.</li>
               </ul>""", unsafe_allow_html=True)

   #### Building Dataframe
   columns_for_new_beaches_df = [
      "name of beach",
      "description of beach"
   ]
   df_html_new_beaches = pd.DataFrame(columns=columns_for_new_beaches_df)

   ###Input Felder
   with st.form(key = "beach generation input fields"):
    st.markdown("<h4>Provide informations:</h4>", unsafe_allow_html=True)

    col1_sights_top_info, col2_sights_top_info = st.columns(2)
    with col1_sights_top_info:
        number_of_beaches_wanted = st.number_input("Number of beaches required", min_value=1, max_value=25, value=5, placeholder="Enter number of beaches...", key = "main number of beaches wanted input")    
        content_length_wanted_beaches = st.slider("Approximate number of words per beach", 200, 1500, 500, key = "main slider content length per beach")

        
    with col2_sights_top_info:
        destination_wanted_for_beach = st.text_input("Insert destination of beaches")
        beaches_not_needed = st.text_area("In case of update: Which beaches are currently mentioned? _Note: 1 sight = 1 line_")
        beaches_not_needed = [beaches_not_needed.strip() for beaches_not_needed in beaches_not_needed.split("\n")]
    form_submit_beaches_input_values = st.form_submit_button(label="Generate content")
   
   ### hier started der API Call

   st.divider()
   if form_submit_beaches_input_values:    
    ###GPT Prompts
    act_as_prompt_beach, structure_prompt_beach = gptprompts.beach_prompts(number_of_beaches_wanted, destination_wanted_for_beach, beaches_not_needed, lang_wanted)

    ### API Call
    top_beaches, top_beachess_cost = gptapi.openAI_json_response(structure_prompt_beach, lang_wanted)
    data = json.loads(top_beaches)
    # Get the first key dynamically
    first_key = list(data.keys())[0]
    # Access the values associated with the first key
    beaches_list_final = data[first_key]
    
    st.subheader("These beaches are going to be added:")
    st.write(beaches_list_final)
    
    ### Loop through sights and generate content
    beach_content_cost = []
    i = 0
    for beach in beaches_list_final:
       #### Print current state to App
       ### Sight GPT Prompts
       content_prompt_new_sight = gptprompts.new_beach_prompt(content_length_wanted_beaches, beach, destination_wanted_for_beach, lang_wanted)
   
       ### generate content
       new_beach_content, new_beach_content_cost, new_beach_content_gptversion = gptapi.openAI_content(act_as_prompt_beach, content_prompt_new_sight, gpt_temp_wanted, "ft:gpt-3.5-turbo-1106:urlaubsguru-gmbh::8X5sqhwW")
       beach_content_cost.append(new_beach_content_cost)


       #generate HTML
       data_html_for_new_beaches = {
          "name of beach": beach,
          "description of beach": new_beach_content,
       }
       df_to_append = pd.DataFrame([data_html_for_new_beaches])
       df_html_new_beaches = pd.concat([df_html_new_beaches, df_to_append], ignore_index=True)


       ### print to chat as list for easier copy-paste
       st.write(f"""
                <h5>{beach}</h5>
                <p>{new_beach_content}</p>
                """, unsafe_allow_html=True)

    
    ### Kosten berechnen
    total_beach_content_cost = sum(beach_content_cost)


    all_cost_beaches_update = (
       top_beachess_cost +
       total_beach_content_cost
       )
    all_cost_beaches_update = round(all_cost_beaches_update, 5)
    
    ### push to google bigquery
    number_of_sights_str = str(number_of_beaches_wanted)
    content_length_wanted_str = str(content_length_wanted_beaches)
    additional_usage_information = ",".join(filter(None, [number_of_sights_str, content_length_wanted_str]))
    bq.to_bigquery("Beaches Generator", all_cost_beaches_update, destination_wanted_for_beach, additional_usage_information, lang_wanted)


    st.divider()
    #### Implement Download button which caches the data
    st.subheader("Download of data")
    @st.cache_data
    def convert_df_to_excel(df):
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        excel_data = excel_buffer.getvalue()
        return excel_data
    new_beaches_excel = convert_df_to_excel(df_html_new_beaches)

    st.download_button("Download beach content as Excel-spreadsheet", data=new_beaches_excel, file_name=f"{destination_wanted_for_beach}_new_beaches.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.divider()
    #####################
    st.subheader("Recap of latest request")
    st.markdown(f"""
                <ul>
                <li><b>Choosen destination:</b> {destination_wanted_for_beach}</li>
                <li><b>Number of beaches:</b> {number_of_beaches_wanted}</li>
                <li><b>Cost:</b> {all_cost_beaches_update} USD</li>
                </ul>""", unsafe_allow_html=True)
