import streamlit as st
from google import genai

# prompt to define the role of the ai
SYSTEM_PROMPT = """
You are a highly skilled cybersecurity expert assistant for a Security Operations Center (SOC).
Your role is to analyze incidents, threats, and provide clear, actionable technical guidance.
- Provide clear, actionable recommendations and mitigations.
- Use standard industry terminology (e.g., MITRE ATT&CK, CVE).
"""

# initializing the gemini ai client using the api key
try:
    client = genai.Client()
except Exception: # if initialization fails, then it prints an error message
    client = None


def get_ai_response(messages):

    # check if the AI service client is connected
    if not client:
        return "Error: AI service is unavailable. Please check the GEMINI_API_KEY setup in your secrets file."

    # makes a list to store gemini messages
    contents = []

    # loop through all messages from the Streamlit chat history.
    for message in messages:
        # translates streamlit from user and assistant to user and model
        api_role = 'user' if message["role"] == 'user' else 'model'

        # adds each message with the role and the text to the contents list
        contents.append({
            "role": api_role,
            "parts": [{"text": message["content"]}]
        })

    try:
        # calls the gemini api to generate content using the selected model and system prompt
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=contents,
            config=genai.types.GenerateContentConfig(
                # Use the SYSTEM_PROMPT to define the AI's personality.
                system_instruction=SYSTEM_PROMPT
            )
        )
        # returns only the text content of the AI reply
        return response.text

    # catch any connection or API errors and return a user-friendly message.
    except Exception as e:
        return f"API Call Error: The Gemini API returned an error: {e}"