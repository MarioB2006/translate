# Describtion
A simple, lightweight web app for instant text translation. It uses `Deep Translate’s API` under the hood to provide fast and accurate translations across 59 languages.
The app features a clean, user‑friendly interface where you can paste or type text, choose source and target languages, and get results in real time.

## Usage
* click on this link for using it as a web-app:<br>
https://mariob2006-translate-srcmain-ea102j.streamlit.app/

## Libraries used
* requests
* streamlit
* json

## How to use
When clicked on the link, the main app will open. Here, the user can choose the languages. The text needs to be translated is written inside the "input" text field. After clicking on "Translate", the result will be shown in the "output" text field. In case of providing a wrong API-key, there will be displayed an error message, saying that the website must be reloaded and re-submitting the right key. The "swap" button will swap the input and output text as well as the sourche and target language<br>
**It is important to click on "end app" to successfully close the app which also removes the API-key used.**<br>
![main app](pictures/main_app.png)

## Roadmap
* v1: first version of the web-app
* v2: adding to swap the text and languages via button
* v3: adding more languages for translation, adding auto-detection