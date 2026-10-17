
import streamlit as st
from pypdf import PdfReader
from google import genai

st.set_page_config(
    page_title="Golu AI Study Master",
    page_icon="📚"
)

st.title("📚 Golu AI Study Master")
st.write("सरकारी नौकरी और टेक्निकल परीक्षा की तैयारी करें।")

api_key = st.sidebar.text_input(
    "Gemini API Key डालें",
    type="password"
)

pdf = st.file_uploader("अपनी किताब की PDF अपलोड करें", type=["pdf"])

if pdf:
    reader = PdfReader(pdf)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)

    question = st.text_input("अपना सवाल लिखें")

    if st.button("उत्तर प्राप्त करें"):
        if not api_key:
            st.warning("पहले Gemini API Key डालें।")
        elif not question:
            st.warning("पहले अपना सवाल लिखें।")
        else:
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=f"इस किताब की सामग्री के आधार पर सरल हिंदी में उत्तर दें।\n{text[:20000]}\nसवाल: {question}"
                )
                st.write(response.text)
            except Exception as e:
                st.error(f"त्रुटि: {e}")
