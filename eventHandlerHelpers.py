import responses

async def sendMessage(message, uMessage):
  try:
    res = responses.handleResponse(uMessage)
    await message.channel.send(res)
  except Exception as e:
    print(e)