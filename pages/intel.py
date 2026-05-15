import streamlit as st
from groq import Groq

st.title("🕵️ Intelligence Department")
st.markdown("---")

api_key = st.secrets.get("GROQ_API_KEY")

if api_key:
    client = Groq(api_key=api_key)
    target = st.text_input("Target for Analysis:")

    if st.button("Generate Intel"):
        with st.spinner("Agent Scout is active..."):
            # Ensure the line below has NO extra spaces before 'system_message'
            system_message = f"""
            You are an OSINT expert. Provide vulnerabilities, market risks, and Google Dorking queries.
            """
            
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": target}
                ]
            )
            st.info(completion.choices[0].message.content)
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
