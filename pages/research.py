import streamlit as st
from groq import Groq

st.title("🔬 Research & Verification")
mission = st.session_state.get('global_mission')

if not mission:
    st.warning("Awaiting mission from War Room...")
else:
    api_key = st.secrets.get("GROQ_API_KEY")
    
    if api_key:
        client = Groq(api_key=api_key)

        # AUTO-EXECUTION LOGIC
        # Checks if we have the mission but haven't run the research yet
        if 'res_res' not in st.session_state:
            with st.spinner("Research Director is verifying data points..."):
                res = client.chat.completions.create(
                    model="llama-3.1-8b-instant", # Faster model for quick fact-checking
                    messages=[
                        {"role": "system", "content": "You are the Research Director. Execute the [RESEARCH] portion of this mission. Provide technical specs, verify claims, and cite potential sources."},
                        {"role": "user", "content": mission}
                    ]
                )
                st.session_state['res_res'] = res.choices[0].message.content

        # Display the result (either newly generated or from memory)
        st.success("### 🔍 Research & Verification Report")
        st.markdown(st.session_state['res_res'])
    else:
        st.error("Missing GROQ_API_KEY in Streamlit Secrets.")
