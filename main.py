import discord
import json
import random

bot_token = 'TOKEN_DU_BOT_ICI'
target_channel_id = 'ID_SALON_CONFESSION_ICI'
logs_channel_id = 'ID_SALON_LOGS_CONFESSION_ICI'

intents = discord.Intents.all()
client = discord.Client(intents=intents)

confession_count = 0
cooldown = 30

cooldowns = {}

def save_confession_count():
    with open('confession_count.json', 'w') as file:
        json.dump({'count': confession_count}, file)

def load_confession_count():
    try:
        with open('confession_count.json', 'r') as file:
            data = json.load(file)
            return data['count']
    except FileNotFoundError:
        return 0

confession_count = load_confession_count()

@client.event
async def on_ready():
    print(f'Bot is ready! Logged in as {client.user.name}')

@client.event
async def on_message(message):
    global confession_count, cooldowns

    if message.author != client.user and isinstance(message.channel, discord.DMChannel):
        if message.author.id in cooldowns and (message.created_at - cooldowns[message.author.id]).seconds < cooldown:
            embed_cooldown = discord.Embed(description=f"Vous devez attendre {cooldown} secondes avant d'envoyer une nouvelle confession.", color=discord.Color.red())
            await message.author.send(embed=embed_cooldown)
            return

        confession_count += 1

        cooldowns[message.author.id] = message.created_at

        message_content = message.content

        anonymous_message = f"\"{message_content}\""

        target_channel = client.get_channel(int(target_channel_id))

        if target_channel:
            embed_confession = discord.Embed(title=f"Anonymous Confession #{confession_count}", description=anonymous_message, color=random.randint(0, 0xFFFFFF))
            embed_confession.set_footer(text="❗ Si cette confession n'est pas appropriée, signaler au staff en ouvrant un ticket.")
            await target_channel.send(embed=embed_confession)

            embed_logs = discord.Embed(title=f"Anonymous Confession #{confession_count}", description=anonymous_message, color=random.randint(0, 0xFFFFFF))
            embed_logs.add_field(name="Utilisateur :", value=f"||{message.author.name} ({message.author.mention})||", inline=False)
            embed_logs.add_field(name="ID de la personne :", value=f"||{message.author.id}||", inline=False)
            embed_logs.add_field(name="", value=f"Cliquez [ici](https://discord.com/channels/@me/{message.channel.id}/{message.id}) pour voir la confession.", inline=False)
            embed_logs.set_footer(text="❗ Si cette confession n'est pas appropriée, signaler au staff en ouvrant un ticket.")

            logs_channel = client.get_channel(int(logs_channel_id))

            if logs_channel:
                await logs_channel.send(embed=embed_logs)

            embed_confirm = discord.Embed(description="Votre confession a été envoyée avec succès. Les staffs n'ont pas accès aux messages privés du bot.", color=discord.Color.green())
            await message.author.send(embed=embed_confirm)
        else:
            print("Erreur : Le salon cible n'existe pas.")

        save_confession_count()

client.run(bot_token)
