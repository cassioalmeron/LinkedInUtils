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

def request_openai(user_prompt : str) -> str:
    openai_response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return openai_response.choices[0].message.content