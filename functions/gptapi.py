import streamlit as st
import openai
from openai import OpenAI

###GPT API KEY
OPENAI_API_KEY = st.secrets["openai_api_key"]
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

####

@st.cache_data
def openAI_json_response(user_prompt, lang_wanted):
    gpt_version = "gpt-3.5-turbo-1106"
    response = client.chat.completions.create(
        model=gpt_version,
        response_format={
            "type": "json_object"
        },
        messages=[
            {"role": "system",
             "content": f"Answer in {lang_wanted}. You are a helpful assistant designed to output JSON."},
             {"role": "user",
              "content": user_prompt}
        ]
    )
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    generated_content = response.choices[0].message.content

    
    if gpt_version == "gpt-4-1106-preview": 
        cost_per_token_input = 0.01
        cost_per_token_output = 0.03
    elif gpt_version == "gpt-4-vision-preview":
        cost_per_token_input = 0.01
        cost_per_token_output = 0.03
    elif gpt_version == "gpt-3.5-turbo-1106":
        cost_per_token_input = 0.001
        cost_per_token_output = 0.002
    elif gpt_version.startswith("ft:"):
        cost_per_token_input = 0.0030
        cost_per_token_output = 0.0060
        
    cost_prompt = prompt_tokens * (cost_per_token_input/1000)
    cost_completion = completion_tokens * (cost_per_token_output/1000)
    total_cost = cost_prompt + cost_completion
    total_cost = round(total_cost, 5)

    return generated_content, total_cost

@st.cache_data
def openAI_content(system_act_as, user_prompt, temp_wanted, gpt_version):
    response = client.chat.completions.create( #).ChatCompletion.create(
        model=gpt_version,
        messages=[
            {"role": "system", "content": system_act_as},
            {"role": "user", "content": user_prompt}
        ],
        temperature=temp_wanted
    )
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
    generated_content = response.choices[0].message.content
    gpt_version_used = response.model

    
    if gpt_version == "gpt-4-1106-preview": 
        cost_per_token_input = 0.01
        cost_per_token_output = 0.03
    elif gpt_version == "gpt-4-vision-preview":
        cost_per_token_input = 0.01
        cost_per_token_output = 0.03
    elif gpt_version == "gpt-3.5-turbo-1106":
        cost_per_token_input = 0.001
        cost_per_token_output = 0.002
    elif gpt_version.startswith("ft:"):
        cost_per_token_input = 0.0030
        cost_per_token_output = 0.0060
        
    cost_prompt = prompt_tokens * (cost_per_token_input/1000)
    cost_completion = completion_tokens * (cost_per_token_output/1000)
    total_cost = cost_prompt + cost_completion
    total_cost = round(total_cost, 5)

    return generated_content, total_cost, gpt_version_used


@st.cache_data
def openAI_vision(user_prompt, image_url):
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text",
                     "text": user_prompt},
                     {
                         "type": "image_url",
                         "image_url": image_url
                     },
                ],
            }
        ],
        max_tokens=500,
    )
    prompt_tokens = response.usage.prompt_tokens
    completion_tokens = response.usage.completion_tokens
        
    cost_per_token_input = 0.01
    cost_per_token_output = 0.03
        
    cost_prompt = prompt_tokens * (cost_per_token_input/1000)
    cost_completion = completion_tokens * (cost_per_token_output/1000)
    total_cost = cost_prompt + cost_completion
    total_cost = round(total_cost, 5)

    generated_content = response.choices[0].message.content
    gpt_version_used = response.model

    return generated_content, total_cost, gpt_version_used