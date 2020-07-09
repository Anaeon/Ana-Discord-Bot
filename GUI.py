import discord
import asyncio
import requests

from PIL import Image
from asynctk import *
from io import BytesIO
from asynctk.scrolledtext import AsyncScrolledText

from modules.data import misc

USER_ICONS = []
GUILD_ICONS = []

class GUI(AsyncTk):
    def __init__(self, asyncloop, client: discord.Client()):
        AsyncTk.__init__(self, loop=asyncloop)

        self.wm_title('Ana')
        self.msg_index = 0

        # Create a frame to put chat messages in.
        self.chat_frame = AsyncFrame(self)
        # self.chat_frame.text = AsyncScrolledText(self.chat_frame, state='disabled', width=80, height=10)
        self.chat_frame.text = AsyncScrolledText(self.chat_frame, state='disabled')
        self.chat_frame.text.tag_config('error', background='black', foreground='red')

        AsyncLabel(self.chat_frame, text='Chat Messages').pack()
        self.chat_frame.text.pack()

        # TODO: Make a text input box.

        # TODO: Make a menu to chose a server for messages.b
        guilds = client.guilds

        # TODO: Create a reset button.

        # TODO: Build the UI grid.
        self.chat_frame.grid(row=0, column=0)

    def error_message(self, message):
        self.add_chat_message(message, 'error')

    def add_chat_message(self, message, tag=None):
        fr = self.chat_frame.text
        m_guild = None if message.guild is None else message.guild.name
        m_channel = 'DM' if type(message.channel) is discord.DMChannel else message.channel.name
        m_author = message.author.name if message.author.display_name is None else message.author.display_name
        fr.config(state='normal')  # unlock the text box so it can be edited.
        if self.msg_index == 0:
            fr.insert(
                END,
                '[G:{}][C:{}][A:{}]:{}'.format(m_guild, m_channel, m_author, message.content),
                None if tag is None else tag
            )
        elif self.msg_index > 0:
            # if m_guild is not None:
                # TODO: WHY? WHY DOES THIS NOT WORK?
                # TO EARLY TO CREATE IMAGE. AsyncTk object must be created before PhotoImage() can be called, but
                # is that not what's happening on line 17? So, why can't I call it here?
                # img = Image.open(misc.CACHE_DIRECTORY + message.author.id + '.png')
                # img = GUILD_ICONS[message.guild.id]
                # print(img)
                # fr.image_create(END, img)  # insert the guild image
                # fr.window_create(END, window=AsyncLabel(fr, image=img))
            fr.insert(
                END,
                '\n[G:{}][C:{}][A:{}]:{}'.format(m_guild, m_channel, m_author, message.content),
                None if tag is None else tag
            )
        fr.config(state='disabled')  # lock the text box so it can't be edited.
        self.msg_index += 1

    async def run(self):
        while True:
            try:
                await self.tick()
            except:
                return
            await asyncio.sleep(0.01)


def on_ready(asyncloop, client: discord.Client()):
    gui = GUI(asyncloop, client)
    asyncloop.create_task(gui.run())

    for guild in client.guilds: # download the guild and client icons and update them here.
        gurl = guild.icon_url_as(format='png', size=32)
        gr = requests.get(gurl, allow_redirects=True)
        gdir = misc.CACHE_DIRECTORY + 'guildicons/'
        open(gdir + str(guild.id) + '.png', 'wb').write(gr.content)
        # GUILD_ICONS[guild.id] = PhotoImage(file=misc.CACHE_DIRECTORY + str(guild.id) + '.png')
        for user in guild.members:
            uurl = user.avatar_url_as(format='png', size=32)
            ur = requests.get(uurl, allow_redirects=True)
            udir = misc.CACHE_DIRECTORY + 'usericons/'
            open(udir + str(user.id) + '.png', 'wb').write(ur.content)

    return gui


def on_exit():
    pass
