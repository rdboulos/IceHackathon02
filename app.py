import openai 
import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

# pip install streamlit-chat  
from streamlit_chat import message

openai.api_key = "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"

# Creating a function which will generate the calls from the API

# Load CSV 
df = pd.read_csv("C:/Users/SurajKannan/OneDrive - Decision Inc/Desktop/Innovation Project/OpenAI/garminfile/GOTOES_FIT.csv")
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
    st.write(x)
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
