import discord
from discord.ext import commands

class Advertencias(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cargos_permitidos = [
             1398078480955998209, 1380259829930524733, 1399188753116827678, 1380260619525296369, 1380272583743897630

        ]
        self.cargos_advertencia = {
            "adv1": 1382447589538009129, # Cargo adv 1
            "adv2": 1382447447703556116, # Cargo adv 2
            "adv3": 1390102182732369982, # Cargo adv 3
            "verbal": 1382447676645179393, # Cargo verbal
        }
        self.canal_destino_id = 1383571702394392686  # canal onde será enviada a advertência

    @commands.command()
    async def advertir(self, ctx, membro: discord.Member = None, tipo: str = None, duracao: int = 0, *, argumentos: str = None):
        autor = ctx.author

        # Verifica permissão do autor
        if not any(role.id in self.cargos_permitidos for role in autor.roles):
            await ctx.send("⛔ Você não tem permissão para usar esse comando.")
            return

        if not membro or not tipo or not argumentos:
            await ctx.send("⚠️ Use assim: `!advertir @membro tipo duração motivo aplicador`")
            return

        if duracao < 0:
            await ctx.send("⚠️ A duração não pode ser negativa.")
            return

        partes = argumentos.rsplit(" ", 1)
        if len(partes) != 2:
            await ctx.send("⚠️ Informe o motivo seguido do nome do aplicador.")
            return

        motivo, aplicador = partes
        tipo = tipo.lower()

        # Verifica tipo de advertência
        if tipo not in self.cargos_advertencia:
            await ctx.send(f"⚠️ Tipo inválido. Use: `{', '.join(self.cargos_advertencia.keys())}`")
            return

        cargo_id = self.cargos_advertencia[tipo]
        cargo = ctx.guild.get_role(cargo_id)

        if not cargo:
            await ctx.send("⚠️ Cargo de advertência não encontrado. Verifique o ID.")
            return

        # Verifica hierarquia
        if cargo.position >= ctx.guild.me.top_role.position:
            await ctx.send("⚠️ Não consigo aplicar esse cargo porque está acima do meu na hierarquia.")
            return

        if membro.top_role.position >= ctx.guild.me.top_role.position:
            await ctx.send("⚠️ Esse membro possui um cargo acima ou igual ao meu. Não posso modificá-lo.")
            return

        # Aplica cargo
        await membro.add_roles(cargo, reason=motivo)

        # Embed
        embed = discord.Embed(
            title="📄 Advertência Aplicada",
            description=f"<@{membro.id}> recebeu uma advertência do tipo **{tipo.upper()}**.",
            color=discord.Color.orange()
        )
        embed.add_field(name="📝 Motivo", value=motivo, inline=False)
        embed.add_field(name="⏳ Duração", value=f"{duracao} dias" if duracao > 0 else "Indeterminada", inline=True)
        embed.add_field(name="👤 Aplicador", value=aplicador, inline=True)
        embed.set_footer(text=f"Ação realizada por {autor}", icon_url=autor.avatar.url if autor.avatar else None)

        # Tenta enviar DM
        try:
            await membro.send(
                f"⚠️ Você foi advertido no servidor **{ctx.guild.name}**.\n"
                f"**Motivo:** {motivo}\n"
                f"**Tipo:** {tipo.upper()}\n"
                f"**Duração:** {'Indeterminada' if duracao == 0 else f'{duracao} dias'}\n"
                f"**Aplicador:** {aplicador}"
            )
        except discord.Forbidden:
            await ctx.send("❌ Não consegui enviar DM ao membro.")

        # Envia no canal de destino
        canal_destino = self.bot.get_channel(self.canal_destino_id)
        if canal_destino:
            await canal_destino.send(content=f"<@{membro.id}>", embed=embed)
        else:
            await ctx.send("⚠️ Canal de destino não encontrado.")

# Setup da cog
async def setup(bot):
    await bot.add_cog(Advertencias(bot))