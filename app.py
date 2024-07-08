from gradio_client import Client

import streamlit as st 
import json

client = Client('AyushS9020/Vivek_Project')

def answer(query , location , history) : 

    query = 'Do not return html or xml tags in your response\n' + query
    
    result = client.predict(
		query = query , 
		type = location , 
		history = history , 
		api_name = '/predict'
    )

    return result 

def check_prompt(prompt) : 

    '''
    Function to check the prompt

    Args:
    prompt : str : The prompt to be checked

    Returns:
    bool : The boolean value indicating whether the prompt is valid or not
    '''

    try : 
        prompt.replace('' , '')
        return True 
    except : return False


def check_mesaage() : 
    '''
    Function to check the messages
    '''

    if 'messages' not in st.session_state : st.session_state.messages = []

check_mesaage()

for message in st.session_state.messages : 

    with st.chat_message(message['role']) : st.markdown(message['content'])

prompt = st.chat_input('Ask me anything')
location = st.sidebar.selectbox('Select the Location' , ['Los Angeles' , 'San Francisco' , 'Washington DC' , 'New York City'])

if check_prompt(prompt) :

    with st.chat_message('user') : st.markdown(prompt)

    st.session_state.messages.append({
        'role' : 'user' , 
        'content' : prompt
    })

    if prompt != None or prompt != '' : 

        location = location.replace(' ' , '_')

        response = answer(
            prompt , 
            location ,
            '\n'.join(open('chat_logs.json').read().split('\n')[- 6 : ])    
        )

        json.dump({
            'query' : prompt , 
            'response' : response
        } , open('chat_logs.json' , 'a'))

        with st.chat_message('assistant') : st.markdown(response)

        st.session_state.messages.append({
            'role' : 'assistant' , 
            'content' : response
        })






