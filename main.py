import discord
from discord.ext import commands
import os
import asyncio
import mysql.connector
import random
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
    cursor.execute("CREATE TABLE Players(Name CHAR(20), Tokens TINYINT,  UID CHAR(30)")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Ava', 0, '209560384313491456')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Christina', 0, '367539851559567360')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Gary', 0, '449781760083886080')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Jack', 0, '148560657640325121')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Janice', 0, '306992983926898689')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Joey', 0, '336671543423795201')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Sid', 0, '501107249960189982')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Sienna', 0, '354347011635544066')")

    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Audrey', 0, '236845578317856769')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Becca', 0, '371627728643948566')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Brian', 0, '315992836002676751')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Christine', 0, '676468054691020810')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Ed', 0, '268470573137526785')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Jun', 0, '275464916188790784')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Eden', 0, '112651984275849216')")
    cursor.execute("INSERT INTO Players (Name, Tokens) VALUES ('Sarah', 0, '468679170227175424')")

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
        connection.cursor().execute("INSERT INTO archetypes (Side, Archetype, Echoes, Memories, Harm, Stress) VALUES (%s, %s, %s, %s, %s, %s)", ("A", oMess[16:], 0, 0, 0, 0))
        connection.commit()
        await message.channel.send("Added " + oMess[16:] + " to A Side")
        return
      elif checkGuide in message.author.roles and message.content.startswith('addb archetype'):
        connection.cursor().execute("INSERT INTO archetypes (Side, Archetype, Echoes, Memories, Harm, Stress) VALUES (%s, %s, %s, %s, %s, %s)", ("B", oMess[16:], 0, 0, 0, 0))
        connection.commit()
        await message.channel.send("Added " + oMess[16:] + " to B Side")
        return

      if checkGuide in message.author.roles and message.content.startswith("harm"):
        target = message.content[5:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[4]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Harm = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + "'s harm is now " + str(curr) + ".")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[4]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Harm = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + "'s harm is now " + str(curr) + ".")
        return

      elif checkGuide in message.author.roles and message.content.startswith("healharm"):
        target = message.content[9:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[4]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Harm = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + "'s harm is now " + str(curr) + ".")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[4]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Harm = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + "'s harm is now " + str(curr) + ".")
        return

      elif checkGuide in message.author.roles and message.content.startswith("stress"):
        target = message.content[7:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[5]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Stress = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + "'s stress is now " + str(curr) + ".")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[5]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Stress = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + "'s stress is now " + str(curr) + ".")
        return

      elif checkGuide in message.author.roles and message.content.startswith("healstress"):
        target = message.content[11:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[5]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Stress = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + "'s stress is now " + str(curr) + ".")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[5]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Stress = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + "'s stress is now " + str(curr) + ".")
        return


      elif checkGuide in message.author.roles and message.content.startswith("addmemory"):
        target = message.content[10:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[3]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Memories = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " memories.")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[3]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Memories = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " memories.")
        return

      elif message.content.startswith("paymemory"):
        target = message.content[10:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[3]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Memories = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " memories.")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[3]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Memories = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " memories.")
        return

      elif checkGuide in message.author.roles and message.content.startswith("addecho"):
        target = message.content[8:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[2]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Echoes = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " echoes.")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[2]
          curr = curr + 1
          cursor.execute("UPDATE archetypes SET Echoes = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " echoes.")
        return

      elif message.content.startswith("payecho"):
        target = message.content[8:].capitalize()
        if message.channel.id in client.ASideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("A", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[2]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Echoes = %s WHERE Side = %s AND Archetype = %s", (curr, "A", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " echoes.")
        elif message.channel.id in client.BSideChannels:
          cursor = connection.cursor(buffered=True)
          cursor.execute("select * from archetypes where Side = %s and Archetype = %s", ("B", target))
          record = cursor.fetchall()
          curr = 0
          for row in record:
            curr = row[2]
          curr = max(0,curr - 1)
          cursor.execute("UPDATE archetypes SET Echoes = %s WHERE Side = %s AND Archetype = %s", (curr, "B", target))
          connection.commit()
          await message.channel.send(target + " now has " + str(curr) + " echoes.")
        return


      message.content = message.content.replace(' ', '')


      if message.content == ("trickster"):
        tgtChar = 'Z'
        if message.channel.id == 853698538473914418: tgtChar = 'A'
        elif message.channel.id == 858425078390456330: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Trickster"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Trickster has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("strong&silent") or message.content == ("strongandsilent") or message.content == ("s&s") or message.content == ("sands"):
        tgtChar = 'Z'
        if message.channel.id == 853698538473914418: tgtChar = 'A'
        elif message.channel.id == 853826359838244874: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Strong & Silent"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Strong & Silent has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("cynic"):
        tgtChar = 'Z'
        if message.channel.id == 858251891049496577: tgtChar = 'A'
        elif message.channel.id == 853826338482028574: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Cynic"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Cynic has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("storyteller"):
        tgtChar = 'Z'
        if message.channel.id == 858251891049496577: tgtChar = 'A'
        elif message.channel.id == 858353300885602364: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Storyteller"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Storyteller has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("paragon"):
        tgtChar = 'Z'
        if message.channel.id == 853703038644912158: tgtChar = 'A'
        elif message.channel.id == 853703410620301352: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Paragon"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Paragon has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("fae"):
        tgtChar = 'Z'
        if message.channel.id == 853703038644912158: tgtChar = 'A'
        elif message.channel.id == 853826418630328340: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Fae"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Fae has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("mentor") or message.content == ("eccentricmentor"):
        tgtChar = 'Z'
        if message.channel.id == 858478351819866143: tgtChar = 'A'
        elif message.channel.id == 853826359838244874: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Mentor"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Mentor has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("sidekick"):
        tgtChar = 'Z'
        if message.channel.id == 858478351819866143: tgtChar = 'A'
        elif message.channel.id == 853826398799134750: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Sidekick"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Sidekick has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("beast"):
        tgtChar = 'Z'
        if message.channel.id == 858164641586216981: tgtChar = 'A'
        elif message.channel.id == 858353300885602364: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Beast"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Beast has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("eee") or message.content == ("enigmaticempoweringentity"):
        tgtChar = 'Z'
        if message.channel.id == 858164641586216981: tgtChar = 'A'
        elif message.channel.id == 862144551581384715: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "EEE"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Enigmatic Empowering Entity has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("hedonist"):
        tgtChar = 'Z'
        if message.channel.id == 858164604719071253: tgtChar = 'A'
        elif message.channel.id == 862144551581384715: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Hedonist"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Hedonist has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("hauntedone"):
        tgtChar = 'Z'
        if message.channel.id == 858164604719071253: tgtChar = 'A'
        elif message.channel.id == 853826338482028574: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Haunted One"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Haunted One has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("geniusditz"):
        tgtChar = 'Z'
        if message.channel.id == 858885465444712518: tgtChar = 'A'
        elif message.channel.id == 853826398799134750: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Genius Ditz"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Genius Ditz has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("rebel"):
        tgtChar = 'Z'
        if message.channel.id == 858885465444712518: tgtChar = 'A'
        elif message.channel.id == 858425078390456330: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Rebel"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Rebel has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("dynamo"):
        tgtChar = 'Z'
        if message.channel.id == 861889058892283915: tgtChar = 'A'
        elif message.channel.id == 853826418630328340: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "Dynamo"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Dynamo has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return

      elif message.content == ("ob") or message.content == ("obstructivebureaucrat"):
        tgtChar = 'Z'
        if message.channel.id == 861889058892283915: tgtChar = 'A'
        elif message.channel.id == 853703410620301352: tgtChar = 'B'
        else: return
        cursor = connection.cursor(buffered=True)
        cursor.execute("select * from archetypes where Side = %s and Archetype = %s", (tgtChar, "OB"))
        record = cursor.fetchall()
        echoes = 0
        memories = 0
        harm = 0
        stress = 0
        for row in record:
          echoes = row[2]
          memories = row[3]
          harm = row[4]
          stress = row[5]
        await message.channel.send("The Obstructive Bureaucrat has " + str(echoes) + " echoes, " + str(memories) + " memories, " + str(harm) + " harm, and " + str(stress) + " stress.")
        return
      

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

      elif message.content == ('checkall') and checkGuide in message.author.roles:
        if message.channel.id == 855934709410562068:
          with connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT * FROM archetypes")
            result = cursor.fetchall()
            r = ""
            for row in result:
              r += str(row) + "\n"
            await message.channel.send(r)

      elif message.content == ('checkplayers') and checkGuide in message.author.roles:
        if message.channel.id == 855934709410562068:
          with connection.cursor(buffered=True) as cursor:
            cursor.execute("SELECT * FROM Players")
            result = cursor.fetchall()
            r = ""
            for row in result:
              r += str(row) + "\n"
            await message.channel.send(r)

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
        m = await message.channel.send('We\'re excited to see you!')
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
        m = await message.channel.send('You don’t have to remember that anymore. You can do it now.')
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
        m = await message.channel.send('Let us know your thoughts. https://forms.gle/h3evqrGxyZo9PPXo8')
        await self_edit(m)

      elif message.content == ('remembersubconscious'):
        m = await message.channel.send('Murder is a drastic measure, but sometimes it is necessary. Try to figure out all you can before coming to a decision. Remember to stay offthebeatenpath.')
        await self_edit(m)

      elif message.content == ('leftbrain'):
        m = await message.channel.send('You were missed.')
        await self_edit(m)

      elif message.content == ('rightbrain'):
        m = await message.channel.send('I was lonely.')
        await self_edit(m)

      elif message.content == ('connectingthedots'):
        m = await message.channel.send('There is a reward for this. It isn\'t ready yet. We will get back to you.')
        await self_edit(m)

      elif message.content == ('ampersandtechnologies'):
        m = await message.channel.send('The & always means there\'s more to come.')
        await self_edit(m)

      elif message.content == ('&'):
        m = await message.channel.send('That would be bad.')
        await self_edit(m)

      elif message.content == (':'):
        m = await message.channel.send('That again? I\'m practically seeing it in my sleep at this point.')
        await self_edit(m)

      elif message.content == ('offthebeatenpath'):
        m = await message.channel.send('There is no path unbeaten here.')
        await self_edit(m)

      elif message.content == ('Julie'):
        m = await message.channel.send('Juliette Armstrong, butler and bodyguard. How could you have forgotten her? There was so much going on, I suppose you could cut yourself a little slack..')
        await self_edit(m)

      elif message.content == ('forget'):
        m = await message.channel.send('We\'ve already forgotten so much. We cannot afford to forget any more.')
        await self_edit(m)

      elif message.content.replace('.', '') == ('alann'):
        m = await message.channel.send('Ben just likes referencing himself. Little vain if you ask me. This isn\'t relevant.')
        await self_edit(m)

      elif message.content == ('general'):
        if message.channel.id in client.ASideChannels:
          general = client.get_channel(884660041632845845)
          await general.set_permissions(message.author, read_messages=True, send_messages=True)
          await general.send(message.author.display_name + " is now among you.")
          general = client.get_channel(884832132189544488)
          await general.set_permissions(message.author, read_messages=True, send_messages=True)

        elif message.channel.id in client.BSideChannels:
          general = client.get_channel(884660176718819330)
          await general.set_permissions(message.author, read_messages=True, send_messages=True)
          await general.send(message.author.display_name + " is now among you.")
          general = client.get_channel(884832202221826059)
          await general.set_permissions(message.author, read_messages=True, send_messages=True)

      elif message.content == ('spiderweb'):
        if message.channel.id in client.ASideChannels:
          puzzle = client.get_channel(886841297485324328)
          if (puzzle.permissions_for(message.author).read_messages == True):
            await puzzle.set_permissions(message.author, read_messages=False, send_messages=False)
          else:
            await puzzle.set_permissions(message.author, read_messages=True, send_messages=True)


        elif message.channel.id in client.BSideChannels:
          puzzle = client.get_channel(886812805527924768)
          if (puzzle.permissions_for(message.author).read_messages == True):
            await puzzle.set_permissions(message.author, read_messages=False, send_messages=False)
          else:
            await puzzle.set_permissions(message.author, read_messages=True, send_messages=True)

      elif message.content == ('audience'):
        m = await message.channel.send('That could be anybody...')
        await self_edit(m)

      elif message.content == ('weaver'):
        m = await message.channel.send('We always thought it was ironic, considering what happened.')
        await self_edit(m)

      elif message.content == ('ms.harriet'):
        m = await message.channel.send('Wished she was nicer.')
        await self_edit(m)

      elif message.content == ('mr.young'):
        m = await message.channel.send('What an asshole.')
        await self_edit(m)

      elif message.content == ('spider'):
        await message.channel.send(':spider:')

      elif message.content == ('odessa'):
        m = await message.channel.send('They never talked about it.')
        await self_edit(m)

      elif message.content == ('wilfredweaver') or message.content == ('dr.wilfredweaver'):
        m = await message.channel.send('What happened to them?')
        await self_edit(m)

      elif message.content == ('esarebrokenwiththepowerd'):
        await message.channel.send(file=discord.File('&esarebrokenwiththePowerD.png'))

      elif message.content == ('cardbcd28d078b562cbc168cb62a018ddaca'):
        await message.channel.send(file=discord.File('A Labs/The Fae\'s Lab.png'))

      elif message.content == ('cardd0aba11c6b5a7467d76b7f5713eeba8d'):
        await message.channel.send(file=discord.File('A Labs/The Paragon\'s Lab.png'))

      elif message.content == ('card41835c2a6ddf12373e09160394e2dc57'):
        await message.channel.send(file=discord.File('A Labs/The S&S\'s Lab.png'))

      elif message.content == ('card0f6f83536aff1225d01c3d471b6c9d05'):
        await message.channel.send(file=discord.File('A Labs/The Trickster\'s Lab.png'))

      elif message.content == ('card75a7955f7abdffea5d992c34a57d97e0'):
        await message.channel.send(file=discord.File('A Labs/The Beast\'s Lab.png'))

      elif message.content == ('card8cdfe5fb3b4aecae4a312e27100155c3'):
        await message.channel.send(file=discord.File('A Labs/The EEE\'s Lab.png'))

      elif message.content == ('carddccfeac2e60b1d47e4d81facbd069b13'):
        await message.channel.send(file=discord.File('A Labs/The OB\'s Lab.png'))

      elif message.content == ('cardad954e87cf8f7b9e661a5e39814bb31b'):
        await message.channel.send(file=discord.File('B Labs/The Sidekick\'s Lab.png'))

      elif message.content == ('card46361a71632e9810d8422c00c49029e9'):
        await message.channel.send(file=discord.File('B Labs/The GD\'s Lab.png'))

      elif message.content == ('carda8515bd8faebac07d0f484f51f22df19'):
        await message.channel.send(file=discord.File('B Labs/The OB\'s Lab.png'))

      elif message.content == ('card248b72b23153515929a3a605fc16e5f7'):
        await message.channel.send(file=discord.File('B Labs/The Paragon\'s Lab.png'))

      elif message.content == ('carda4ef37044af1b18f767f86cde513e443'):
        await message.channel.send(file=discord.File('B Labs/The EEE\'s Lab.png'))

      elif message.content == ('card835675ec40be36e4b4b0f149e64da117'):
        await message.channel.send(file=discord.File('B Labs/The Hedonist\'s Lab.png'))

      elif message.content == ('carda4e2466d6ab2f25fa40235d5024f7893'):
        await message.channel.send(file=discord.File('B Labs/The Dynamo\'s Lab.png'))

      elif message.content == ('card1495d8e7a1bab809481255c4fe58cb5a'):
        await message.channel.send(file=discord.File('B Labs/The Fae\'s Lab.png'))

      elif message.content == ('card4857ed8827790609fd88a94a25686ead'):
        await message.channel.send(file=discord.File('B Labs/The Cynic\'s Lab.png'))

      elif message.content == ('card7e9a0b300a3a7d8e2ce50ba6b6dcbfe0'):
        await message.channel.send(file=discord.File('B Labs/The Haunted One\'s Lab.png'))

      elif message.content == ('14e49010c0cf571e3133a585dd833789') or message.content == ('0e3964e70f6aca22f1edc573a01882eb') or message.content == ('03e423335d50461e14f5c71bb089e861') or message.content == ('157546964e5aa203d49b80c828aa53db') or message.content == ('5e06edb4ed226b1711b4acfb7a3aefa3'):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('nicky') or message.content == ('anna')) and message.author.id == (336671543423795201):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('clay') or message.content == ('eleanor')) and message.author.id == (501107249960189982):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('charlie') or message.content == ('tania')) and message.author.id == (209560384313491456):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('sage') or message.content == ('paige')) and message.author.id == (354347011635544066):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('ken') or message.content == ('remy')) and message.author.id == (449781760083886080):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('blythe') or message.content == ('august')) and message.author.id == (148560657640325121):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('quinn') or message.content == ('aiden')) and message.author.id == (306992983926898689):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('vivian') or message.content == ('marlow')) and message.author.id == (367539851559567360):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('marlow') or message.content == ('charlie')) and message.author.id == (315992836002676751):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('paige') or message.content == ('quinn')) and message.author.id == (371627728643948566):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('tania') or message.content == ('vivian')) and message.author.id == (676468054691020810):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('eleanor') or message.content == ('ken')) and message.author.id == (112651984275849216):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('aiden') or message.content == ('nicky')) and message.author.id == (275464916188790784):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('anna') or message.content == ('sage')) and message.author.id == (468679170227175424):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('august') or message.content == ('clay')) and message.author.id == (268470573137526785):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()

      elif (message.content == ('remy') or message.content == ('blythe')) and message.author.id == (236845578317856769):
        await message.channel.send('You found a memory token! @Guides will help you figure out what this means. Good job!')
        with connection.cursor(buffered=True) as cursor:
          cursor.execute("UPDATE Players SET Tokens = Tokens + 1 WHERE Name = %s", (message.author.id))
          connection.commit()




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


      elif message.content.startswith('roll'):
        full = message.content[4:]
        result = ""
        successes = 0
        if 'd' in full:
          dArgs = full.split("d")
          try:
            numDice = int(dArgs[0])
            diceType = int(dArgs[1])
            if numDice > 100:
              await message.channel.send("Little more than I can handle...")
              return
            for i in range(numDice):
              roll = random.randint(1, diceType)
              result += str(roll) + ", "
              if roll > 3: successes += 1
            await message.channel.send(message.author.display_name + " rolled: " + result[:-2] +". **Successes:** " + str(successes))
          except:
            await message.channel.send("Failed to roll dice. Hopefully that's what you were going for.")
        else:
          try:
            numDice = int(full)
            if numDice > 100:
              await message.channel.send("Little more than I can handle...")
              return
            for i in range(numDice):
              roll = random.randint(1, 6)
              result += str(roll) + ", "
              if roll > 3: successes += 1
            await message.channel.send(message.author.display_name + " rolled: " + result[:-2] +". **Successes:** " + str(successes))
          except:
            await message.channel.send("Failed to roll dice. Hopefully that's what you were going for.")





      else:
        await message.channel.send(oMess[1:])

client.run(token)
