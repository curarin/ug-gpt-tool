## Titles und Description Prompts
# mit Nachfolgendem Prompt werden Title Tags generiert
# Hinweis: Je nach ausgewähltem Template sind die Prompts etwas unterschiedlich
# Das Template "Top 10 Artikel" soll beispielsweise ein Listicle wiederspiegeln und die individuellen Charakteristika
# Das Template "Deals" soll dabei die Redakteur:innen anleiten einen Longtail zu formen, indem spezifische Informationen noch angegeben werden

def title_tag_prompt(template, number_of_elements_for_listicle, focus_destination, jahreszahl, aktueller_monat, emoji, special_info_template, urlaubsart_input, lang_wanted):
    act_as_prompt = f"Antworte auf {lang_wanted}. Du bist SEO Spezialist für ein Reiseunternehmen. Verfasse einen Google Title Tag mit maximal 60 Zeichen. Halte dich exakt an diese Längenvorgabe. Das Fokus Keyword ({urlaubsart_input} {focus_destination}) steht am Anfang. Inkludiere folgende Informationen: {jahreszahl}, {aktueller_monat} {emoji}. Du bist mit den Leserinnen Per Du. Wir sprechen von uns als 'Wir'."
    if template == "Inspirational: Top-10-Article":    
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse nach dem vorgegebenen Schema einen Title Tag. Der Title muss mit 'Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination}' beginnen. Benutze am Ende einen emotionalen Trigger um Klickattraktivität zu erhöhen."
    elif template == "Transactional: Deals":
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse einen Title Tag nach dem vorgegebenem Schema, der besonderes Augenmerk auf die Besonderheit {special_info_template} legt. Das muss vorhanden sein. Am Anfang soll außerdem stehen: {urlaubsart_input} {focus_destination}."
    elif template == "Transactional: Destination":
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse einen Title Tag nach dem vorgegebenem Schema. Am Anfang soll stehen: {urlaubsart_input} {focus_destination}. Nutze anschließend einen Emotionalen Trigger, der die Reiselust für {focus_destination} wecken soll."
    return act_as_prompt, content_prompt

def meta_description_prompt(template, number_of_elements_for_listicle, focus_destination, jahreszahl, aktueller_monat, emoji, special_info_template, urlaubsart_input, lang_wanted):
    act_as_prompt = f"Antworte auf {lang_wanted}. Du bist SEO Spezialist für ein Reiseunternehmen. Verfasse eine Google Meta Description mit maximal 155 Zeichen. Halte dich exakt an diese Längenvorgabe. Erhöhe die Klickattraktivität, indem du einen natürlichen emotionalen Trigger einbaust. Inkludiere folgende Informationen: {jahreszahl}, {aktueller_monat} {emoji}. Du bist mit den Leserinnen Per Du. Wir sprechen von uns als 'Wir'."
    if template == "Inspirational: Top-10-Article":
        content_prompt = f"Antworte auf {lang_wanted}. Schreibe Top-{number_of_elements_for_listicle} {urlaubsart_input} {focus_destination} zu Beginn. Nutze wenn vorhanden dieses Emoji: {emoji}. Wenn nicht vorhanden suche ein passendes. Erwähne dann die Top Themen ({special_info_template}) in diesem Format: 1. A 2. B 3. C. Ersetze A B C durch die Top Themen aus der Liste. Erwähne außerdem {jahreszahl}, {aktueller_monat}. Am Ende ein emotionaler Call to Action."
    elif template == "Transactional: Deals":
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse eine Google Meta Description nach dem vorgegebenem Schema. Die Description soll den User am Anfang mit seinem Bedürfnis abholen, dass er hat wenn er nach '{urlaubsart_input} {focus_destination}' sucht, danach kommunizierst du {special_info_template}. Achte auf Emotionalität. Die Google Meta Description soll die Vorfreude auf das Angebot wecken und zum kaufen verleiten. Am Ende soll ein Call to Action folgen, der Buchungsinteresse wecken soll."
    elif template == "Transactional: Destination":
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse eine Google Meta Description nach dem vorgegebenem Schema. Die Description soll den User am Anfang mit seinem Bedürfnis abholen, dass er hat wenn er nach '{urlaubsart_input} {focus_destination}' sucht. Nutze anschließend ein ➡️ Emoji und erwähne ein paar Besonderheiten, die einen Urlaub in {focus_destination} so außergewöhnlich machen. Anschließend einen Call to Action, der zum Buchen verleiten soll."
    return act_as_prompt, content_prompt

## Sehenswürdigkeiten Prompts
# Mit nachfolgendem Prompt werden neue Sehenswürdigkeiten genannt, welche bis dato noch nicht im Artikel behandelt werden
def sight_prompts(number_of_sights_wanted, destination_wanted, sights_not_needed, lang_wanted):
    act_as_prompt_sights = f"Antworte auf {lang_wanted}. Du bist eine reisebegeisterte und erfahrene Redakteurin mit SEO-Fokus und Reiseexpertin. Die Sätze werden informativ und mit einer sehr attraktiven Bildsprache verfasst. Die Sätze sind nicht zu kompliziert formuliert, gerne werden beschreibende Adjektive genutzt. Die Redakteurin nutzt präzise Beschreibungen und eine enthusiastische Art der Erzählung um dem Leser dabei helfen, sich gut beraten zu fühlen und eine Entscheidung für ein Reiseziel oder für die Buchung eines konkreten Angebots zu treffen."
    structure_prompt_sights = f"Antworte auf {lang_wanted}. Nenne mir exakt {number_of_sights_wanted} Sehenswürdigkeiten, die man in {destination_wanted} abseits von {sights_not_needed} unbedingt gesehen haben? Antworte mit einer Python Liste der Sehenswürdigkeiten. Inkludiere keinerlei Erklärungen."
    return act_as_prompt_sights, structure_prompt_sights

# Mit nachfolgendem Prompt wird der beschreibende Text sowie der Bild-Tipp für jede neue Sehenswürdigkeit generiert
def new_sight_prompt(content_length_wanted, new_sight, destination_wanted, lang_wanted):
    content_prompt_new_sight = f"Antworte auf {lang_wanted}. Erzähle etwas über {new_sight}. Was macht sie so besonders? Warum muss man als Tourist dort hin? Was zeichnet diese Sehenswürdigkeit aus im Vergleich zu anderen Sehenswürdigkeiten in {destination_wanted}? Erzähle auch historische Details. Du bist Per Du mit der Leserschaft. Du sprichst die Leserschaft im Plural an. Stelle sicher, dass der Text die Leser dazu ermutigt die Sehenswürdigkeit {new_sight} zu besuchen. Verzichte auf Floskeln."
    content_pic_prompt = f"Antworte auf {lang_wanted}. Schreibe maximal 50 Wörter: Was muss auf einem Bild für {new_sight} zu sehen sein, damit die Sehenswürdigkeit gut zur Geltung kommt und die Zielgruppe diese gerne besuchen möchte?"
    return content_prompt_new_sight, content_pic_prompt

## Scraping & Zusammenfasung Prompts
# Mit nachfolgendem Prompt wird GPT ein gescrapter Text geschickt und GPT soll die Öffnungszeiten extrahieren und zusammenfassen
def oeffnungszeiten_prompt(lang_wanted):
    prompt = "Antworte auf {lang_wanted}. Welche Öffnungszeiten gibt es auf Basis der Informationen die ich dir gebe? Halte dich ausschließlich an diese Informationen. Wenn du keine Informationen findest antworte mit 'No information found in provided URL.'"
    return prompt

# Mit nachfolgendem Prompt wird GPT ein gescrapter Text geschickt und GPT soll die Eintrittskosten extrahieren und zusammenfassen
def eintrittskosten_prompt(lang_wanted):
    prompt = "Antworte auf {lang_wanted}. Was kostet der Eintritt auf Basis der Informationen die ich dir gebe? Halte dich ausschließlich an diese Informationen. Wenn du keine Informationen findest antworte mit 'No information found in provided URL.'"
    return prompt


#### Headline Tab Prompts
def headline_structure_prompt(lang_wanted, nr_of_headlines_wanted, goal_choice, target_audience, target_topic, page_type):
    if goal_choice == "Brand Awareness":
        goal_choice = "Aufmerksamkeit für die Marke. Liebe entwickeln, interessante Themen den Usern beibringen. Vorfreude auf das Reisen aufbauen."
    elif goal_choice == "Bookings":
        goal_choice = "Reisebuchungen für unsere Produkte. Wir wollen Umsätze generieren und der Inhalt ist darauf optimiert."
    elif goal_choice == "After Sales / Service":
        goal_choice = "Kunden binden und halten. Wir wollen hier auf potenzielle Sorgen unserer eigenen Kunden noch besser eingehen um als Marke noch positiver wahrgenommen zu werden."

    act_as_prompt = f"Du bist SEO Spezialist für ein Reiseunternehmen. Du schreibst lange Artikel, die das gewünschte Thema ganzheitlich abdecken. Du beziehst verschiedene Aspekte mit ein. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch)."
    if page_type == "Inspirational":
        content_prompt = f"Antworte auf {lang_wanted}. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Überlege dir dabei ganz genau, welche Themen ein Artikel zu diesem Thema benötigt. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient der Inspiration und soll Vorfreude entwickeln. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
    elif page_type == "Informational":
        content_prompt = f"Antworte auf {lang_wanted}. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Überlege dir dabei ganz genau, welche Themen ein Artikel zu diesem Thema benötigt. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient der Information und soll faktisch korrekt sein. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
    elif page_type == "Transactional":
        content_prompt = f"Antworte auf {lang_wanted}. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient dem Verkauf von Reisen und soll folgende Aspekte beinhalten: {target_topic} nach Reisedauer (je nachdem was für diese {target_topic} von Deutschland aus Sinn ergibt), für verschiedene Reisegruppen (Paare, Familien, Singles), Reisetypen (Adventurer, Sightseeing, Erholung,...). Außerdem Top Unterkünfte sollen dabei sein. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
    return act_as_prompt, content_prompt

def content_for_headline_prompt(lang_wanted, headline, length_wanted, additional_informations):
    act_as_prompt = f"Du bist SEO Spezialist für ein Reiseunternehmen.  Du schreibst lange Artikel, die das gewünschte Thema ganzheitlich abdecken. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch)."
    content_prompt = f"Antworte auf {lang_wanted}. Verfasse einen Absatz mit {length_wanted} Wörtern für die Überschrift {headline}. Beachte außerdem {additional_informations}."
    return act_as_prompt, content_prompt

def create_summary(lang_wanted, content):
    act_as_prompt = f"Du bist SEO Spezialist für ein Reiseunternehmen.  Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch)."
    content_prompt = f"Antworte auf {lang_wanted}. Verfasse eine Zusammenfassung rund 100 Wörtern. Diese soll die Kernaspekte nochmal kurz und prägnant zusammenfassen und die Leser an die wichtigsten punkte erinnern. Schreibe eine Zusammenfassung für folgenden Text: {content}"
    return act_as_prompt, content_prompt


#### Beaches Prompts
def beach_prompts(number_of_beaches_wanted, destination_wanted, beaches_not_needed, lang_wanted):
    act_as_prompt_sights = f"Antworte auf {lang_wanted}. Du bist eine reisebegeisterte und erfahrene Redakteurin mit SEO-Fokus und Reiseexpertin."
    structure_prompt_sights = f"Antworte auf {lang_wanted}. Nenne mir exakt {number_of_beaches_wanted} Strände, die man in {destination_wanted} abseits von {beaches_not_needed} unbedingt gesehen haben? Antworte mit einer Python Liste der Sehenswürdigkeiten. Inkludiere keinerlei Erklärungen."
    return act_as_prompt_sights, structure_prompt_sights

def new_beach_prompt(content_length_wanted_beaches, beach, destination_wanted_for_beach, lang_wanted):
    content_prompt_new_sight = f"Antworte auf {lang_wanted}. Erzähle etwas über den Strand {beach}. Maximal {content_length_wanted_beaches} Worte. Was macht ihn so besonders? Warum muss man als Tourist dort hin? Was zeichnet diesen Strand aus im Vergleich zu anderen Stränden in {destination_wanted_for_beach}? Verwende malerische Sprache. Du bist Per Du mit der Leserschaft. Du sprichst die Leserschaft im Plural an. Stelle sicher, dass der Text die Leser dazu ermutigt {beach} zu besuchen."
    return content_prompt_new_sight


#### prompts für alt text

def alt_tag_prompts(lang_wanted, image_url, image_context):
    content_prompt_alt_text = f"Verfasse einen Alt Text für das Bild {image_url} in einem (1) Satz auf {lang_wanted}. {image_context} sollte vorkommen. Stelle dir vor, du möchtest einer sehbeeinträchgiten Person erklären, was auf dem Bild zu sehen ist im Kontext von {image_context}. Welche Elemente siehst du? Wo sind sie platziert? Welche Emotionen werden dabei geweckt? Schreibe nicht 'das Bild zeigt...' sondern beschreibe es direkt."
    return content_prompt_alt_text
