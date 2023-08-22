client = None

def init(c):
    global client
    client = c

async def handleReady():
    print("Bot connected")

# users' messages are deleted
# returns True if the function succeeded
# async def handleMessage(message, lastUser):
#     try:
#         # storing message data
#         uMessage = str(message.content).strip()
#
#         # exit if the bot sends a message
#         if message.author == client.user:
#             raise Exception("Invalid message: bot response")
#
#         # exit if the same user has sent consecutive messages
#         if str(message.author) == lastUser:
#             await message.delete()
#             raise Exception("Invalid message: consecutive user")
#
#         # exit on whitespace
#         if len(uMessage.split('\t')) != 1 or len(uMessage.split('\n')) != 1 or len(uMessage.split(' ')) != 1:
#             await message.delete()
#             raise Exception("Invalid message: contains whitespace")
#
#         # updating message history
#         history = [message async for message in message.channel.history(limit=3)]
#
#         # deleting user messages and any 'last messenger' messages
#         # Note: we are guaranteed that a block of bot messages ends with a 'last messenger' message
#         if len(history) == 3 and history[0].author != client.user and history[1].author == client.user and history[2].author == client.user:
#             await history[0].delete()
#             await history[1].delete()
#         else:  # deleting the user message
#             await message.delete()
#
#         # sending messages
#         await helpers.sendMessage(message, uMessage)
#         await helpers.sendMessage(message, "\n`Last messenger: @" + str(message.author) + "`")
#     except:
#         return False
#
#     return True

# users' messages are kept
async def handleMessage(message, lastUser):
    try:
        # storing message data
        uMessage = str(message.content).strip()

        # exit if the bot sends a message
        if message.author == client.user:
            raise Exception("Invalid message: bot response")

        # exit if the same user has sent consecutive messages
        if str(message.author) == lastUser:
            await message.delete()
            raise Exception("Invalid message: consecutive user")

        # exit on whitespace
        if len(uMessage.split('\t')) != 1 or len(uMessage.split('\n')) != 1 or len(uMessage.split(' ')) != 1:
            await message.delete()
            raise Exception("Invalid message: contains whitespace")
    except:
        return False

    return True