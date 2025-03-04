import requests

from bs4 import BeautifulSoup 

import streamlit as st

from gtts import gTTS

import time

from pydub import AudioSegment

next_page = ""

chapter_title = ""

def get_novel(url): # Function used to scrape the chapter text

    headers = {
         
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}
    
    try:

        # Web Scraping using Requests Package 

        response = requests.get(url,headers=headers) 

        # Checking whether the Response is Valid

        if response and response.status_code == 200 : 

            print("Response retrieved successfully")

            # Retrieving the content needed using Beautiful Soup from html Response

            soup = BeautifulSoup(response.text,"html.parser") 

            chapter_txt = soup.find_all("div",class_ = "chr-c")

            chapter_txt = [p.text for p in chapter_txt]

            chapter_text = "\n\n".join(chapter_txt)

            global next_page

            next_page = soup.find("a", id ="next_chap")['href']

            return chapter_text
        
        # Print Statements For Debugging as we use Streamlit which do not interfere with Print statements

        print(f"Request cannot be Retrieved - Response Code - {response.status_code}")

        # Returning None for Improper Responses

        return
    
    except Exception as e:

        print(f"Invalid URL Exception - {e}")

        # This error only occurs for any other websites. For now the App only takes "www.novelbin.com"

        return


# Function For Generating Audio From Text.

def generate_audio(text,lang):

    # Filtering Bad Response so they don't be 
    if text:

        # Creating GTTS object 

        tts = gTTS(text=text,lang=lang,slow=False)

        audio_path = "output.mp3"

        # Saving the File

        tts.save(audio_path)

        print("Audio generated successfully using TTS")

        return audio_path
    
    print("Text is None")

    return None

# Function to change the format from MP3 to WAV as the Streamlit audiplayer seems to be having issue with MP3

def change_format(audio_path):

    if audio_path :

        # Using Pydub which inturn uses FFMPEG to convert the imported audio file.

        mp3_audio = AudioSegment.from_file(audio_path, format="mp3")

        wav_audio_path = "output.wav"

        # Exporting Audio File

        mp3_audio.export(wav_audio_path, format="wav")

        print("Audio successfully changed")

        return wav_audio_path
    
    return 

# Streamlit Web App creation with Title and text boxes and buttons

st.title("Sonus Flow")

if "loading" not in st.session_state:
    
    st.session_state.loading = False

chap_url = st.text_input("Enter your chapter URL:")

language = st.selectbox("Select the Language ", ["en", "es", "fr", "de"])

st.write("Hi, This Web Application currently only takes the www.novelbin.com novels and chapters until further updates.")

# Using Time package to log the time of the operation.

start_time = time.time()

if st.button("Generate Audio file"):

    st.session_state.loading = True

    # Checking for any Errors and Valid Web inputs 

    try:

        # Running all the above functions and Implimenting Spinner for loading button.

        if chap_url:


            with st.spinner("loading..."):

                text = get_novel(chap_url)

                audio_path = generate_audio(text,lang=language)

                wav_audio_path = change_format(audio_path)


            with open(wav_audio_path, "rb") as f:
                
                audio_bytes = f.read()

                st.audio(audio_bytes, format="audio/wav")

            with open(audio_path, "rb") as audio_file:
                        
                st.download_button(label="Download Audio", data=audio_file, file_name="output.wav", mime="audio/mp3")
    
            st.write("Audio Generated Successfully!!!")
        
            if next_page:

                st.link_button("Next Chapter", next_page)
            
        else:

            st.error("Enter a Valid URL")

    except Exception as e:
        resp = f"The Audio Could not be Generated {e}"
        st.error(resp)

    st.session_state.loading = False

stop_time = time.time()

st.write(f"Total Time Taken - {int((stop_time-start_time)//60)} minutes and {int((stop_time-start_time)%60)} seconds")
