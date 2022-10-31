import discord
import requests
import os
import json
from discord import app_commands
from python_aternos import Client
from python_aternos import Status

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_DIR = os.path.join(SCRIPT_DIR, '.env.json')
ENV_JSON = json.load(open(ENV_DIR))

API_ENDPOINT = ENV_JSON["API_ENDPOINT"]
USERNAME = ENV_JSON["USERNAME"]
PASSWORD = ENV_JSON["PASSWORD"]
DISCORD_API_KEY = ENV_JSON["DISCORD_API_KEY"]

aternos = Client.from_credentials(username=USERNAME, password=PASSWORD)
server_list = aternos.list_servers()

class disc_client(discord.Client):
  def __init__(self):
    super().__init__(intents=discord.Intents.default())
    self.synced = False
  
  async def on_ready(self):
    await self.wait_until_ready()
    if (not self.synced):
      await tree.sync(guild=discord.Object(id=999596756050378773))
      self.synced = True
    print('Logged on as', self.user)

client = disc_client()
tree = app_commands.CommandTree(client)

@tree.command(name='status', description='Get the server status.', guild=discord.Object(id=999596756050378773))
async def self(interaction: discord.Interaction):
  if requests.get(url = API_ENDPOINT).json()['online'] == True:
    embed = discord.Embed(title="🟢 Status", description="Get the server status.", color=0x000000)
    embed.add_field(name=server_list[0].address, value="🎮 Players: " + str(server_list[0].players_count) + "/" + str(server_list[0].slots) + "\n🖥 Status: Online" + "\nℹ Version: " + server_list[0].version + "\n🛠 Commands: `/start` `/help`", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/mWVVF6m.png")
    embed.set_footer(text="Created by iHxp#6160 • MIT License")
    await interaction.response.send_message(embed=embed)
  else:
    embed = discord.Embed(title="🔴 Status", description="Get the server status.", color=0x000000)
    embed.add_field(name=server_list[0].address, value="🎮 Players: 0/" + str(server_list[0].slots) + "\n🖥 Status: Offline" + "\nℹ Version: " + server_list[0].version + "\n🛠 Commands: `/start` `/help`", inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/mWVVF6m.png")
    embed.set_footer(text="Created by iHxp#6160 • MIT License")
    await interaction.response.send_message(embed=embed)
  

@tree.command(name='help', description='List all commands.', guild=discord.Object(id=999596756050378773))
async def self(interaction: discord.Interaction):
  embed = discord.Embed(title="🛠 Help", description="List all commands.", color=0x000000)
  embed.add_field(name="`/help`", value="Display a list of commands.", inline=False)
  embed.add_field(name="`/start`", value="Start the Minecraft Server", inline=False)
  embed.add_field(name="`/status`", value="Display the server status", inline=False)
  embed.add_field(name="FAQ", value="Server IP: `kingsinterhigh.aternos.me`", inline=False)
  embed.set_thumbnail(url="https://i.imgur.com/3yJgL4r.png")
  embed.set_footer(text="Created by iHxp#6160 • MIT License")
  await interaction.response.send_message(embed=embed)

@tree.command(name='start', description='Start the server!', guild=discord.Object(id=999596756050378773))
async def self(interaction: discord.Interaction):
  if requests.get(url = API_ENDPOINT).json()['online'] == True:
    embed = discord.Embed(title="The server is already on!", description="You can't start a server that is already on... or can you? 🤔 \n\nCheck the server status using the `/status` command.", color=0x000000)
    embed.set_footer(text="Created by iHxp#6160 • MIT License")
    await interaction.response.send_message(embed=embed)
  else:
    try:
      server_list[0].start()
      embed = discord.Embed(title="Starting...", description="The server is starting! Check back in a few minutes using the `/status` command.", color=0x000000)
      embed.set_footer(text="Created by iHxp#6160 • MIT License")
      await interaction.response.send_message(embed=embed)
    except:
      embed = discord.Embed(title="Almost there...", description="Hold on, the server is still starting! Check back in a few minutes using the `/status` command.", color=0x000000)
      embed.set_footer(text="Created by iHxp#6160 • MIT License")
      await interaction.response.send_message(embed=embed)
  


client.run(DISCORD_API_KEY)