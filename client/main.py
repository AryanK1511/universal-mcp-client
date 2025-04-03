# client/main.py

from client.components.chat import chat
from client.components.hero import hero
from client.components.model_selector import model_selector


def main():
    hero()
    model_selector()
    chat()
