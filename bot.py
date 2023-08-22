import discord
from discord.ext import commands
import os
import eventHandler
import pymongoManager
from keep_alive import keep_alive

def isAdmin(ctx):
  return ctx.author.guild_permissions.administrator

def updateChannelData(message, data):
  pymongoManager.update_collection('active_channels', message.guild.id, {'server_name': str(message.guild.name), 'channel_data': data})

def getLastChannelUser(message):
  rawData = pymongoManager.find_in_collection('active_channels', message.guild.id)

  if rawData:
    return rawData['channel_data']

  return None

# main bot driver function
def runDiscordBot():
  # initialization
  intents = discord.Intents.default()
  intents.typing = True
  intents.messages = True
  # intents.message_content = True    # needed for replit

  bot = commands.Bot(command_prefix='!', intents=intents)
  eventHandler.init(bot)

  # commands
  @bot.command(name='init')
  @commands.check(isAdmin)
  async def init(ctx):
    lastChannelUser = getLastChannelUser(ctx)

    # setting the lastChannelUser to a dictionary if null
    if not lastChannelUser:
      lastChannelUser = {}

    # indication of existence of the new channel
    if not (str(ctx.channel) in lastChannelUser.keys()):
      lastChannelUser[str(ctx.channel.id)] = None

      updateChannelData(ctx, lastChannelUser)

      # visual feedback
      await ctx.channel.send('`This channel is now a one-word-story channel!`')

  @bot.command(name='disable')
  @commands.check(isAdmin)
  async def disable(ctx):
    lastChannelUser = getLastChannelUser(ctx)

    if lastChannelUser and str(ctx.channel.id) in lastChannelUser.keys():
      del lastChannelUser[str(ctx.channel.id)]
      updateChannelData(ctx, lastChannelUser)

    await ctx.channel.send('`One-word-stories have been disabled for this channel!`')

  # trigger declaration
  @bot.event
  async def on_ready():
    await eventHandler.handleReady()

  @bot.event
  async def on_message(message):
    await bot.wait_until_ready()

    lastChannelUser = getLastChannelUser(message)

    # the bot can only send messages to channels that it has been initialized for
    if lastChannelUser and str(message.channel.id) in lastChannelUser.keys():
      # responding to the message
      lastUser = lastChannelUser[str(message.channel.id)]

      success = await eventHandler.handleMessage(message, lastUser)

      # updating the last user for the channel
      if success:
        lastChannelUser[str(message.channel.id)] = str(message.author)

        # updating the active users in the DB, or adding the active users if
        # it doesn't already exist
        updateChannelData(message, lastChannelUser)

    await bot.process_commands(message)

  # execution
  keep_alive()
  bot.run(os.environ['TOKEN'])
