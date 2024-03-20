# Importing libraries
import chainlit as cl
import json
import openai
from openai import OpenAI
import requests
from dotenv import load_dotenv
import os

GPT_MODEL = "gpt-4-turbo-preview"
GPT_RESULT = []

# Load environment variables from .env file
load_dotenv()
# Read the API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Gets the current weather",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city name only. No country or state required",
                    },
                },
                "required": ["location"],
            },
        }
    },
]


def get_location(message):
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model=GPT_MODEL,
        response_format={"type": "text"},
        messages=[{"role": "system",
                   "content": "Don't make assumptions about what values to plug into functions. Ask for location if it is not provided"},
                  {"role": "user", "content": message}
                  ],
        tools=tools
    )
    print("Response:", response)
    GPT_RESULT.append(response.choices[0].message.content)
    loc_ = json.loads(response.json())["choices"][0]["message"]['tool_calls'][0]["function"]['arguments']
    loc = json.loads(loc_)["location"]

    return loc



def get_weather(loc):
    url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "APPID": "3dbbcaefaee14eb4243faed7b7ccb28d"
    }

    response = requests.get(url, params=params)
    return response.text


def extract_weather(weather_api_response):
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system",
             "content": "You are weather API assistant.Round the temperature. Provide short answer like this: The temperature in Yereven is 5 celcius."},
            {"role": "user",
             "content": f"What is the temerature in celcius in the location based on this: {weather_api_response}"}
        ]
    )
    return response.choices[0].message.content


def translate_into_am(text):

    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
      model = GPT_MODEL,
      messages = [
        {"role": "system", "content": """You are professional translator. Translate into the language instructed.
        Translate any numbers or symbols into text.
        Original: The temperature in Yerevan is 10 Celsius.
        Translation: Երևանում ջերմաստիճանը տասը աստիճան ցելսիուս է։
        Original: The temperature in Tavush is 12 Celsius.
        Translation: Տավուշում ջերմաստիճանը տասներկու աստիճան ցելսիուս է։

        """},
        {"role": "user", "content": f"Translate into Armenian this text: {text}"}
      ]
    )
    return response.choices[0].message.content


def convert_TTS(text_am):
    client = OpenAI(api_key=openai.api_key)

    text_to_speech = client.audio.speech.create(
        model="tts-1-hd",
        voice="echo",
        input=text_am
    )
    return text_to_speech.stream_to_file("weather.mp3")


def gen_image_from_text(text):
    client = OpenAI(api_key=openai.api_key)

    image_gen = client.images.generate(
        model="dall-e-3",
        prompt=f"Generate realistic image based on this text:{text}. Depict temperature as a number as well.",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = image_gen.data[0].url
    response = requests.get(image_url)
    return response, image_url


def extract_text_from_image(image_url):
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system",
             "content": "You are text extractor from image. If there is no text, output there is no text in the image."},
            {"role": "user",
             "content": [
                 {
                     "type": "text",
                     "text": "Output text from the image."
                 },
                 {
                     "type": "image_url",
                     "image_url": {
                         "url": image_url
                     }
                 }
             ]
             }
        ]
    )
    return response.choices[0].message.content


@cl.on_message
async def main(message: cl.Message):
    # Your custom logic goes here...
    message = message.content
    loc = 0
    while True:
        try:
            loc = get_location(message)
            weather_api_response = get_weather(loc)
            text = extract_weather(weather_api_response)
            text_am = translate_into_am(text)
            convert_TTS(text_am)
            image, image_url = gen_image_from_text(text)
            extraction = extract_text_from_image(image_url)

            image = cl.Image(url=image_url, name=loc, display="inline")
            audio = cl.Audio(name="weather.mp3", path="weather.mp3", display="inline")
            elements = [image, audio]
            await cl.Message(content=f"{text}{text_am}{extraction}", elements=elements).send()
            break
        except:
            await cl.Message(content=GPT_RESULT[-1]).send()
            break

