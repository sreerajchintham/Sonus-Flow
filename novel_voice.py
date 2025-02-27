import requests
from bs4 import BeautifulSoup 
import streamlit as st
from gtts import gTTS
import time
from pydub import AudioSegment
next_page = ""
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
            global next_page
            next_page = soup.find("a", id ="next_chap")['href']
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
def change_format(audio_path):
    mp3_audio = AudioSegment.from_file(audio_path, format="mp3")
    mp3_audio.export("output.wav", format="wav")

st.title("Sonus Flow")
chap_url = st.text_input("Enter your chapter URL:")
language = st.selectbox("Select the Language ", ["en", "es", "fr", "de"])
start_time = time.time()
if st.button("Generate Audio file"):
    if chap_url:
        text = get_novel(chap_url)
        print(next_page)
        if next_page:
            st.link_button("Next Chapter", next_page)
        audio_path = generate_audio(text,lang=language)
        change_format(audio_path)
        with open("output.wav", "rb") as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/wav")
        with open(audio_path, "rb") as audio_file:
                    st.download_button(label="Download Audio", data=audio_file, file_name="output.wav", mime="audio/mp3")

        st.write("Audio Generated Successfully!!!")
    else:
        st.error("Enter a Valid URL")

stop_time = time.time()

st.write(f"Total Time Taken - {int((stop_time-start_time)//60)} minutes and {int((stop_time-start_time)%60)} seconds")