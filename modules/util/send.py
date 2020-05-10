import asyncio


async def message(channel, msg='', embed=None):
    """
    Default function for sending messages. Encapsulates the API function call for easy updating.
    :param channel: The TextChannel object to send the message to.
    :type channel: discord.TextChannel
    :param msg: A string representing the message to be sent to the channel.
    :type msg: str
    embed Optional[:class: discord.Embed] an Embed object to send instead of a message.
    """
    if embed is None:
        time = len(msg)/4
        await channel.trigger_typing()
        await asyncio.sleep(time)
        await channel.send(msg)
    else:
        await channel.send(embed=embed)


async def reaction(message, reaction):
    """
    Default function for adding a reaction to a specified message.
    :type message: discord.Message
    :type reaction: discord.Reaction
    """

    await message.add_reaction(reaction)


async def file(channel, input_file):
    """
    Default function for sending a file.
    :param channel: The Channel to send the file to.
    :param input_file: The file itself
    :type channel: discord.Channel
    :type input_file: discord.File
    """
    await channel.send(file=input_file)


async def typing(channel):
    channel.trigger_typing()

# TODO: Make a method to handle sending an embedded table.
