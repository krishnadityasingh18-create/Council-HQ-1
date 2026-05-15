import streamlit as st
from groq import Groq

st.title("🔬 Research & Verification")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
    query = st.text_input("Claim to verify:")

    if st.button("Verify Data"):
        with st.spinner("Consulting archives..."):
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "system", "content": "You are the Research Director. Fact-check the input and provide sources."},
                          {"role": "user", "content": query}]
            )
            st.success(completion.choices[0].message.content)
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
