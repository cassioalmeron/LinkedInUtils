import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key)

system_prompt = """You are a helpful assistant that generates comments for a given text.
The comments should be in the same language as the text, even though the observations are in a different language."""

def get_user_prompt(text : str, tone : str, observations : str) -> str:
    user_prompt = f"""Please generate a professional LinkedIn comment for the following post:

<Content>
  {text}
</Content>
<Tone>
  {tone}
</Tone>
<Observations>
  {observations}
</Observations>

Please provide a single, well-crafted comment that would be appropriate for LinkedIn."""
    return user_prompt

def request_openai(text : str, tone : str, observations : str) -> str:
    user_prompt = get_user_prompt(text, tone, observations)
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return openai_response.choices[0].message.content