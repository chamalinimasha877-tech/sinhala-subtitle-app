import streamlit as st
import google.generativeai as genai

st.title("🎬 Spoken Sinhala Subtitle Converter")
st.write("Upload your English .srt file and convert it into natural conversational Sinhala!")

api_key = st.text_input("Enter your Gemini API Key:", type="password")
uploaded_file = st.file_uploader("Upload English .srt file", type=["srt"])

if uploaded_file is not None and api_key:
    srt_content = uploaded_file.read().decode("utf-8", errors="ignore")
    
    if st.button("Translate Now 🚀"):
        with st.spinner("Translating into conversational Sinhala... Please wait..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                prompt = f"""
                Translate the following English SRT subtitle content into natural, conversational, and spoken Sinhala (කතා කරන බසින් සිංහලට).
                
                CRITICAL RULES:
                1. Do NOT change, translate, or mess up the SRT numbers, timestamps, or line formatting. Keep them 100% identical to the original.
                2. Only translate the dialogue text lines into natural, fluent spoken Sinhala using accurate Sinhala letters.
                3. Return ONLY the valid SRT format output without any extra explanations.
                
                Here is the SRT content:
                {srt_content}
                """
                
                response = model.generate_content(prompt)
                translated_text = response.text
                
                if translated_text.startswith("```"):
                    translated_text = translated_text.split("```")[1]
                    if translated_text.startswith("srt") or translated_text.startswith("text"):
                        translated_text = translated_text.split("\n", 1)[1]
                    translated_text = translated_text.rsplit("```", 1)[0].strip()
                
                st.success("Done! 🎉")
                
                st.download_button(
                    label="📥 Download Sinhala SRT File",
                    data=translated_text,
                    file_name="sinhala_conversational.srt",
                    mime="text/plain"
                )
            except Exception as e:
                st.error(f"Error: {e}")
elif uploaded_file is not None and not api_key:
    st.warning("⚠️ Please enter your Gemini API key.")