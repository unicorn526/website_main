import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generateImg(text, sz):
    img = client.images.generate(
        model="gpt-image-1",
        prompt=text,
        n=1,
        size=sz,
        quality="medium"
    )

    image_base64 = img.data[0].b64_json
    return f"data:image/png;base64,{image_base64}"
