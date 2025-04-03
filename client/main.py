# client/main.py

from client.components.chat import chat
from client.components.hero import hero


async def main():
    hero()
    await chat()
