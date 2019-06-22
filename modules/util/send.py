async def message(channel, message):
    """
    Default function for sending messages. Encapsulates the API function call for easy updating.
    :type channel: discord.TextChannel
    :type message: str
    """

    await channel.send(message)


async def reaction(message, reaction):
    """
    Default function for adding a reaction to a specified message.
    :type message: discord.Message
    :type reaction: discord.Reaction
    """

    await message.add_reaction(reaction)


async def file(channel, input_file):

    await channel.send(file=input_file)


async def typing(channel):
    # TODO: Check the API for the new client.send_typing() method and pass it here.
    pass

# TODO: Make a method to handle sending an embedded table.
