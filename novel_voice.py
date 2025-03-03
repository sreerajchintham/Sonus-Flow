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
            print("Response retrieved successfully")
            soup = BeautifulSoup(response.text,"html.parser")
            chapter_txt = soup.find_all("div",class_ = "chr-c")
            chapter_txt = [p.text for p in chapter_txt]
            chapter_text = "\n\n".join(chapter_txt)
            global next_page
            next_page = soup.find("a", id ="next_chap")['href']
            return chapter_text
        print(f"Response Not retrieved {response.status_code}")
        return f"Can not retrieve the URL : Response Status Code - {response.status_code}"
    except:
        print("Invalid URL")
        return "Invalid URL"


def generate_audio(text,lang):
    if text == "Invalid URL" or f"Can not retrieve the URL : Response Status Code" in text:
        print("audio didn't generate because not right text")
        return
    tts = gTTS(text=text,lang=lang,slow=False)
    audio_path = "output.mp3"
    tts.save(audio_path)
    print("Audio generated successfully using TTS")
    return audio_path
def change_format(audio_path):
    mp3_audio = AudioSegment.from_file(audio_path, format="mp3")
    wav_audio_path = "output.wav"
    mp3_audio.export(wav_audio_path, format="wav")
    print("Audio successfully changed")
    return wav_audio_path

     
st.title("Sonus Flow")
if "loading" not in st.session_state:
    st.session_state.loading = False
chap_url = st.text_input("Enter your chapter URL:")
language = st.selectbox("Select the Language ", ["en", "es", "fr", "de"])
start_time = time.time()
if st.button("Generate Audio file",):
    st.session_state.loading = True
    try:
        if chap_url:
            with st.spinner("Loading..."):
                text = get_novel(chap_url)
                print(next_page)
                audio_path = generate_audio(text,lang=language)
                wav_audio_path = change_format(audio_path)

            with open(wav_audio_path, "rb") as f:
                audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/wav")
            with open(audio_path, "rb") as audio_file:
                        st.download_button(label="Download Audio", data=audio_file, file_name="output.wav", mime="audio/mp3")
    
            st.success("Audio Generated Successfully!!!")
        
            if next_page:
                st.link_button("Next Chapter", next_page)
        else:
            st.error("Enter a Valid URL")
    except:
        st.write("Audio could not be generated")
    st.session_state.loading = False
stop_time = time.time()

st.write(f"Total Time Taken - {int((stop_time-start_time)//60)} minutes and {int((stop_time-start_time)%60)} seconds")
