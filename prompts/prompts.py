## Titles und Description Prompts
# mit Nachfolgendem Prompt werden Title Tags generiert
# Hinweis: Je nach ausgewähltem Template sind die Prompts etwas unterschiedlich
# Das Template "Top 10 Artikel" soll beispielsweise ein Listicle wiederspiegeln und die individuellen Charakteristika
# Das Template "Deals" soll dabei die Redakteur:innen anleiten einen Longtail zu formen, indem spezifische Informationen noch angegeben werden

def title_tag_prompt(template, number_of_elements_for_listicle, focus_destination, jahreszahl, aktueller_monat, emoji, special_info_template, urlaubsart_input, lang_wanted):
    act_as_prompt = f"Du bist SEO in einem Reisemagazin. Du schreibst SEO Title Tags mit 65 Zeichen."
    if template == "Inspirational: List-Article":    
        content_prompt = f"Antworte auf {lang_wanted}. Verfasse einen Title Tag. Der Title muss mit 'Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination}' beginnen. Halte dich an die trainierten Vorgaben."
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Überlege dir die Antwort auf {lang_wanted}. Verfasse einen SEO Title Tag mit 65 Zeichen. Der Title muss mit 'Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination}' beginnen. Folge dabei dem Beispiel 'Top 15 Sehenswürdigkeiten in Wien', oder auf Spanisch '15 lugares que visitar en viena imprescindibles', oder auf Holländisch 'Bezienswaardigheden van wenen: Bekijk de top 12'. "
    elif template == "Transactional: Destination":
        content_prompt = f"Antworte auf {lang_wanted}. Erstelle einen SEO Title Tag für {urlaubsart_input} {focus_destination}. Falls vorhanden ergänze: {emoji} {aktueller_monat} {jahreszahl}"
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Überlege dir die Antwort auf {lang_wanted}. Verfasse einen SEO Title Tag mit 65 Zeichen. Der Title muss {urlaubsart_input} {focus_destination} beinhalten. Falls vorhanden ergänze: {emoji} {aktueller_monat} {jahreszahl}. Folge dem Beispiel 'Urlaub Mallorca 2024', oder auf Spanisch 'Viajes canarias 2024', oder auf Holländisch 'Griekenland vakantie 2024'."
    return act_as_prompt, content_prompt

def meta_description_prompt(template, number_of_elements_for_listicle, focus_destination, jahreszahl, aktueller_monat, emoji, special_info_template, urlaubsart_input, lang_wanted):
    act_as_prompt = f"Antworte auf {lang_wanted}. Du bist SEO Spezialist für ein Reiseunternehmen. Verfasse eine Google Meta Description mit maximal 155 Zeichen. HHalte dich an die trainierten Vorgaben."
    if template == "Inspirational: List-Article":
        if urlaubsart_input == "Sehenswürdigkeiten":
            content_prompt = f"Schreibe Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination} zu Beginn. Erwähne mit ✅-Emoji als Bulletpoint die Top Themen: {special_info_template}. Erwähne 'inkl. Guru-Touren von 1-4 Tagen'."
        elif urlaubsart_input == "Geheimtipps":
            content_prompt = f"Schreibe Top {number_of_elements_for_listicle} Geheimtipps {focus_destination} zu Beginn. Erwähne mit ✅-Emoji als Bulletpoint die Top Themen: {special_info_template}."
        else:
            content_prompt = f"Schreibe Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination} zu Beginn. Erwähne mit ✅-Emoji als Bulletpoint die Top Themen: {special_info_template}."
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Überlege dir die Antwort auf {lang_wanted}. Schreibe Top-{number_of_elements_for_listicle} {urlaubsart_input} {focus_destination} zu Beginn. Nutze wenn vorhanden dieses Emoji: {emoji}. Wenn nicht vorhanden suche ein passendes. Erwähne dann die Top Themen ({special_info_template}) in diesem Format: 1. A 2. B 3. C. Ersetze A B C durch die Top Themen aus der Liste. Erwähne außerdem {jahreszahl}, {aktueller_monat}. Am Ende ein emotionaler Call to Action."  
    elif template == "Transactional: Destination":
        content_prompt = f"Antworte auf {lang_wanted}. Erstelle eine Meta Description für {urlaubsart_input} {focus_destination}. Falls vorhanden ergänze: {emoji} {aktueller_monat} {jahreszahl} "
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Überlege dir die Antwort auf {lang_wanted}. Erstelle eine Meta Description mit maximal 155 Zeichen für {urlaubsart_input} {focus_destination}. Falls vorhanden ergänze: {emoji} {aktueller_monat} {jahreszahl}. Verwende am Ende eine Aufforderung / einen Call to Action, der die Leute auf die Buchung hinweist. Schreib Emotional. Sei mit den Lesern Per Du. Verwende keine Floskeln."
    return act_as_prompt, content_prompt

def h1_prompt(template, number_of_elements_for_listicle, focus_destination, jahreszahl, aktueller_monat, special_info_template, urlaubsart_input, lang_wanted):
    act_as_prompt = f"Du bist SEO Spezialist für ein Reiseunternehmen. Du schreibst Hauptüberschriften (H1) für einen Artikel. Halte dich an die trainierten Vorgaben."
    if template == "Inspirational: List-Article":
        content_prompt = f"Antworte auf {lang_wanted}. Schreibe eine H1 Headline für die Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination}."
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Erstelle eine H1 Überschrift für die Top {number_of_elements_for_listicle} {urlaubsart_input} {focus_destination}. Folge dabei dem Beispiel 'Top 15 Sehenswürdigkeiten in Wien', oder auf Spanisch '15 lugares que visitar en viena imprescindibles', oder auf Holländisch 'Bezienswaardigheden van wenen: Bekijk de top 12'."
    elif template == "Transactional: Destination":
        content_prompt = f"Antworte auf {lang_wanted}. Erstelle eine H1 Überschrift für {urlaubsart_input} {focus_destination}. Falls vorhanden ergänze: {aktueller_monat} {jahreszahl}"
        if lang_wanted == "Spanisch" or lang_wanted == "Holländisch":
            content_prompt = f"Antworte auf {lang_wanted}. Erstelle eine H1 Überschrift für {urlaubsart_input} {focus_destination}. Falls vorhanden ergänze: {aktueller_monat} {jahreszahl}. Folge dem Beispiel 'Urlaub Mallorca 2024', oder auf Spanisch 'Viajes canarias 2024', oder auf Holländisch 'Griekenland vakantie 2024'."
    return act_as_prompt, content_prompt   

## Sehenswürdigkeiten Prompts
# Mit nachfolgendem Prompt werden neue Sehenswürdigkeiten genannt, welche bis dato noch nicht im Artikel behandelt werden
def sight_prompts(number_of_sights_wanted, destination_wanted, sights_not_needed, lang_wanted):
    act_as_prompt_sights = f"Du bist SEO Spezialist für ein Reiseunternehmen. Du verfasst einen Sehenswürdigkeiten Artikel in der Urlaubsguru Brand Tonalität."
    structure_prompt_sights = f"Antworte auf {lang_wanted}. Nenne mir exakt {number_of_sights_wanted} Sehenswürdigkeiten, die man in {destination_wanted} abseits von {sights_not_needed} unbedingt gesehen haben. Wenn es weniger geben sollte, dann antworte mit ausschließlich denen, die du kennst. Antworte mit dem originlen Namen der Sehenswürdigkeiten in der jeweiligen Landessprache."
    #structure_famous_prompts = f"Antworte auf {lang_wanted}. Nenne mir exakt 3 berühmte Sehenswürdigkeiten auf {destination_wanted}."
    return act_as_prompt_sights, structure_prompt_sights

# Mit nachfolgendem Prompt wird der beschreibende Text sowie der Bild-Tipp für jede neue Sehenswürdigkeit generiert
def new_sight_prompt(content_length_wanted, new_sight, destination_wanted, lang_wanted):
    content_prompt_new_sight = f"Antworte auf {lang_wanted}. Schreibe maximal {content_length_wanted} Wörter. Beschreibe die Sehenswürdigkeit {new_sight} in {destination_wanted} in der Urlaubsguru Brand Tonalität. Verwende direkte Ansprache der Leser bei Bedarf, indem du sie im Plural mit 'Ihr' anredest."
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
        content_prompt = f"Antworte auf {lang_wanted}. Antworte ausschließlich mit einer Python-Liste. Sonst nichts. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Überlege dir dabei ganz genau, welche Themen ein Artikel zu diesem Thema benötigt. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient der Inspiration und soll Vorfreude entwickeln. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
    elif page_type == "Informational":
        content_prompt = f"Antworte auf {lang_wanted}. Antworte ausschließlich mit einer Python-Liste. Sonst nichts. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Überlege dir dabei ganz genau, welche Themen ein Artikel zu diesem Thema benötigt. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient der Information und soll faktisch korrekt sein. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
    elif page_type == "Transactional":
        content_prompt = f"Antworte auf {lang_wanted}. Antworte ausschließlich mit einer Python-Liste. Sonst nichts. Ich brauche {nr_of_headlines_wanted} Überschriften für einen ganzheitlichen Artikel zu {target_topic}. Zielgruppe des Artikels ist: {target_audience}. Der Artikel dient dem Verkauf von Reisen und soll folgende Aspekte beinhalten: {target_topic} nach Reisedauer (je nachdem was für diese {target_topic} von Deutschland aus Sinn ergibt), für verschiedene Reisegruppen (Paare, Familien, Singles), Reisetypen (Adventurer, Sightseeing, Erholung,...). Außerdem Top Unterkünfte sollen dabei sein. Ziel der Seite: {goal_choice}. Schreibe jede Headline als List-Item einer Python List und antworte ausschließlich mit der Python Liste."
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
    act_as_prompt_sights = f"Du bist SEO Spezialist für ein Reiseunternehmen. Du verfasst Artikel über die schönsten Strände dieser Welt in der Urlaubsguru-Brand-Tonalität."
    structure_prompt_sights = f"Antworte auf {lang_wanted}. Nenne mir exakt {number_of_beaches_wanted} Strände, die man in {destination_wanted} abseits von {beaches_not_needed} unbedingt gesehen haben? Wenn es weniger geben sollte, dann antworte mit ausschließlich denen, die du kennst. Antworte mit dem originlen Namen der Strände in der jeweiligen Landessprache."
    return act_as_prompt_sights, structure_prompt_sights

def new_beach_prompt(content_length_wanted_beaches, beach, destination_wanted_for_beach, lang_wanted):
    content_prompt_new_sight = f"Antworte auf {lang_wanted}. Erzähle etwas über den Strand {beach}. Schreibe {content_length_wanted_beaches} Worte. Was macht ihn so besonders? Warum muss man als Tourist dort hin? Schreibe in der Urlaubsguru Brand Tonalität. Verwende direkte Ansprache der Leser bei Bedarf, indem du sie im Plural mit 'Ihr' anredest."
    return content_prompt_new_sight


#### prompts für alt text

def alt_tag_prompts(lang_wanted, image_url, image_context):
    content_prompt_alt_text = f"Verfasse einen Alt Text für das Bild {image_url} mit maximal 150 Zeichen auf {lang_wanted}. {image_context} sollte vorkommen. Stelle dir vor, du möchtest einer sehbeeinträchgiten Person erklären, was auf dem Bild zu sehen ist. Welche Elemente siehst du? Wo sind sie platziert? Schreibe nicht 'das Bild zeigt...' sondern beschreibe es direkt."
    return content_prompt_alt_text

def caption_prompts(lang_wanted, image_url):
    caption_prompt_text = f"Verfasse einen Caption Text für das Bild {image_url} mit bis zu 10 Wörtern in der Sprache {lang_wanted}. Die Caption ist direkt unter dem Bild und soll während dem Betrachten des Bildes zusätzlichen Kontext bieten."
    return caption_prompt_text



#### prompts for product data
def product_text_prompt(lang_wanted,  angebotsdetails, emojis_wanted, headline, vorteilskommunikation, exlusiv_angebot):
    if emojis_wanted == False:
        act_as_prompt_product = f"Antworte auf {lang_wanted}. Du bist Produkt-Spezialist bei einem Reiseunternehmen. Du verfasst Angebote für ganz besondere Unterkünfte und Destinationen. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch)."
    elif emojis_wanted == True:
        act_as_prompt_product = f"Antworte auf {lang_wanted}. Du bist Produkt-Spezialist bei einem Reiseunternehmen. Du verfasst Angebote für ganz besondere Unterkünfte und Destinationen. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch). Verwende passende Emojis."

    product_text_prompt_no_voucher = f"Verfasse eine Angebotsbeschreibung mit maximal 3 Absätzen. Formuliere einen ansprechenden Text über das Angebot selbst. Gehe dabei auf das generelle Thema ein ({headline}) und konzentriere dich auf die Vorteilskommunikation ({vorteilskommunikation}. Anschließend erwähnst du wichtige Details über das Angebot ({angebotsdetails}). Schließe den Text mit einem Schluss ab, das Lust auf die Reise wecken soll."
    title_tag_prompt = f"Verfasse einen Google Title Tag mit maximal 60 Zeichen, der besonderes Augenmerk auf die Besonderheit {headline} legt. Das muss vorhanden sein. Kommuniziere außerdem {vorteilskommunikation}."
    description_tag_prompt = f"Verfasse eine Google Meta Description mit maximal 150 Zeichen. Die Description soll den User am Anfang mit seinem Bedürfnis abholen, dass er hat wenn er nach '{headline} {vorteilskommunikation}' sucht, danach kommunizierst du {exlusiv_angebot}. Achte auf Emotionalität. Die Google Meta Description soll die Vorfreude auf das Angebot wecken und zum kaufen verleiten. Am Ende soll ein Call to Action folgen, der Buchungsinteresse wecken soll."
    h1_prompt = f"Verfasse eine Hauptüberschrift (H1) mit maximal 60 Zeichen. Im Fokus stehen sollte {headline} sowie {vorteilskommunikation}"
    subheader_prompt = f"Verfasse eine Subheader mit maximal 60 Zeichen. Wichtig ist hier insbesondere {angebotsdetails} und soll zum weiterlesen und buchen anregen."

    return product_text_prompt_no_voucher, act_as_prompt_product, title_tag_prompt, description_tag_prompt, h1_prompt, subheader_prompt

def product_text_prompt_with_voucher(lang_wanted,  angebotsdetails, emojis_wanted, headline, vorteilskommunikation, exlusiv_angebot, gutscheincode, einloesezeitraum_start, einloesezeitraum_ende, mindestbestellwert, gueltig_bis):
    if emojis_wanted == False:
        act_as_prompt_product = f"Antworte auf {lang_wanted}. Du bist Produkt-Spezialist bei einem Reiseunternehmen. Du verfasst Angebote für ganz besondere Unterkünfte und Destinationen. Bei dem Angebot geht es ganz speziell um den Fokus auf {exlusiv_angebot}. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch)."
    elif emojis_wanted == True:
        act_as_prompt_product = f"Antworte auf {lang_wanted}. Du bist Produkt-Spezialist bei einem Reiseunternehmen. Du verfasst Angebote für ganz besondere Unterkünfte und Destinationen. Bei dem Angebot geht es ganz speziell um den Fokus auf {exlusiv_angebot}. Du bist mit den Lesern Per Du, sprichst sie im Plural an (ihr/euch). Verwende passende Emojis. "
    
    product_text_prompt_with_voucher = f"Verfasse eine Angebotsbeschreibung mit maximal 3 Absätzen. Die Struktur ist dabei in zwei Bereiche gegliedert: Zunächst sprichst du über den Gutschein, danach über das Angebot. Für den Gutschein ziehst du folgende Informationen heran: Den Gutschein-Code ({gutscheincode}), den Einlösezeitraum (Startdatum: {einloesezeitraum_start} sowie Enddatum: {einloesezeitraum_ende}), den Mindestbestellwert ({mindestbestellwert}) sowie die allgemeine Gültigkeit ({gueltig_bis}. Anschließend formulierst du einen ansprechenden Text über das Angebot selbst. Gehe dabei auf das generelle Thema ein ({headline}) und konzentriere dich auf die Vorteilskommunikation ({vorteilskommunikation}. Anschließend erwähnst du wichtige Details über das Angebot ({angebotsdetails}). Schließe den Text mit einem Schluss ab, das Lust auf die Reise wecken soll."
    headline_prompt = f"Verfasse einen Google Title Tag mit maximal 60 Zeichen, der besonderes Augenmerk auf die Besonderheit {headline} legt. Das muss vorhanden sein. Kommuniziere außerdem {vorteilskommunikation}."
    description_prompt = f"Verfasse eine Google Meta Description mit maximal 150 Zeichen. Die Description soll den User am Anfang mit seinem Bedürfnis abholen, dass er hat wenn er nach '{headline} {vorteilskommunikation}' sucht, danach kommunizierst du {exlusiv_angebot}. Achte auf Emotionalität. Die Google Meta Description soll die Vorfreude auf das Angebot wecken und zum kaufen verleiten. Am Ende soll ein Call to Action folgen, der Buchungsinteresse wecken soll."
    h1_prompt = f"Verfasse eine Hauptüberschrift (H1) mit maximal 60 Zeichen. Im Fokus stehen sollte {headline} sowie {vorteilskommunikation}. Erwähne außerdem, dass es einen Gutschein gibt. "
    subheader_prompt = f"Verfasse eine Subheader mit maximal 60 Zeichen. Wichtig ist hier insbesondere {angebotsdetails} und die Möglichekit eines Gutscheins. Soll zum weiterlesen und buchen anregen."

    return product_text_prompt_with_voucher, act_as_prompt_product, headline_prompt, description_prompt, h1_prompt, subheader_prompt

