import time
import logging
from groq import Groq, GroqError
from src.config import settings

logger = logging.getLogger(__name__)

class GroqClient:
    def __init__(self):
        """
        Initialize the Groq client. If settings.GROQ_API_KEY is not defined,
        the SDK will automatically fall back to the GROQ_API_KEY environment variable.
        """
        api_key = settings.GROQ_API_KEY if settings.GROQ_API_KEY else None
        self.client = Groq(api_key=api_key)

    def get_recommendations(self, system_prompt: str, user_prompt: str) -> str:
        """
        Sends the system and user prompts to the Groq API using the configured model.
        Forces JSON output format and incorporates retry logic with exponential backoff on errors.
        """
        max_retries = 2
        backoff_seconds = 1.0
        
        for attempt in range(max_retries + 1):
            try:
                # Reduce temperature slightly on retry to discourage deviation/hallucination
                temp = settings.GROQ_TEMPERATURE if attempt == 0 else 0.1
                
                logger.info(f"Invoking Groq model '{settings.GROQ_MODEL}' (Attempt {attempt + 1})...")
                
                response = self.client.chat.completions.create(
                    model=settings.GROQ_MODEL,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=temp,
                    response_format={"type": "json_object"}
                )
                
                return response.choices[0].message.content
            except GroqError as e:
                logger.warning(f"Groq API call failed on attempt {attempt + 1}: {e}")
                if attempt < max_retries:
                    logger.info(f"Retrying in {backoff_seconds} seconds...")
                    time.sleep(backoff_seconds)
                    backoff_seconds *= 2
                else:
                    logger.error("Max retries exceeded for Groq API call.")
                    raise e
