from openai import OpenAI
from sshhhh import OPENAI_API_KEY
from selenium import webdriver as wd

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_image(prompt):
  response = client.images.generate(
    model="dall-e-2",
    prompt=prompt,
    size="1024x1024",
    quality="standard",
    n=1,
  )

  image_url = response.data[0].url
  return image_url