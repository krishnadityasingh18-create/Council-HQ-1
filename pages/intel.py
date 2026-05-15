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
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are an OSINT expert. Provide vulnerabilities, market risks, and Google Dorking queries."},
                    {"role": "user", "content": target}
                ]
            )
            st.info(completion.choices[0].message.content)
else:
    st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
            # The System Prompt is what makes the "Intel" agent unique
            system_message = f"""
            You are the Intelligence Director. You specialize in OSINT, competitive strategy, and risk analysis.
            Perform a {depth} analysis on the provided target.
            Structure your response as follows:
            - 🛡️ VULNERABILITY REPORT
            - 📈 MARKET OPPORTUNITIES
            - ⚠️ POTENTIAL RISKS
            - 🔍 SUGGESTED GOOGLE DORKS (for further research)
            """
            
            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": f"Analyze: {target}"}
                    ]
                )
                
                # 4. Display the Result
                st.markdown("### 📋 Intelligence Briefing")
                st.info(completion.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Agent Disconnected: {e}")
else:
    st.warning("Intelligence Agent is **Offline**. Please enter your Groq API Key in the sidebar.")

# 5. Sidebar Department Status
st.sidebar.markdown("---")
st.sidebar.write("Agent: **Scout-Llama-4**")
st.sidebar.write("Status: **Active**" if groq_key else "Status: **Locked**")
