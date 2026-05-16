import requests
import streamlit as st
import json

from dotenv import load_dotenv
import os

class Translator:
    def __init__(self,API_key):
        self.API_key=API_key
    def get_response(self,source_language,target_language,query):
        payload = {
                "q": query,
                "source": source_language,
                "target": target_language
            }
        headers = {
                "x-rapidapi-key": self.API_key,
                "x-rapidapi-host": "deep-translate1.p.rapidapi.com",
                "Content-Type": "application/json"
            }
        response = requests.post(url="https://deep-translate1.p.rapidapi.com/language/translate/v2", json=payload, headers=headers).json()
        try:
            translation = response['data']['translations']['translatedText'][0]
        except KeyError:
            error="Error from translation extraction. Please reload this website!!"
            return error
        return translation

class AI_teacher:
    def __init__(self):
        pass
    def get_response(self,query):
        url = "https://chatgpt-42.p.rapidapi.com/conversationgpt4"

        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": query
                }
            ],
            "system_prompt": "",
            "temperature": 0.9,
            "top_k": 5,
            "top_p": 0.9,
            "max_tokens": 256,
            "web_access": False
        }
        headers = {
            f"x-rapidapi-key": st.secrets["TRANSLATE_KEY"],
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers).json()

        return response

class Web_app:
    def __init__(self,translator:Translator):
        self.translator=translator
    def style(self):
        st.markdown(
        """
        <style>
            .title { 	 
                font-size: 40px;
                font-family: cursive;
                text-align: center;
                color: #ffffff !important;
            }
                .stApp {
                background-image: url("https://img.freepik.com/premium-vector/dark-background-with-red-black-background-with-red-light-middle_1065176-5971.jpg");
                background-size: cover;
            }
                .center-button {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        """, unsafe_allow_html=True) 

    def main_app(self):
        if "text_input" not in st.session_state:
            st.session_state.text_input=None
        if "language1" not in st.session_state:
            st.session_state.language1=None
        if "language1_key" not in st.session_state:
            st.session_state.language1_key=None
        if "language2" not in st.session_state:
            st.session_state.language2=None
        if "language2_key" not in st.session_state:
            st.session_state.language2_key=None
        if "text_output" not in st.session_state:
            st.session_state.text_output=None
        if "error" not in st.session_state:
            st.session_state.error=""
        if "AI_input" not in st.session_state:
            st.session_state.AI_input=None
        if "AI_output" not in st.session_state:
            st.session_state.AI_output=None

        with open("src/languages.json", 'r') as f: 
            loaded_dict = json.load(f)
        keys=[k for k in loaded_dict]
        self.style()
        st.markdown('<div class="title">TRANSLATE</div><br><br>', unsafe_allow_html=True)
        st.set_page_config(layout="wide")
        space1,col1,space2,col2,space3 = st.columns([0.5,1,0.25,1,0.5])
        with col1:
            st.selectbox(label="Translate from",options=keys,key="language1")
            st.markdown('<div>', unsafe_allow_html=True)
            st.text_area("input",key="text_input")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:15px;'>{st.session_state.error}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.text_area("AI tutor",key="AI_input")
        with space2:
            st.button("Translate",width=100,on_click=lambda:query())
            st.button("swap",width=100,on_click=lambda:swap())
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            st.button("delete text",on_click=lambda:delete())
            st.markdown('</div><br><br><br><br>', unsafe_allow_html=True)
            st.button("send AI",width=100,on_click=lambda:AI())
            st.markdown('<br><br><br><br><div class="center-button">', unsafe_allow_html=True)
            st.button("end app",width=100,on_click=lambda:stop())
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.selectbox(label="Translate to",options=keys,key="language2")
            st.markdown('<div>', unsafe_allow_html=True)
            st.text_area("output",key="text_output")
            st.markdown('</div><br><br>', unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:15px;'></p>", unsafe_allow_html=True)
            st.text_area("AI output",key="AI_output")

            def stop():
                st.session_state.temp_api_key = ""
                st.stop()
            def delete():
                st.session_state.text_input=None
                st.session_state.text_output=None
                st.session_state.AI_input=None
                st.session_state.AI_output=None
            def swap():
                lang1=st.session_state.language1
                lang2=st.session_state.language2
                text_out=st.session_state.text_output
                text_in=st.session_state.text_input
                for key, value in loaded_dict.items():
                    if key == lang1:
                        st.session_state.language2_key=value
                        st.session_state.language2=key
                    if key == lang2:
                        st.session_state.language1_key=value
                        st.session_state.language1=key
                st.session_state.text_input=text_out
                st.session_state.text_output=text_in
            def query():
                for key, value in loaded_dict.items():
                    if key == st.session_state.language1:
                        st.session_state.language1_key=value
                    if key == st.session_state.language2:
                        st.session_state.language2_key=value
                translation = self.translator.get_response(st.session_state.language1_key,st.session_state.language2_key,st.session_state.text_input)
                if translation.startswith("Error"):
                    st.session_state.error = translation
                else:
                    st.session_state.text_output = translation
            def AI():
                response= AI_teacher().get_response(st.session_state.AI_input)
                st.session_state.AI_output=response["result"]

def main():	
    api_key =st.secrets["TRANSLATE_KEY"]
    t = Translator(api_key)
    web = Web_app(t)
    web.main_app()

if __name__=="__main__":
    main()