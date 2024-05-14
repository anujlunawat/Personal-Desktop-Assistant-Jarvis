import openai
from sshhhh import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def chat_with_gpt(prompt, file=True):
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{'role': "user", "content": prompt}]
    )
    if file: return save_to_file(response.choices[0].message.content.strip(), prompt)
    else: return response.choices[0].message.content.strip()

def save_to_file(r, prompt):
    reply = f"OpenAI response for prompt: {prompt.capitalize()}\n" + "*" * 25 + "\n\n"
    reply += r

    with open(fr"assets\OpenAI\{prompt}.txt", mode='w') as file:
        file.write(reply)
    return fr"assets\OpenAI\{prompt}.txt"