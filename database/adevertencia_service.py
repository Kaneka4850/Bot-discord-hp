import discord
from datetime import datetime

def criar_embed_advertencia(membro, motivo, autor):
    embed = discord.Embed(title="⚠️ Advertência Aplicada", color=discord.Color.orange())
    embed.add_field(name="👤 Membro Advertido", value=membro.mention, inline=True)
    embed.add_field(name="📄 Motivo", value=motivo, inline=False)
    embed.set_footer(text=f"⏰ Advertência registrada em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    embed.set_author(name=f"Aplicada por: {autor}")
    return embed