import discord
from discord.ext import commands
import os
import asyncio

client = discord.Client()
token = os.getenv("TOKEN")
client.state = "ready"

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.guild:
      await message.channel.send('Not here. Go back to the server.')
      return

    oMess = message.content
    message.content = message.content.casefold()

    #if 'alan' in message.content:
    #  await message.add_reaction('👋')

    if message.content.startswith('&'):

      message.content = message.content[1:]
      print(message.content)
      

      #permRole = discord.utils.get(message.guild.roles, name='Normie')
      #if permRole not in message.author.roles:
      #  await message.channel.send('You don\'t have the right permissions.')
      #  return


      if message.content == ('hello'):
        await message.channel.send('Hello!')
    
      elif message.content == ('dm'):
        await message.author.send('Here I am!')

      #elif message.content == ('normie'):
      #  role = discord.utils.get(message.guild.roles, name='Normie')
      #  await message.author.add_roles(role)

      #elif message.content == ('unnormie'):
      #  role = discord.utils.get(message.guild.roles, name='Normie')
      #  await message.author.remove_roles(role)

      elif message.content == ('8622985399'):
        await message.channel.send('Looks like a phone number to me.')

      elif message.content == ('help'):
        await message.channel.send('You got yourself into this mess. You\'ll have to get yourself out.')

      elif message.content == ('remember'):
        first = 'You awaken alone in a shadowed room. A flickering, sourceless, flame, mere inches away, makes you aware of the drifting grey shape of this place. You cannot see the dark edges that skulk from the light... or perhaps you cannot remember. Memory begins to flood back, though jagged holes and shifting faces keep you from recalling clear. You remember *what you are*. You do not remember **why you are here**. You remember *who you were*. You do not remember **your name**. You remember *what you can do*. You do not remember **what you must do**.\n\nSomething... powerful... glints in the fire. Your hand, outstretched, runs and billows like smoke. You cannot reach it, not yet. When your memories - those that have not deserted you - are solid in your mind, then your body will be ready to bear the heat of the crucible!'

        m = await message.channel.send(first)
        await asyncio.sleep(10)

        while (client.state != "ready"):
          await asyncio.sleep(10)
        bold = False;
        italics = False;
        client.state = "busy"

        for i in first:
          while first.startswith ('\n'):
            first = first[2:]

          if first.startswith('**') and not bold:
            bold = True
            first = first[2:]
          elif first[1:].startswith('**') and bold:
            bold = False
            first = first[0] + first[3:]
          elif first.startswith('*') and not italics:
            italics = True
            first = first[1:]
          elif first[1:].startswith('*') and italics:
            italics = False
            first = first[0] + first[2:]
          
          await asyncio.sleep(.5)
          if (first == '' or first[1:] == ''):
            await m.edit(content="You seem to have forgotten...")
            client.state = "ready"
            return
          first = first[1:]
          if first.startswith(" "): first = first[1:]

          if bold and not first.startswith("**"): await m.edit(content= "**" + first)
          elif italics and not first.startswith("*"): await m.edit(content= "*" + first)
          else: await m.edit(content=first)
        client.state = "ready"

      else:
        await message.channel.send(oMess[1:])

client.run(token)