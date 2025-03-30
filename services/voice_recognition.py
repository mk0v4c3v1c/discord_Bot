import speech_recognition as sr
import discord
import io
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class VoiceRecognition:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True

    async def process_voice(self, audio_data: bytes) -> Optional[str]:
        # Convert voice audio to text
        try:
            audio_file = io.BytesIO(audio_data)
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)

            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            logger.warning("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            logger.error(f"Could not request results from Google Speech Recognition service; {e}")
        except Exception as e:
            logger.error(f"Error processing voice: {e}")
        return None


voice_service = VoiceRecognition()