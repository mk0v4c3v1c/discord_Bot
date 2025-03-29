import AIChat
import openai
import os
from dotenv import load_dotenv
from typing import Optional
import logging

logger = logging.getLogger(__name__)

load_dotenv()


def __init__(self):
    # Initialize the AI chat service with configuration.
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    openai.api_key = api_key

    # Configurable parameters
    self.model = "gpt-4"
    self.max_tokens = 150
    self.temperature = 0.7


def generate_response(self, prompt: str, conversation_history: Optional[list] = None) -> str:
    # Generate AI response to the given prompt.

    try:
        messages = conversation_history or []
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        return response["choices"][0]["message"]["content"]
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        return "Sorry, I'm having trouble processing your request right now."
    except Exception as e:
        logger.error(f"Unexpected error in generate_response: {e}")
        return "An unexpected error occurred. Please try again later."


# Singleton instance for easy access
ai_chat_service = AIChat()
