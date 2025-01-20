import speech_recognition as sr
import pyttsx3
import pygame
from itertools import cycle
import sys
import random
from transformers import pipeline
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json
import requests
# IBM Watson Credentials
NLU_API_KEY = 'NEsQG65-lVSPsM2-issI-NBqAE96DdqF9ORoF3_Shtkd'
NLU_URL = 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/be7753cc-37a4-4b45-b195-37b72b01cc3c'
TTS_API_KEY = 'PHytK8-NV2IxL0DuXVZE8phU6eX5onAGz3TVvg66tDnH'  
TTS_URL = 'https://api.au-syd.text-to-speech.watson.cloud.ibm.com/instances/19d8c601-c1e6-43eb-b6d7-45442e62fc2f'  

authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(version='2021-08-01', authenticator=authenticator)
nlu.set_service_url(NLU_URL)
# Initialize Text-to-Speech
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.setProperty("volume", 0.9)

# Import font module for text rendering
pygame.font.init()

# Animate Cozmo (Modified to Include Text)
def animate_cozmo():
    global current_expression, last_message
    blink_active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1 and not blink_active:
                current_expression = BLINK
                blink_active = True
                pygame.time.set_timer(pygame.USEREVENT + 2, 200)
            if event.type == pygame.USEREVENT + 2 and blink_active:
                current_expression = REGULAR
                blink_active = False
                set_blink_timer()

        screen.fill((0, 0, 0))  
        screen.blit(body_sprite, (403, 260))
        screen.blit(head_sprite, (400, 200))
        screen.blit(left_hand_sprite, (393, 264))
        screen.blit(right_hand_sprite, (465, 264))
        current_expression.rect.topleft = (410, 220)
        screen.blit(current_expression.image, current_expression.rect)
        pygame.display.flip()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Initialize conversational model (BlenderBot)
model_name = "facebook/blenderbot-400M-distill"
nlp_pipeline = pipeline("text2text-generation", model=model_name)

# Initialize Pygame and Cozmo animation
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Cozmo Assistant Animation")
TILE_SIZE = 2.5

# Load Cozmo sprites
head_sprite = pygame.image.load("Head.svg")
left_hand_sprite = pygame.image.load("Left Hand.svg")
right_hand_sprite = pygame.image.load("Right Hand.svg")
body_sprite = pygame.image.load("body.svg")

# Define expressions
class Expression(pygame.sprite.Sprite):
    def __init__(self, data):
        super().__init__()
        self.image = pygame.Surface((len(data[0]), len(data)), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))
        x = y = 0
        for row in data:
            for col in row:
                if col == "O":
                    self.image.set_at((x, y), pygame.Color("dodgerblue"))
                x += 1
            y += 1
            x = 0
        self.image = pygame.transform.scale(
            self.image, (TILE_SIZE * len(data[0]), TILE_SIZE * len(data))
        )
        self.rect = self.image.get_rect()

REGULAR = Expression([
    "                     ",
    "                     ",
    "    OOOO     OOOO    ",
    "   OOOOOO   OOOOOO   ",
    "   OOOOOO   OOOOOO   ",
    "    OOOO     OOOO    ",
    "                     ",
    "                     ",
])

QUESTION = Expression([
    "                     ",
    "                     ",
    "    OOOO             ",
    "   OOOOOO    OOOO    ",
    "   OOOOOO   OOOOOO   ",
    "    OOOO     OOOO    ",
    "                     ",
    "                     ",
])

GLEE = Expression([
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "    OOOO     OOOO    ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
])
SCARED = Expression([
    "                     ",
    "                     ",
    "     OOOO   OOOO     ",
    "    OOOOO   OOOOO    ",
    "   OOOOOO   OOOOOO   ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
])
ANGRY = Expression([
    "                     ",
    "                     ",
    "   OOO        OOO    ",
    "   OOOO      OOOO    ",
    "   OOOOOO  OOOOOO    ",
    "   OOOOOO  OOOOOO    ",
    "                     ",
    "                     ",
])
HAPPY = Expression([
    "                     ",
    "                     ",
    "    OOOO     OOOO    ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
])
SAD = Expression([
    "                     ",
    "                     ",
    "      OOO   OOO      ",
    "     OOOO   OOOO     ",
    "   OOOOOO   OOOOOO   ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
])
UNIMPRESSED= Expression([
    "                     ",
    "                     ",
    "   OOOOOO   OOOOOO   ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
])
BORED = Expression([
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "   OOOOOO   OOOOOO   ",
    "    OOOO     OOOO    ",
    "                     ",
    "                     ",
])
ANNOYED = Expression([
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "   OOOOOO   OOOOOO   ",
    "    OOOO             ",
    "                     ",
    "                     ",
])
FOCUSED = Expression([
    "                     ",
    "                     ",
    "                     ",
    "    OOOOO    OOOOO   ",
    "    OOOOOO  OOOOOO   ",
    "                     ",
    "                     ",
    "                     ",
])
WORRIED= Expression([
    "                     ",
    "                     ",
    "      OOO   OOO      ",
    "     OOOO   OOOO     ",
    "   OOOOOO   OOOOOO   ",
    "   OOOOOO   OOOOOO   ",
    "                     ",
    "                     ",
])
BLINK= Expression([
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
    "                     ",
])

expressions = cycle([REGULAR])
current_expression = next(expressions)

def set_blink_timer():
    blink_interval = random.randint(2, 5) * 1000
    pygame.time.set_timer(pygame.USEREVENT + 1, blink_interval)

set_blink_timer()

# Map emotions to expressions
emotion_to_expression = {
    "happy": GLEE,
    "confused": QUESTION,
    "neutral": REGULAR,
    "sadness": SAD,
    "anger": ANGRY,
    "feared": SCARED,
    "joy": HAPPY,
    "disgust": UNIMPRESSED,
    "surprise": QUESTION,
    "trust": FOCUSED,
    "anticipation": WORRIED,
    "annoyed": ANNOYED,
    "bored": BORED
}

# Detect emotions using IBM Watson
def detect_emotion(text):
    global current_expression
    try:
        # Call Watson NLU to analyze text emotions
        response = nlu.analyze(
            text=text,
            features=Features(emotion=EmotionOptions())
        ).get_result()

        # Extract emotions
        emotions = response.get('emotion', {}).get('document', {}).get('emotion', {})
        print(f"Detected Emotions: {json.dumps(emotions, indent=2)}")

        if emotions:
            # Determine primary emotion by score
            primary_emotion = max(emotions, key=emotions.get)
            print(f"Primary Emotion: {primary_emotion} (Score: {emotions[primary_emotion]:.2f})")

            # Map to Cozmo's expressions
            current_expression = emotion_to_expression.get(primary_emotion)
        else:
            print("No emotions detected. Defaulting to neutral.")
            current_expression = REGULAR
    except Exception as e:
        print(f"Error detecting emotion: {e}")
        current_expression = REGULAR

# Generate response using BlenderBot
def generate_response(user_input):
    try:
        response = nlp_pipeline(user_input, max_length=100, do_sample=True)
        return response[0]["generated_text"]
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I can't respond to that at the moment."

# Speech-to-text function
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            return None

# Animate Cozmo
def animate_cozmo():
    global current_expression
    blink_active = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.USEREVENT + 1 and not blink_active:
                current_expression = BLINK
                blink_active = True
                pygame.time.set_timer(pygame.USEREVENT + 2, 200)
            if event.type == pygame.USEREVENT + 2 and blink_active:
                current_expression = REGULAR
                blink_active = False
                set_blink_timer()

        screen.blit(body_sprite, (403, 260))
        screen.blit(head_sprite, (400, 200))
        screen.blit(left_hand_sprite, (393, 264))
        screen.blit(right_hand_sprite, (465, 264))
        current_expression.rect.topleft = (410, 220)
        screen.blit(current_expression.image, current_expression.rect)
        pygame.display.flip()

# Assistant function
def assistant():
    speak("Hello, I am Cozmo! How can I assist you today?")
    while True:
        user_input = listen()
        if user_input:
            response = generate_response(user_input)
            print(f"Assistant: {response}")
            speak(response)
            detect_emotion(response)
            if "bye" in user_input:
                speak("Goodbye! Have a nice day!")
                break
        else:
            speak("I couldn't hear you. Can you repeat that?")

# Main execution
if __name__ == "__main__":
    from threading import Thread
    Thread(target=animate_cozmo).start()
    assistant()
