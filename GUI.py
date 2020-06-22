import asynctk as tk
import discord
import asyncio

from asynctk.scrolledtext import AsyncScrolledText

class GUI(tk.AsyncTk):
    def __init__(self, asyncloop, client:discord.Client()):
        tk.AsyncTk.__init__(self, loop=asyncloop)

        self.chat_frame = tk.AsyncFrame(self)
        self.chat_frame.text = AsyncScrolledText(self.chat_frame, state='disabled', width=40, height=10)

        # TODO: Make a text input box.

        # TODO: Make a menu to chose a server for messages.

        # TODO: Create a reset button.
