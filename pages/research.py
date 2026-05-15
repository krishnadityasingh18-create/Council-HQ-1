import streamlit as st
from groq import Groq

st.title("🔬 Research & Verification")

groq_key = st.sidebar.text_input("Groq API Key (Research)", type="password")

if groq_key:
    client = Groq(api_key=groq_key)
    query = st.text_input("Data to Verify:")

    if st.button("Fact Check"):
        with st.spinner("Scanning academic databases..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant", # Or Llama 4 Scout if available on your Groq tier
                messages=[{"role": "system", "content": "You are the Research Director. Be skeptical. Fact-check everything and provide sources."},
                          {"role": "user", "content": query}]
            )
            st.write(completion.choices[0].message.content)