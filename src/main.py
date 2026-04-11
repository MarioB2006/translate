import requests
import streamlit as st
import json

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
            error="Error from translation extraction. Provided API-key was wrong. Please reload and re-enter this website!!"
            return error
        return translation 

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

    def first_panel(self):
        self.style()
        if "text_input_api" not in st.session_state:
            st.session_state.text_input_api=None
        st.markdown('<div class="title">API Key</div><br><br><br><br><br>', unsafe_allow_html=True)
        width = 500
        st.markdown('<div>', unsafe_allow_html=True)
        st.session_state.text_input_api = st.text_input("input",width=width)
        st.markdown('</div>', unsafe_allow_html=True,width=width)
        st.markdown('<div class="center-button">', unsafe_allow_html=True)
        st.button("Submit API-key",on_click=lambda:submit())
        st.markdown('</div>', unsafe_allow_html=True)
        def submit():
            st.session_state.temp_api_key = st.session_state.text_input_api
            st.session_state.show_main_app = True

    def main_app(self):
        if "text_input" not in st.session_state:
            st.session_state.text_input=None
        if "language1" not in st.session_state:
            st.session_state.language1=None
        if "language2" not in st.session_state:
            st.session_state.language2=None
        if "text_output" not in st.session_state:
            st.session_state.text_output=None
        if "error" not in st.session_state:
            st.session_state.error=""
        if "temp_api_key" not in st.session_state:
            st.session_state.temp_api_key = ""

        with open("languages.json", 'r') as f:
            loaded_dict = json.load(f)
        keys=[k for k in loaded_dict]
        self.style()
        st.markdown('<div class="title">TRANSLATE</div><br><br>', unsafe_allow_html=True)
        st.set_page_config(layout="wide")
        space1,col1,space2,col2,space3 = st.columns([0.5,1,0.25,1,0.5])
        with col1:
            st.session_state.language1 = st.selectbox(label="Translate from",options=keys)
            st.markdown('<div>', unsafe_allow_html=True)
            st.session_state.text_input = st.text_area("input")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<br><br><div class="center-button">', unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:15px;'>{st.session_state.error}</p>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with space2:
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            st.button("Translate",on_click=lambda:query())
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('<br><br><br><br><br><div class="center-button">', unsafe_allow_html=True)
            st.button("end app",on_click=lambda:stop())
            st.markdown('</div>', unsafe_allow_html=True)
        with col2:
            st.session_state.language2 = st.selectbox(label="Translate to",options=keys)
            st.markdown('<div>', unsafe_allow_html=True)
            st.session_state.text_output = st.text_area("output",value=st.session_state.text_output)
            st.markdown('</div>', unsafe_allow_html=True)

            def stop():
                st.session_state.temp_api_key = ""
                st.stop()
            def query():
                for key, value in loaded_dict.items():
                    if key == st.session_state.language1:
                        st.session_state.language1=value
                    if key == st.session_state.language2:
                        st.session_state.language2=value
                translation = self.translator.get_response(st.session_state.language1,st.session_state.language2,st.session_state.text_input)
                if translation.startswith("Error"):
                    st.session_state.error = translation
                else:
                    st.session_state.text_output = translation
    
def main():	
    if "show_main_app" not in st.session_state:
        st.session_state.show_main_app = False
    if not st.session_state.show_main_app:
        web = Web_app(None)  
        web.first_panel()
    else:
        api_key = st.session_state.get("temp_api_key")
        t = Translator(api_key)
        web = Web_app(t)
        web.main_app()

if __name__=="__main__":
    main()