import streamlit as st
import prompts.prompts as gptprompts
import functions.bigquery as bq
import functions.gptapi as gptapi



def about():
    st.title("Urlaubsguru GTP-Web-App")
    st.markdown("<h3>Cost overview for the current month</h3>", unsafe_allow_html=True)
    if st.button("Query costs"):
        current_cost_for_this_month = bq.fetch_total_cost_current_month()
        
    st.divider()
    with st.expander("Glossary (click to expand)"):
        st.subheader("Glossary")
        st.markdown("""<ul>
                    <li><b><u>Temperature</u></b>: Temperature is a parameter that controls the creativity of the language model (GPT4). The higher the temperature (0.1 - 1), the more diverse and creative the output. The lower the temperature, the more reproducible and focused the output.</li>
                    <li><b><u>Top_p</u></b>: Language models select the order of words according to the frequency with which they occur in the training data. Thus, in the context of a sentence or a word, the 'next most likely' word is always selected. The top_p value now controls whether only the top 10% (top_p = 0.1) should be used or whether a larger data pool should be fished (top_p = 0.5 correspond to the top 50%).</li>
                    </ul>""", unsafe_allow_html=True)
    
    with st.expander("Generic GPT-Settings Overview (Click to expand)"):
        st.subheader("General GPT-4 settings")
        st.markdown("<p>GPT-4 has been fine-tuned for Creative Writing.</p>", unsafe_allow_html=True)
        st.markdown("""<ul>
                    <li><b><u>Temperature</u></b>: 0.7</li>
                    <li><b><u>Top_p</u></b>: 0.8</li></ul>
                    <p>GPT now generates creative and diverse content made for storytelling. The output is exploratory and adheres less to existing patterns from the training data.</p>""", unsafe_allow_html=True)
    st.divider()
    ############################################################################################################################################################
    st.subheader("Find all prompts here")
    with st.expander("Titles & Description Generator: Prompts (click to expand)"):
        st.subheader("Titles & Description Generator: Prompts")
        ### code für prompts
        listicle_act_as_prompt_title, listicle_content_prompt_title = gptprompts.title_tag_prompt("Inspirational: Top-10-Article", 10, "Amsterdam", "2024", "", "🔥", "", "Sehenswürdigkeiten", "Deutsch")
        listicle_act_as_prompt_descr, listicle_content_prompt_descr = gptprompts.meta_description_prompt("Inspirational: Top-10-Article", 15, "Amsterdam", "2024", "Jänner", "🔥", "Anne Frank Haus, Van Gogh Museum, Rijksmuseum", "Sehenswürdigkeiten", "Deutsch")

        st.markdown(f"""<h5>Prompts for the template "Inspirational: Top 10 Articles"</h5>
                    <h6>Title Tag Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {listicle_act_as_prompt_title}</li>
                    <li><b><u>Additional informations:</u></b> Current year, listicle contains 15 content elements, the 🔥-emoji, the focus keyword "sights of Amsterdam</li>
                    <li><b><u>Content Prompt:</u></b> {listicle_content_prompt_title}</li>
                    </ul>
                    <br>
                    <h6>Meta Descr. Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {listicle_act_as_prompt_descr}</li>
                    <li><b><u>Additional informations:</u></b> Aktuelle Jahreszahl, das 🔥-Emoji.</li>
                    <li><b><u>Content Prompt:</u></b> {listicle_content_prompt_descr}</li><br><br></ul>            
                    """, unsafe_allow_html=True)

        deal_act_as_prompt_title, deal_content_prompt_title = gptprompts.title_tag_prompt("Transactional: Deals", 0, "Santorini", "", "", "🔥", "4 Tage im 5 Sterne Hotel mit Frühstück & einer Duplex Suite", "Wochenendtrip", "Deutsch")
        deal_act_as_prompt_descr, deal_content_prompt_descr = gptprompts.meta_description_prompt("Transactional: Deals", 0, "Santorini", "", "", "🔥", "4 Tage im 5 Sterne Hotel mit Frühstück & einer Duplex Suite", "Wochenendtrip", "Deutsch")

        st.markdown(f"""<h5>Prompts for the "Transactional: Offers" template</h5>
                    <h6>Title Tag Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {deal_act_as_prompt_title}</li>
                    <li><b><u>Additional informations:</u></b> The deal has the special feature: "4 days in a 5 star hotel with breakfast & a duplex suite", the 🔥-Emoji</li>
                    <li><b><u>Content Prompt:</u></b> {deal_content_prompt_title}</li>
                    </ul>
                    <br>
                    <h6>Meta Descr. Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {deal_act_as_prompt_descr}</li>
                    <li><b><u>Additional informations:</u></b> The deal has the special feature: "4 days in a 5 star hotel with breakfast & a duplex suite", the 🔥-Emoji</li>
                    <li><b><u>Content Prompt:</u></b> {deal_content_prompt_descr}</li><br><br></ul>                
                    """, unsafe_allow_html=True)
        
        
        uz_act_as_prompt_title, uz_content_prompt_title = gptprompts.title_tag_prompt("Transactional: Destination", 0, "Santorini", "2024", "", "🔥", "", "Pauschalreise", "Deutsch")
        uz_act_as_prompt_descr, uz_content_prompt_descr = gptprompts.meta_description_prompt("Transactional: Destination", 0, "Santorini", "2024", "", "🔥", "", "Pauschalreise", "Deutsch")

        st.markdown(f"""<h5>Prompts for template "Transactional: Destination"</h5>
                    <h6>Title Tag Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {uz_act_as_prompt_title}</li>
                    <li><b><u>Additional informations:</u></b> Year "2024", the emoji "🔥" and the holiday type "package holiday</li>
                    <li><b><u>Content Prompt:</u></b> {uz_content_prompt_title}</li>
                    </ul>
                    <br>
                    <h6>Meta Descr. Prompts</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {uz_act_as_prompt_descr}</li>
                    <li><b><u>Additional informations:</u></b> Year "2024", the emoji "🔥" and the holiday type "package holiday</li>
                    <li><b><u>Content Prompt:</u></b> {uz_content_prompt_descr}</li>                
                    """, unsafe_allow_html=True)
        
    ############################################################################################################################################################
    with st.expander("Generate new sights content: Prompts overview (click to expand)"):
        st.subheader("Expand sights: Prompts")
        ### code für Prompts ###
        act_as_prompt_sights, structure_prompt_sights = gptprompts.sight_prompts(3, "Amsterdam", "Anne Frank Haus", "Deutsch")
        content_prompt_new_sight, content_pic_prompt = gptprompts.new_sight_prompt("150", "Anne Frank Haus", "Amsterdam", "Deutsch")
        oeffnungszeiten_prompt = gptprompts.oeffnungszeiten_prompt("Deutsch")
        eintrittskosten_prompt = gptprompts.eintrittskosten_prompt("Deutsch")
        st.markdown(f"""<ul>
                    <li><b><u>System Prompt:</u></b> {act_as_prompt_sights}</li>
                    <li><b><u>Sample structure prompt:</u></b> {structure_prompt_sights}</li>
                    <li><b><u>Exemplary prompt for each new sight:</u></b> {content_prompt_new_sight}</li>
                    <li><b><u>Sample prompt for a picture tip of the new sight:</u></b> {content_pic_prompt}</li>
                    <li><b><u>Prompt for summary of opening hours:</u></b> {oeffnungszeiten_prompt}</li>
                    <li><b><u>Prompt for the summary of admission prices:</u></b> {eintrittskosten_prompt}</li>
                    </ul>""", unsafe_allow_html=True)
    ############################################################################################################################################################
    with st.expander("Generate new beaches content: Prompts overview (click to expand)"):
        st.subheader("Expand beaches: Prompts")
        ### code für Prompts ###
        act_as_prompt_beach, structure_prompt_beach = gptprompts.beach_prompts(3, "Griechenland", "Elafonisi Strand", "Deutsch")
        content_prompt_new_beach = gptprompts.new_beach_prompt("100", "Simos Strand", "Griechenland", "Deutsch")
        st.markdown(f"""<ul>
                    <li><b><u>System Prompt:</u></b> {act_as_prompt_beach}</li>
                    <li><b><u>Sample structure prompt:</u></b> {structure_prompt_beach}</li>
                    <li><b><u>Exemplary prompt for each new beach:</u></b> {content_prompt_new_beach}</li>
                    </ul>""", unsafe_allow_html=True)
    ############################################################################################################################################################
    with st.expander("Generate new headlines and content: Prompts overview (click to expand)"):
        st.subheader("New headlines and content: Prompts")
        ### code für promots ###
        act_as_prompt_headline_content, content_prompt_headline_content = gptprompts.content_for_headline_prompt("Deutsch", "Sizilien für Singles: So erlebt ihr einen unvergesslichen Solo-Trip", 100, "")
        act_as_prompt_summary, content_prompt_summary = gptprompts.create_summary("Deutsch", "Wenn ihr denkt, dass Reisen nur für Paare oder Gruppen ist, dann liegt ihr falsch. Solo-Reisen sind auf dem Vormarsch und Sizilien ist ein perfekter Ort für eure erste oder nächste Solo-Tour. Sizilien ist mehr als nur eine italienische Insel; es ist eine bunte Mischung aus Kulturen, Landschaften und Aromen, die ihr alleine in eurem eigenen Tempo erkunden könnt. Sizilien für Singles ist nicht nur eine Möglichkeit, sondern eine fantastische Erfahrung, die euch die Möglichkeit gibt, euch selbst besser kennenzulernen, neue Freunde zu finden und eine andere Kultur zu entdecken.")
        act_as_prompt_headlines, content_prompt_headlines = gptprompts.headline_structure_prompt("Deutsch", 15, "Bookings", "Leute mitte 30, die ein eigenes Ferienhaus mieten wollen. Teilweise auch mit Familie. Schätzen es sehr, dass es nicht so touristisch ist. Gehen auch gerne wandern.", "Urlaub Sizilien", "Transactional")
        
        st.markdown(f"""
                    <h6>Headline Generation Prompt</h6>
                    <ul>
                    <li><b><u>System Prompt:</u></b> {act_as_prompt_headlines}</li>
                    <li><b><u>Exemplary prompt for a new headline:</u></b> {content_prompt_headlines}</li>
                    </ul>
                    <br>
                    <h6>Headline Content Prompts</h6>
                                       <ul>
                    <li><b><u>System Prompt:</u></b> {act_as_prompt_headline_content}</li>
                    <li><b><u>Exemplary prompt for content of a new headline:</u></b> {content_prompt_headline_content}</li>
                    </ul><br>
                    <h6>Content Summary Prompts</h6>
                   <ul>
                    <li><b><u>System Prompt:</u></b> {act_as_prompt_summary}</li>
                    <li><b><u>Exemplary prompt for summary of all the content:</u></b> {content_prompt_summary}</li>
                    </ul>

                    </ul>""", unsafe_allow_html=True)
    ############################################################################################################################################################
    with st.expander("Generate summaries from content pieces: Prompts overview (click to expand)"):
        st.markdown(f"""<h6>Generic Prompt</h6>
                    <ul>
                    <li>Antworte mir Deutsch. Erstelle mir eine Zusammenfassung. Nutze diese Art der Zusammenfassung: 'Beispiel'. Inhalt: 'Scraping Resultat'</li>
                    </ul>
                    <br>
                    <h6>Types of Summary Types</h6>
                    <ul>
                    <li><b>Most important informations:</b> Fasse mir den Text als Informative Zusammenfassung zusammen und konzentriere dich auf die Übertragung der wichtigsten Informationen aus dem Text. Sei sachlich und stelle die Fakten klar dar. Kommuniziere mir Daten und Fakten. </li>
                    <li><b>Very short with key aspects:</b> Fasse mir den Text kurz und knapp als Kurze Zusammenfassung zusammen. Konzetriere dich auf das absolute Minimum an Informationen, um den Hauptpunkt des Textes zu vermitteln. Kommuniziere mir Daten und Fakten.</li>
                    <li><b>Focus on broader topics:</b> Hebe die Hauptthemen und Konzepte des Textes hervor. Ignoriere dabei die Details. Ich möchte mich auf die großen Ideen konzentrieren. </li>
                    <li><b>Chronological summary:</b> Fasse die Reihenfolge von Ereignissen oder Informationen im Text zusammen mittels Chronologischer Zusammenfassung.  Kommuniziere mir Daten und Fakten.</li>
                    <li><b>Facts focused:</b> Fasse den Text mittels Statistischer Zusammenfassung zusammen. Hebe statistische Daten oder Fakten aus dem Text hervor.  Kommuniziere mir Daten und Fakten.</li>
                    </ul>
                    """, unsafe_allow_html=True)
    ############################################################################################################################################################
    with st.expander("Generate alt text: Prompts overview (click to expand)"):
        st.subheader("Alt Text Prompts")
        alt_text_prompt = gptprompts.alt_tag_prompts("Deutsch", "https://mediafiles.urlaubsguru.de/wp-content/uploads/2022/03/Museum-Square-in-the-borough-Amsterdam-South_shutterstock_245364502.jpg", "Sehenswürdigkeiten Amsterdam")
        st.markdown(f"""<h6>Generate alt text prompt</h6>
                    <ul>
                    <li><b>Language:</b> Deutsch</li>
                    <li><b>Image URL:</b> https://mediafiles.urlaubsguru.de/wp-content/uploads/2022/03/Museum-Square-in-the-borough-Amsterdam-South_shutterstock_245364502.jpg</li>
                    <li><b>Topic selected:</b> Sehenswürdigkeiten Amsterdam</li>
                    </ul>
                    <br>
                    <h6>Final prompt</h6>
                    <p>{alt_text_prompt}</p>
                    """, unsafe_allow_html=True)
