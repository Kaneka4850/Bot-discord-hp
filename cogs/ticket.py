import discord
from discord.ext import commands
from cogs.cadastro import listar_registros_aprovados  # Certifique-se de que essa função retorna uma lista de dicts com 'discord_id' e 'nome'

# ID do canal de logs (não é uma função!)
canal_logs_id = 1401309129183727688

# Lista de cargos que têm permissão para criar ticket
cargo_ticket = [1380259951116685486]

class TicketCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticket(self, ctx: commands.Context):
        # Verifica se o autor tem algum dos cargos permitidos
        tem_cargo = any(role.id in cargo_ticket for role in ctx.author.roles)
        if not tem_cargo:
            return await ctx.send("❌ Você precisa se registrar primeiro com o comando `!registro`.")

        # Busca os registros aprovados e localiza o usuário
        registros = listar_registros_aprovados()
        usuario = next((r for r in registros if r['discord_id'] == ctx.author.id), None)
        if usuario is None:
            return await ctx.send("❌ Registro não encontrado.")

        async def criar_ticket(interaction: discord.Interaction):
            categoria_nome = usuario['nome']

            # Verifica se a categoria já existe
            if discord.utils.get(ctx.guild.categories, name=categoria_nome):
                return await interaction.response.send_message(
                    f"🎫 Ticket já existe em `{categoria_nome}`.", ephemeral=True
                )

            # Cria a categoria e os canais dentro dela
            cat = await ctx.guild.create_category(categoria_nome)
            chat = await ctx.guild.create_text_channel("⚪￤chat", category=cat)
            provas = await ctx.guild.create_text_channel("🔴￤farm", category=cat)

            # Define permissões privadas
            await cat.set_permissions(ctx.guild.default_role, view_channel=False)
            await chat.set_permissions(ctx.author, view_channel=True, send_messages=True, read_message_history=True)
            await provas.set_permissions(ctx.author, view_channel=True, send_messages=True, read_message_history=True)

            # Resposta para o usuário
            await interaction.response.send_message(
                f"🎫 Ticket criado em `{categoria_nome}`!", ephemeral=True
            )

            # Envia mensagem no canal de logs
            canal_logs = ctx.guild.get_channel(canal_logs_id)
            if canal_logs:
                await canal_logs.send(f"🎫 Canal do(a) médico(a) {ctx.author.mention} criado: `{categoria_nome}`.")

        # Cria a interface com botão
        view = discord.ui.View()
        botao = discord.ui.Button(label="Crie seu chat", style=discord.ButtonStyle.green)
        botao.callback = criar_ticket
        view.add_item(botao)

        await ctx.send("Clique para criar sua aba de farm:", view=view)

# Para adicionar a cog ao bot:
async def setup(bot):
    await bot.add_cog(TicketCog(bot))
