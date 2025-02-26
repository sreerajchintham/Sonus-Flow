import requests
from bs4 import BeautifulSoup 
import streamlit as st
from gtts import gTTS
def get_novel(url):
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
    try:
        response = requests.get(url,headers=headers)
        if response and response.status_code == 200 :
            soup = BeautifulSoup(response.text,"html.parser")
            chapter_txt = soup.find_all("div",class_ = "chr-c")
            chapter_txt = [p.text for p in chapter_txt]
            chapter_text = "\n\n".join(chapter_txt)
            return chapter_text
        return f"Can not retrieve the URL : Response Status Code - {response.status_code}"
    except:
          return "Invalid URL"

def generate_audio(text,lang):
    if text == "Invalid URL" or f"Can not retrieve the URL : Response Status Code" in text:
         return 
    tts = gTTS(text=text,lang=lang,slow=False)
    audio_path = "output.mp3"
    tts.save(audio_path)
    return audio_path


st.title("Chapter Audio Generator")
chap_url = st.text_input("Enter your chapter url:")
language = st.selectbox("Select Language", ["en", "es", "fr", "de"])
if st.button("Generate Audio file"):
    if chap_url:
        text = get_novel(chap_url)
        audio_path = generate_audio(text,lang=language)
        with open(audio_path, "rb") as audio_file:
                    st.audio(audio_path, format="audio/mp3")
                    st.download_button(label="Download Audio", data=audio_file, file_name="output.mp3", mime="audio/mp3")

        st.write("Audio Generated Successfully!!!")
    else:
        st.error("Enter a Valid URL")