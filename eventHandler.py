client = None

def init(c):
    global client
    client = c

async def handleReady():
    print("Bot connected")

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