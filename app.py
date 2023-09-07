import openai 
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

# pip install streamlit-chat  
from streamlit_chat import message


API_KEY='````sk-KUXXmJ4kF````Eblnb1JXwSg````T3BlbkFJw````E8Qbz411kQ2Q````pWww90w````'
openai.api_key = API_KEY.replace('````', '')

#openai.api_key = "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"

# Creating a function which will generate the calls from the API

# Load CSV 
if "openai_key" not in st.session_state:
    with st.form("API key"):
        key = st.text_input("OpenAI Key", value="", type="password")
        if st.form_submit_button("Submit"):
            st.session_state.openai_key = key
            st.session_state.prompt_history = []
            st.session_state.df = None

if "openai_key" in st.session_state:
    if st.session_state.df is None:
        uploaded_file = st.file_uploader(
            "Choose a CSV file. This should be in long format (one datapoint per row).",
            type="csv",
        )
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.session_state.df = df
		
# Define the LLM
def generate_response(user_input):
    llm = OpenAI(api_token=openai.api_key)
    pandas_ai = PandasAI(llm, conversational=True)
    x = pandas_ai.run(st.session_state.df, prompt=user_input)

    fig = plt.gcf()
    # fig, ax = plt.subplots()
    if fig.get_axes():
        st.pyplot(fig)
    #st.write(x)
    return x


st.title("ICE Chatbot Assistant")

# Storing the chat
if 'generated' not in st.session_state:
	st.session_state['generated'] = []

if 'past' not in st.session_state:
	st.session_state['past'] = []

def get_text():
	input_text = st.text_input("You: ","Hello, how are you?", key = "input")
	return input_text

user_input = get_text()

if user_input:
	output = generate_response(user_input)
	#store the output
	st.session_state.past.append(user_input)
	st.session_state.generated.append(output)

if st.session_state['generated']:

	for i in range(len(st.session_state['generated'])-1,-1,-1):
		message(st.session_state["generated"][i],key=str(i))
		message(st.session_state['past'][i],is_user=True,key=str(i) + '_user')
