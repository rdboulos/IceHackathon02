import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import matplotlib.pyplot as plt

API_KEY='````sk-KUXXmJ4kF````Eblnb1JXwSg````T3BlbkFJw````E8Qbz411kQ2Q````pWww90w````'
API_KEY_2 = API_KEY.replace('````', '')


st.title("Matthew Dinham")

st.write("2023 UCI Cycling World Championships")
#st.write(
    #"Looking for an example *.csv-file?, check [here](https://gist.github.com/netj/8836201).")

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
            
            #data_frames = []
            #data_frames.append(df)
            #combined_df = pd.concat(data_frames, ignore_index=True)

    with st.form("Question"):
        question = st.text_input("Question", value="", type="default")
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner():
                llm = OpenAI(api_token=API_KEY_2)
                pandas_ai = PandasAI(llm, conversational=True, enable_cache=False)
                x = pandas_ai.run(st.session_state.df, prompt=question)
                
                fig = plt.gcf()
                #fig, ax = plt.subplots()
                if fig.get_axes():
                    st.pyplot(fig)
                st.write(x)
                st.session_state.prompt_history.append(question)

    if st.session_state.df is not None:
        st.subheader("Current dataframe:")
        st.write(st.session_state.df)

    st.subheader("Prompt history:")
    st.write(st.session_state.prompt_history)


if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None
