import discord
import random
import sqlite3
import datetime
from discord import File
import os
import asyncio

admin_user_id = ''  # Replace with the actual discord admin user ID
prizes = [("Extra spin count", 0.05, "wheel.png"),
          ("Second prize", 0.02, "wheel.png"),
          ("Third prize", 0.001, "wheel.png"),
          ("Fourth prize", 0.00035, "wheel.png"),
          ("Fifth prize", 0.000001, "wheel.png"),
          ("womp womp", 0.928649, "wheel.png")]


intents = discord.Intents.default()
intents.messages = True
intents.dm_messages = True
intents.guilds = True
intents.reactions = True
intents.members = True
intents.presences = True
intents.typing = True
intents.voice_states = True
intents.message_content = True

client = discord.Client(intents=intents)
conn = sqlite3.connect('mydb.db')
c = conn.cursor()

@client.event
async def on_ready():
    print("Logged in as {}".format(client.user))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!spin'):
        await message.channel.send('Spinning...')
        await asyncio.sleep(3)  # Delay for 3 seconds

        c.execute('SELECT * FROM spins WHERE user_id=?', (message.author.id,))
        result = c.fetchone()
        current_time = datetime.datetime.now()

        if result is None:
            c.execute('INSERT INTO spins VALUES (?, ?, ?, ?, ?, ?)', (message.author.id, 1, current_time, 0, "", ""))
        else:
            last_spin_time, spins, reset_count, prize_won, prize_time = result[2], result[1], result[3], result[4], result[5]
            last_spin_time = last_spin_time.split('.')[0] if last_spin_time is not None else None

            if last_spin_time is None or (current_time - datetime.datetime.strptime(last_spin_time, '%Y-%m-%d %H:%M:%S')).total_seconds() / 3600 >= 24:
                spins += 1

                if spins == 30:
                    await message.channel.send("Congratulations! You've accumulated 30 spins! Your spin counter has been reset, and you can claim your prize by sending a DM to 'name'.")
                    spins = 0  # Reset spin count to zero
                    reset_count += 1  # Increment reset count by 1

                    admin_user = await client.fetch_user(admin_user_id)
                    if admin_user is not None:
                        await admin_user.send(f"User {message.author.name} has reached 30 spins!")

                c.execute('UPDATE spins SET value=?, last_spin_time=?, reset_count=?, prize_won=?, prize_time=? WHERE user_id=?',
                          (spins, current_time, reset_count, "", "", message.author.id))
            else:
                await message.channel.send("You can only spin once every 24 hours.")
                conn.commit()
                return

        prize = random.choices([prize[0] for prize in prizes], [prize[1] for prize in prizes])[0]

        if prize == "Extra spin count":
            c.execute('UPDATE spins SET value=value+1, prize_won=?, prize_time=? WHERE user_id=?',
                      ("Extra spin count", current_time, message.author.id))
            conn.commit()

            png_file = next((p[2] for p in prizes if p[0] == prize), None)
            if png_file:
                file_path = os.path.join(os.getcwd(), png_file)  # Get the full path to the PNG file
                file = discord.File(file_path, filename="prize.png")
                await message.channel.send(file=file)

            await message.channel.send('Congratulations! You win an extra spin count.')


        elif prize != "womp womp":
            if prize is not None:
                c.execute('UPDATE spins SET prize_won=?, prize_time=? WHERE user_id=?',
                          (prize, current_time, message.author.id))
        conn.commit()

        if prize == "womp womp":

            png_file = next((p[2] for p in prizes if p[0] == prize), None)
            if png_file:
                file_path = os.path.join(os.getcwd(), png_file)  # Get the full path to the PNG file
                file = discord.File(file_path, filename="prize.png")
                await message.channel.send(file=file)
            await message.channel.send("womp womp. You didn't win a prize today. Better luck next time.")
        else:
            png_file = next((p[2] for p in prizes if p[0] == prize), None)
            if png_file:
                file_path = os.path.join(os.getcwd(), png_file)  # Get the full path to the GIF file
                file = discord.File(file_path, filename="prize.gif")
                if prize != "Extra spin count":
                    await message.channel.send(f'Congratulations! You win: {prize}.', file=file)
                admin_user = await client.fetch_user(int(admin_user_id))
                if admin_user is not None:
                    await admin_user.send(f"User {message.author.name} has won a prize: {prize}")

        c.execute('SELECT * FROM spins WHERE user_id=?', (message.author.id,))
        user_data = c.fetchone()

        await message.channel.send('You have accumulated {} spins.'.format(user_data[1]))

    elif message.content.startswith('!stats'):
        c.execute('SELECT * FROM spins WHERE user_id=?', (message.author.id,))
        user_data = c.fetchone()

        if user_data is None:
            await message.channel.send("You don't have any data in the database yet.")
        else:
            response = f"Here are your stats:\nSpins: {user_data[1]}\nLast spin time: {user_data[2]}\nReset count: {user_data[3]}\nPrize won: {user_data[4]}\nPrize time: {user_data[5]}\n"
            await message.channel.send(response)

client.run('your discord dev api token here')
conn.close()
