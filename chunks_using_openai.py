'''
from dotenv import load_dotenv
import os

load_dotenv()  # loads .env
api_keys = os.getenv("OPENAI_API_KEY")

from openai import OpenAI
import os

# If you set OPENAI_API_KEY as env variable, you don't need to pass it here.
client = OpenAI(api_key=os.getenv("api_keys"))

def transcribe_to_english(audio_path: str) -> str:
    """
    Transcribe first 10 seconds of an audio file (mp3, wav, m4a, etc.)
    Spoken language can be Hindi or anything else.
    Output will be English text.
    """
    with open("audios/1_Stranger_Things - Episode01.mp3", "rb") as f:
        transcript = client.audio.transcriptions.create(
            file=f,
            model="whisper-1",   # latest speech-to-text model
            response_format="text",      # return plain text
            # Optional: force translation to English
            # If you want original language, remove this line.
            language="en"                
        )
    return transcript

if __name__ == "__main__":
    audio_file = "audios/1_Stranger_Things - Episode01.mp3"   # change to your path
    text = transcribe_to_english(audio_file)
    print("---- TRANSCRIPT (ENGLISH) ----")
    print(text)

    
    '''
