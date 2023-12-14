import streamlit as st

def sidebar():
    st.image("https://mediafiles.urlaubsguru.de/wp-content/uploads/2023/06/Logo_UG_mit-claim.png")
    st.title("GPT-Tool")
    st.markdown("<p>Welcome to the Urlaubsguru GPT-Tool.</p>", unsafe_allow_html=True)
    st.markdown("<h3>General information:</h3>", unsafe_allow_html=True)
    st.markdown("<ul><li>Tools are located in the tabs on the main screen.</li><li>GPT settings can be made in the sidebar. These then apply to all tools.</li><li><b>Beware:</b> Selection of new parameters via input fields resets already queried data.</li></ul>", unsafe_allow_html=True)
    st.divider()
    st.markdown("<h4>Language Settings</h4><p>Please select the desired language for your GPT output.</p>", unsafe_allow_html=True)
    lang_wanted = st.selectbox("Language", ["german", "english", "dutch", "spanish"])
    if lang_wanted == "german":
        lang_wanted = "Deutsch"
    elif lang_wanted == "spanish":
        lang_wanted = "Spanisch"
    elif lang_wanted == "dutch":
        lang_wanted = "Holländisch"
    elif lang_wanted == "english":
        lang_wanted = "Englisch"
    st.divider()
    st.markdown("<h4>GPT Settings</h4><p>Glossary can be found within 'About'-section</p>", unsafe_allow_html=True)
    gpt_version_wanted = st.selectbox("GPT Version", ["GPT-4", "GPT-3.5"])
    if gpt_version_wanted == "GPT-4":
        gpt_version_wanted = "gpt-4-1106-preview"
    elif gpt_version_wanted == "GPT-3.5":
        gpt_version_wanted = "gpt-3.5-turbo-1106"
        
    gpt_temp_wanted = st.slider("Temperatur - Standard: 0.5", 0.09, 1.0, 0.7, key = "sidebar slider gtp temp")

    st.divider()
    st.markdown("<h3>Kontakt</h3><p>If you have any questions, requests or comments, please contact the Inbound Marketing Team:</p><ul><li><a href='https://teams.microsoft.com/l/channel/19%3a72197b1f3177425aba225726ec4f2f5f%40thread.skype/Inbound%2520Automation?groupId=1da7e5cc-703e-4d39-8dac-4b5a723173a4&tenantId=5f4d3a64-cc9f-49a2-be2d-41ac01dba2dd'>Inbound Marketing Automation Teams Channel</a></li><li><a href='mailto:paul.herzog@urlaubsguru.de'>E-Mail</a></li>", unsafe_allow_html=True)
    st.divider()

    return gpt_version_wanted, gpt_temp_wanted, lang_wanted