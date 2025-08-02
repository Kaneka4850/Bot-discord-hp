import discord
from discord.ext import commands

class Convocacao(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="convocar")
    async def convocar(self, ctx, membro: discord.Member = None, hora: str = None, moderador: str = None):
        cargos_permitidos = [
            1398078480955998209, 1380259829930524733, 1399188753116827678, 1380260619525296369, 1380272583743897630
        ]

        autor = ctx.author
        possui_cargo = any(role.id in cargos_permitidos for role in autor.roles)

        if not possui_cargo:
            await ctx.send("⛔ Você não tem permissão para usar esse comando.")
            return

        if not all([membro, hora, moderador]):
            await ctx.send("⚠️ Use assim: `!convocar @membro hora moderador`")
            return

        canal_id = 1390444561897357463 # ID do canal de alinhamento
        canal_destino = self.bot.get_channel(canal_id)

        if canal_destino is None:
            await ctx.send("❌ Canal de convocação não encontrado.")
            return

        embed = discord.Embed(
            title="🏥 Convocação de alinhamento",
            description=f"Caro {membro.mention},\n\nVocê está sendo convocado para um alinhamento para falarmos sobre sua conduta no hospital.",
            color=discord.Color.blurple()
        )
        embed.add_field(name="⏰ Horário do alinhamento", value=hora, inline=True)
        embed.add_field(name="👤 Procurar por:", value=moderador, inline=True)
        embed.set_footer(text="O não comparecimento em até 24hrs pode acarretar em sanções.")

        await canal_destino.send(content=f'|| {membro.mention} ||', embed=embed)

        # ✅ Registro no canal de logs
        canal_logs = self.bot.get_channel(1401309129183727688) # ID do canal de logs
        if canal_logs:
            log_embed = discord.Embed(
                title="📋 Log de Convocação",
                description=f"{autor.mention} convocou {membro.mention}",
                color=discord.Color.dark_purple()
            )
            log_embed.add_field(name="🕒 Horário", value=hora)
            log_embed.add_field(name="👤 Moderador", value=moderador)
            log_embed.set_footer(text=f"Comando usado por: {autor}", icon_url=autor.display_avatar.url)
            await canal_logs.send(embed=log_embed)

async def setup(bot):
    await bot.add_cog(Convocacao(bot))