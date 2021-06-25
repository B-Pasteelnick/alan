import discord
from discord.ext import commands
import os
import asyncio

client = discord.Client()
token = os.getenv("TOKEN")
client.state = "ready"
client.activeChannels = []

async def self_edit(message):
  m = message.content
  for i in m:
    m = m[1:]
    await asyncio.sleep(1)
    if not m: await message.edit('Don’t strain. Better to forget, first.')
    else: await message.edit(content=m)

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
      message.content = message.content.replace(' ', '')
      

      #permRole = discord.utils.get(message.guild.roles, name='Normie')
      #if permRole not in message.author.roles:
      #  await message.channel.send('You don\'t have the right permissions.')
      #  return

      #elif message.content == ('normie'):
      #  role = discord.utils.get(message.guild.roles, name='Normie')
      #  await message.author.add_roles(role)

      #elif message.content == ('unnormie'):
      #  role = discord.utils.get(message.guild.roles, name='Normie')
      #  await message.author.remove_roles(role)

      if message.content == ('8622985399'):
        m = await message.channel.send('A phone number, maybe? It\'s all a mess.')
        await self_edit(m)

      elif message.content == ('name'):
        await message.channel.send('If we could remember that, we would have.')

      elif message.content == ('rules'):
        await message.channel.send('The parameters of life. This may help us remember who we are - but they may change with time, if only slightly. https://docs.google.com/document/d/1-V_DE5DHX8zRxWVKk6y_KeJvukQjswfMaqXpPSskfLA/edit?usp=sharing')

      elif message.content == ('test'):
        await message.channel.send('Perhaps it is.')

      elif message.content == ('echoesandmemories'):
        await message.channel.send('Something does stir at the name. +1 Despair.')

      elif message.content == ('hope\'speak') or message.content == ('hopespeak') or message.content == ('ultimate') or message.content == ('danganronpa'):
        await message.channel.send('A fantasy, and nothing more.')

      elif message.content == ('echo'):
        await message.channel.send('Is that all we are?')

      elif message.content == ('game'):
        await message.channel.send('The stakes are too high.')

      elif message.content == ('guide') or message.content == ('guides'):
        await message.channel.send('Who are they? What do they know?')

      elif message.content == ('personalchats'):
        await message.channel.send('It feels personal.')

      elif message.content == ('privatechannels'):
        await message.channel.send('Is it private, here? What lurks?')

      elif message.content == ('explore') or message.content == ('lookaround') or message.content == ('gonorth') or message.content == ('goeast') or message.content == ('gowest') or message.content == ('gosouth'):
        await message.channel.send('The flame captures your attention... but first you must remember who you are.')

      elif message.content == ('help'):
        await message.channel.send('We got ourselves into this mess. It\'s up to us to get out of it.')

      elif message.content == ('remember'):
        bars = '\n**-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------**\n'
        first = 'You awaken alone in a shadowed room. A flickering, sourceless, flame, mere inches away, makes you aware of the drifting grey shape of this place. You cannot see the dark edges that skulk from the light... or perhaps you cannot remember. Memory begins to flood back, though jagged holes and shifting faces keep you from recalling clear. You remember *what you are*. You do not remember **why you are here**. You remember *who you were*. You do not remember **your name**. You remember *what you can do*. You do not remember **what you must do**.\n\nSomething... powerful... glints in the fire. Your hand, outstretched, runs and billows like smoke. You cannot reach it, not yet. When your memories - those that have not deserted you - are solid in your mind, then your body will be ready to bear the heat of the crucible!'

        if message.channel in client.activeChannels:
          await message.channel.send("Don’t strain. Better to forget, first.")
          return

        m = await message.channel.send(bars + first + bars)
        
        bold = False;
        italics = False;
        client.activeChannels.append(message.channel)

        await asyncio.sleep(10)

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
          
          await asyncio.sleep(1)
          if (first == '' or first[1:] == ''):
            await m.edit(content="You seem to have forgotten...")
            client.activeChannels.remove(message.channel)
            return
          first = first[1:]
          if first.startswith(" "): first = first[1:]

          if bold and not first.startswith("**"): await m.edit(content= bars + "**" + first + bars)
          elif italics and not first.startswith("*"): await m.edit(content= bars + "*" + first + bars)
          else: await m.edit(content=bars + first + bars)
        client.activeChannels.remove(message.channel)


      else:
        await message.channel.send(oMess[1:])

client.run(token)
