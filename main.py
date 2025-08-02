import os
import logging
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

bot = commands.Bot(command_prefix="!", intents=intents)

COGS = [
    "cogs.cadastro",
    "cogs.alinhamento",
    "cogs.advertencia",
    "cogs.ticket",
]

recrutadores = 1388684130891468952
canal_logs_id = 1401309129183727688

@bot.command(name="comandos")
async def comandos(ctx):
    embed = discord.Embed()
    embed.title = "📝 Lista de Comandos Disponiveis"
    embed.description = "Esses são os comandos do bot, não esqueça de usar o prefixo `!` antes de cada comando."
    embed.color = discord.Color.pink()
    embed.add_field(name="!registro", value="Inicia o processo de registro.", inline=False)
    embed.add_field(name="!listar_registros", value="Lista todos os registros aprovados.", inline=False)
    embed.add_field(name="!demitir", value="Demitir um agente (apenas admins).", inline=False)
    embed.add_field(name="!convocar", value="Convoca um membro para uma reunião.", inline=False)
    embed.add_field(name="!advertir", value="Aplica uma advertência a um membro.", inline=False)
    embed.add_field(name="!comandos", value="Lista todos os comandos disponíveis.", inline=False)
    embed.add_field(name="!ticket", value="Abre seu chat privado e sua aba de farm", inline=False)
    embed.set_footer(text="Use os comandos apenas em caso de necessidade, não abuse do bot.")
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    await ctx.send(embed=embed)

async def load_cogs():
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            logging.info(f"✅ Cog carregado: {cog}")
        except Exception as e:
            logging.error(f"❌ Erro ao carregar {cog}: {e}")

@bot.event
async def on_ready():
    logging.info(f"🤖 Bot online como: {bot.user}")
    logging.info(f"📊 Servidores conectados: {[guild.name for guild in bot.guilds]}")
    print(f"Bot online como {bot.user}")

@bot.event
async def setup_hook():
    await load_cogs()
    await bot.tree.sync()

if __name__ == "__main__":
    logging.info("🚀 Iniciando o bot...")
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("Token do Discord não encontrado nas variáveis de ambiente (.env)!")
    bot.run(token)
