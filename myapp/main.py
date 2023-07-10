import speech_recognition as sr
import time
from google.cloud import translate_v2 as translate
from google.oauth2.service_account import Credentials
from gtts import gTTS
from pygame import mixer
import tempfile
import os

credentials = Credentials.from_service_account_file("service-account.json")

# Create a recognizer instance
recognizer = sr.Recognizer()

# Timeout constants
PAUSE_THRESHOLD = 3  # Seconds of silence before transcribing
MAX_RECORDING_LENGTH = 30  # Maximum length of a single recording

# Create a translation client
translate_client = translate.Client(credentials=credentials)

def transcribe_audio(audio):
    # This function could be expanded to handle errors, retries, etc.
    return recognizer.recognize_google(audio)

def translate_text(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

def main():
    # Create a microphone instance
    with sr.Microphone() as mic:
        print("Starting transcription. Speak into the microphone...")

        start_time = time.time()
        current_transcription = ""

        while True:
            # Listen for audio
            try:
                audio = recognizer.listen(mic, timeout=PAUSE_THRESHOLD, phrase_time_limit=PAUSE_THRESHOLD)
            except sr.WaitTimeoutError:
                print("Timeout error, no speech detected")
                continue

            try:
                # Try to transcribe the audio
                transcription = transcribe_audio(audio)
                if transcription:
                    translation = translate_text(transcription, 'tl')

                    # Form the output string
                    english_output = f"{transcription} in Tagalog is"
                    tagalog_output = f"{translation}"

                    # Create tts objects for both parts
                    tts_english = gTTS(english_output, lang="en")
                    tts_tagalog = gTTS(tagalog_output, lang="tl")

                    # Save the tts objects to temporary files
                    with tempfile.NamedTemporaryFile(delete=True) as fp_english, tempfile.NamedTemporaryFile(delete=True) as fp_tagalog:
                        tts_english.save(f"{fp_english.name}.mp3")
                        tts_tagalog.save(f"{fp_tagalog.name}.mp3")

                        # Play the English part
                        mixer.init()
                        mixer.music.load(f"{fp_english.name}.mp3")
                        mixer.music.play()
                        while mixer.music.get_busy():
                            # Wait for English part to finish
                            time.sleep(0.1)

                        # Then play the Tagalog part
                        mixer.music.load(f"{fp_tagalog.name}.mp3")
                        mixer.music.play()

                        print(f"{transcription} in Tagalog is: {translation}")


                else:
                    print("Silence...")

                # Output the current transcription
                print("Collected Transcription:", current_transcription)
                current_transcription = ""

            except sr.UnknownValueError:
                print("Could not understand audio")

            # Check if the maximum recording length has been reached
            if time.time() - start_time >= MAX_RECORDING_LENGTH:
                if current_transcription:
                    # If there's any transcription left, output it
                    print("Final Transcription:", current_transcription)
                break

if __name__ == "__main__":
    main()


