import discord
from discord.ext import commands
import os
import asyncio
import mysql.connector
from getpass import getpass
from mysql.connector import connect, Error

client = discord.Client()
token = os.getenv("TOKEN")
client.state = "ready"
client.activeChannels = []
client.allPCs = [853698538473914418, 853703038644912158, 858164604719071253, 858164641586216981, 858251891049496577, 858478351819866143, 858885465444712518, 853826338482028574, 853826359838244874, 853703410620301352, 853826398799134750, 853826418630328340, 858353300885602364, 858425078390456330, 861889058892283915, 862144551581384715]
client.ASideChannels = [853698538473914418, 853703038644912158, 858164604719071253, 858164641586216981, 858251891049496577, 858478351819866143, 858885465444712518, 861889058892283915]
client.BSideChannels = [853826338482028574, 853826359838244874, 853703410620301352, 853826398799134750, 853826418630328340, 858353300885602364, 858425078390456330, 862144551581384715]

try:
  connection = connect(
    host=os.getenv("DBHOST"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASS"),
    database="pxjxsg6c1d91xf93",
  )
  print(connection)
  with connection.cursor() as cursor:
    cursor.execute('''
      CREATE TABLE Archetypes (
        Side varchar(1),
        Archetype varchar(100)
      );
      ''')
    connection.commit()
except Error as e:
    print(e)



async def self_edit(message):
  await asyncio.sleep(5)
  m = message.content
  for i in m:
    m = m[1:]
    await asyncio.sleep(1)
    if not m:
      await message.edit(content='You seem to have forgotten...')
      return
    await message.edit(content=m)

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

      checkGuide = discord.utils.get(message.guild.roles, name='Guides')
      if checkGuide in message.author.roles and message.content.startswith('announceall'):
        for i in client.allPCs:
          await client.get_channel(i).send("ANNOUNCEMENT: \n" + oMess[12:])
        return
      elif checkGuide in message.author.roles and message.content.startswith('announceaside'):
        for i in client.ASideChannels:
          await client.get_channel(i).send("ANNOUNCEMENT: \n" + oMess[14:])
        return
      elif checkGuide in message.author.roles and message.content.startswith('announcebside'):
        for i in client.BSideChannels:
          await client.get_channel(i).send("ANNOUNCEMENT: \n" + oMess[14:])
        return


      if checkGuide in message.author.roles and message.content.startswith('adda archetype'):
        connection.cursor().execute("INSERT INTO archetypes (Side, Archetype) VALUES (%s, %s)", ("A", oMess[16:]))
        connection.commit()
        await message.channel.send("Added " + oMess[16:] + " to A Side")
        return
      elif checkGuide in message.author.roles and message.content.startswith('addb archetype'):
        connection.cursor().execute("INSERT INTO archetypes (Side, Archetype) VALUES (%s, %s)", ("B", oMess[16:]))
        connection.commit()
        await message.channel.send("Added " + oMess[16:] + " to B Side")
        return
      elif checkGuide in message.author.roles and message.content.startswith('archetype replace'):
        args = oMess.split("\"")
        connection.cursor().execute("UPDATE archetypes SET Archetype = %s WHERE Archetype = %s", (args[3], args[1]))
        connection.commit()
        return

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

      elif message.content == ('archetypecheck'):
        if message.channel.id in client.ASideChannels:
          with connection.cursor() as cursor:
            cursor.execute("SELECT Archetype FROM archetypes WHERE Side = 'A'")
            toSend = ""
            for i in cursor.fetchall():
              for e in i:
                toSend += e + ", "
            m = await message.channel.send(toSend[:-2])
            await self_edit(m)
        elif message.channel.id in client.BSideChannels:
          with connection.cursor() as cursor:
            cursor.execute("SELECT Archetype FROM archetypes WHERE Side = 'B'")
            toSend = ""
            for i in cursor.fetchall():
              for e in i:
                toSend += e + ", "
            m = await message.channel.send(toSend[:-2])
            await self_edit(m)
        elif message.channel.id == 855934709410562068:
          with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM archetypes")
            await message.channel.send(cursor.fetchall())

      elif message.content == ('dream'):
        m = await message.channel.send('We did think that, at first.')
        await self_edit(m)

      elif message.content == ('name'):
        m = await message.channel.send('If we could remember that, we would have.')
        await self_edit(m)

      elif message.content == ('rules'):
        if message.channel.id in client.ASideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('The parameters of life. This may help us remember who we are - but they may change with time, if only slightly. https://docs.google.com/document/d/1H-eWcMv_5avqHZ5_uFek-W18zlNfkbUcC54gzVWMqC4/edit?usp=sharing')
          await self_edit(m)
        if message.channel.id in client.BSideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('The parameters of life. This may help us remember who we are - but they may change with time, if only slightly. https://docs.google.com/document/d/1RkLS-1lk0A2PbrUZ0dpfNolKy0iJBaCmMwCDmf5k5dg/edit?usp=sharing')
          await self_edit(m)

      elif message.content == ('test'):
        m = await message.channel.send('Perhaps it is.')
        await self_edit(m)

      elif message.content == ('echoes&memories'):
        m = await message.channel.send('Something does stir at the name... A hint of despair. (Both your characters start with one despair.)')
        await self_edit(m)

      elif message.content == ('hope\'speak') or message.content == ('hopespeak') or message.content == ('ultimate') or message.content == ('danganronpa'):
        m = await message.channel.send('A fantasy, and nothing more.')
        await self_edit(m)

      elif message.content == ('echo'):
        m = await message.channel.send('Is that all we are?')
        await self_edit(m)

      elif message.content == ('game'):
        m = await message.channel.send('The stakes are too high.')
        await self_edit(m)

      elif message.content == ('guide') or message.content == ('guides'):
        m = await message.channel.send('Who are they? What do they know?')
        await self_edit(m)

      elif message.content == ('personalchats'):
        m = await message.channel.send('It feels personal.')
        await self_edit(m)

      elif message.content == ('privatechannels'):
        m = await message.channel.send('Is it private, here? What lurks?')
        await self_edit(m)

      elif message.content == ('explore') or message.content == ('lookaround') or message.content == ('gonorth') or message.content == ('goeast') or message.content == ('gowest') or message.content == ('gosouth'):
        m = await message.channel.send('The flame captures your attention... but first you must remember who you are.')
        await self_edit(m)

      elif message.content == ('help'):
        m = await message.channel.send('We got ourselves into this mess. It\'s up to us to get out of it.')
        await self_edit(m)

      elif message.content == ('schedule'):
        if message.channel.id in client.ASideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Who remembers schedules? Good thing you can check back later. https://docs.google.com/document/d/1yfWeXkCj6Eu7wezA_5Cox5q2sY7atYFqzwljcxpgOyw/edit?usp=sharing')
          await self_edit(m)
        if message.channel.id in client.BSideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Who remembers schedules? Good thing you can check back later. https://docs.google.com/document/d/11oLM22FdQuvQEa_6pMFwRRn8RbJupL1OUtVLCjKNttM/edit?usp=sharing')
          await self_edit(m)

      elif message.content == ('questionnaire'):
        if message.channel.id in client.ASideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Memory is rather fickle... but you can always make a backup. https://docs.google.com/document/d/1rXDT17ei9PJyVi0OISm65l8j-plqY08s00WEUAdUx_A/edit?usp=sharing')
          await self_edit(m)
        if message.channel.id in client.BSideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Memory is rather fickle... but you can always make a backup. https://docs.google.com/document/d/1C9vJfUEOIlWeYGaEinr9OLkX-4BH_OK8H0Kyu1tkxQE/edit?usp=sharing')
          await self_edit(m)

      elif message.content == ('poll'):
        if message.channel.id in client.ASideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Let us know your thoughts. https://forms.gle/h3evqrGxyZo9PPXo8')
          await self_edit(m)
        if message.channel.id in client.BSideChannels or checkGuide in message.author.roles:
          m = await message.channel.send('Let us know your thoughts. https://forms.gle/h3evqrGxyZo9PPXo8')
          await self_edit(m)

      elif message.content == ('remembersubconscious'):
        m = await message.channel.send('Murder is a drastic measure, but sometimes it is necessary. Try to figure out all you can before coming to a decision. Remember to stay offthebeatenpath.')
        await self_edit(m)

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
