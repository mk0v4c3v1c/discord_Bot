import openai
import os
from dotenv import load_dotenv
from typing import Optional, List, Dict
import logging
from database.db_handler import db


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
    self.max_tokens = 250
    self.temperature = 0.7
    self.max_history = 5 # keep last 5 messages in memory

    def _get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history from database"""
        history = db.execute(
            "SELECT history FROM ai_conversations WHERE user_id = ?",
            (user_id,)
        ).fetchone()

        return json.loads(history[0]) if history else []

    def _save_conversation_history(self, user_id: str, history: List[Dict]) -> None:
        """Save conversation history to database"""
        db.execute(
            "INSERT OR REPLACE INTO ai_conversations (user_id, history) VALUES (?, ?)",
            (user_id, json.dumps(history))
        )

    def generate_response(self, user_id: str, prompt: str) -> str:
        """Generate AI response with conversation memory"""
        try:
            # Get conversation history
            history = self._get_conversation_history(user_id)

            # Add new user message
            history.append({"role": "user", "content": prompt})

            # Keep only the most recent messages
            history = history[-self.max_history:]

            # Generate response
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    *history
                ],
                max_tokens=self.max_tokens,
                temperature=self.temperature
            )

            # Get AI response
            ai_response = response["choices"][0]["message"]["content"]

            # Add AI response to history
            history.append({"role": "assistant", "content": ai_response})
            self._save_conversation_history(user_id, history)

            return ai_response

        except openai.error.OpenAIError as e:
            logger.error(f"OpenAI API error: {e}")
            return "Sorry, I'm having trouble processing your request right now."
        except Exception as e:
            logger.error(f"Unexpected error in generate_response: {e}")
            return "An unexpected error occurred. Please try again later."

    def clear_memory(self, user_id: str) -> bool:
        """Clear conversation history for a user"""
        try:
            db.execute(
                "DELETE FROM ai_conversations WHERE user_id = ?",
                (user_id,)
            )
            return True
        except Exception as e:
            logger.error(f"Error clearing memory: {e}")
            return False


# Singleton instance
ai_chat = AIChat()
