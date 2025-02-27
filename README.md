# Sonus Flow
## For a smooth, natural listening experience.

Sonus Flow is a Web Application built using Streamlit and deployed via Streamlit Community Cloud.

### **What is Sonus Flow?**  
Sonus Flow is a personal project designed to convert light novel chapters into audio files seamlessly. It allows users to take any chapter from [Novel Bin](https://novelbin.com/) and generate an audio file for listening.  

### **Features:**  
- Scrapes and retrieves novel content using **requests** and **BeautifulSoup**.  
- Converts text to speech using **Google Text-to-Speech (GTTS)**.  
- Provides an online streaming experience using **Streamlit** and **pydub (ffmpeg)**.  
- Includes **Next Chapter** and **Download** buttons for a seamless reading experience.  

### **Tech Stack:**  
- **Python**  
- **Streamlit** (for Web UI)  
- **Requests & BeautifulSoup** (for web scraping)  
- **Google Text-to-Speech (GTTS)** (for audio conversion)  
- **pydub & ffmpeg** (for handling audio playback)  

### **Installation & Usage**  

To install and run it locally:  
``` sh
git clone https://github.com/sreerajchintham/Sonus-Flow.git  
cd sonus-flow  
pip install -r requirements.txt  
streamlit run app.py 
```


