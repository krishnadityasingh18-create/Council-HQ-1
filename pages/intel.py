import streamlit as st
from groq import Groq

st.title("🕵️ Intelligence Department")
st.markdown("---")

# 1. Access the API Key from the Sidebar
groq_key = st.sidebar.text_input("Groq API Key (Intel)", type="password")

if groq_key:
    client = Groq(api_key=groq_key)
    
    # 2. Input for the "Target"
    target = st.text_input("Enter Target/Topic for Analysis:", 
                          placeholder="e.g., Competitor analysis for low-cost PCB assembly in India")

    # 3. Intelligence Parameters
    depth = st.select_slider("Analysis Depth", options=["Surface", "Standard", "Deep Dive"])
    
    if st.button("Generate Intelligence Dossier"):
        with st.spinner("Scout Agent is performing reconnaissance..."):
            
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