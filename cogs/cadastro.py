import discord
from discord.ext import commands
import re

# 🧩 Serviços e utilitários
from services.membro_service import (
    adicionar_registro,
    aprovar_registro,
    listar_registros_aprovados,
    remover_registro,
    buscar_registro_por_discord_id
)
from utils.logger import log_event
from utils.permissao import is_admin

# 🔧 IDs e configuração
Cargos_aprovadores = [1388684130891468952] # Cargo de recrutadores
Cargo_membro = 1380259951116685486 # Cargo de hp
Canal_logs = 1401309129183727688 # Canal de logs
canal_aprovacao = 1401309203980877924 # Canal de aprovação de registros


# 🔹 Função para enviar logs e embeds
async def enviar_log(guild, mensagem=None, view=None, embed=None):
    canal = guild.get_channel(Canal_logs)
    if canal:
        if embed:
            await canal.send(embed=embed)
        else:
            await canal.send(mensagem, view=view)

# 📥 Modal de Registro
class RegistroModal(discord.ui.Modal, title="Registre seu Nome, ID e Telefone"):
    nome = discord.ui.TextInput(label="Nome e sobrenome", max_length=32)
    user_id = discord.ui.TextInput(label="Digite seu ID", max_length=32)
    telefone = discord.ui.TextInput(label="Telefone (000-000)", max_length=10)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        telefone_fmt = self.telefone.value
        if not re.fullmatch(r"\d{3}-\d{3}", telefone_fmt):
            return await interaction.response.send_message("❌ Formato inválido! Use 000-000.", ephemeral=True)

        if buscar_registro_por_discord_id(interaction.user.id):
            return await interaction.response.send_message("⛔ Você já enviou um registro.", ephemeral=True)

        registro = {
            "nome": self.nome.value,
            "id": self.user_id.value,
            "telefone": telefone_fmt,
            "usuario": interaction.user.name,
            "discord_id": interaction.user.id,
            "aprovado": False
        }
        adicionar_registro(registro)

        embed_confirma = discord.Embed(
            title="✅ Registro enviado com sucesso!",
            description=f"{interaction.user.name}, seus dados foram enviados para aprovação.",
            color=discord.Color.green()
        )
        await interaction.response.send_message(embed=embed_confirma, ephemeral=True)

        view = discord.ui.View()

        async def aprovar_callback(interaction_):
            aprovador = interaction_.user
            if not is_admin(aprovador) and not any(r.id in Cargos_aprovadores for r in aprovador.roles):
                return await interaction_.response.send_message("❌ Sem permissão para aprovar.", ephemeral=True)

            aprovar_registro(registro["discord_id"])
            log_event(str(aprovador), "Aprovou registro", registro["usuario"])

            membro = interaction_.guild.get_member(registro["discord_id"])
            cargo = interaction_.guild.get_role(Cargo_membro)
            if membro and cargo:
                await membro.add_roles(cargo, reason="Registro aprovado")

                # ✨ Novo nickname com estética "ID | Nome"
                nome_limite = registro["nome"][:20]
                novo_nick = f"{registro['id']} | {nome_limite}"
                try:
                    await membro.edit(nick=novo_nick)
                except discord.Forbidden:
                    print("❌ Permissão insuficiente para mudar o apelido.")
                except discord.HTTPException as e:
                    print(f"❌ Erro ao editar apelido: {e}")

            await interaction_.response.edit_message(
                content=f"✅ Registro de {registro['usuario']} aprovado por {aprovador.mention}.",
                view=None
            )

            await interaction_.channel.send(
                f"🎉 O membro <@{registro['discord_id']}> foi aprovado por {aprovador.mention}."
            )

            # 📝 Envia embed de aprovação
            embed_aprovado = discord.Embed(
                title="✅ Registro Aprovado",
                description=(
                    f"👤 {registro['usuario']}\n"
                    f"🆔 Discord ID: {registro['discord_id']}\n"
                    f"📛 Nome: {registro['nome']}\n"
                    f"📞 Telefone: {registro['telefone']}\n"
                    f"👮 Aprovado por: {aprovador.mention}"
                ),
                color=discord.Color.green()
            )
            await enviar_log(interaction_.guild, embed=embed_aprovado)

        botao = discord.ui.Button(label="Aprovar", style=discord.ButtonStyle.green)
        botao.callback = aprovar_callback
        view.add_item(botao)

        await interaction.guild.get_channel(canal_aprovacao).send(
            f"📥 Registro pendente:\n<@&{Cargos_aprovadores[0]}> favor revisar.\n👤 {interaction.user.mention}\n📛 Nome: {self.nome.value}\n🆔 ID: {self.user_id.value}\n📞 Telefone: {telefone_fmt}",
            view=view
        )

        
    

        embed_pendente = discord.Embed(
            title="📋 Registro Pendente",
            description=(
                f"👤 {interaction.user.name}\n"
                f"🆔 Discord ID: {interaction.user.id}\n"
                f"📛 Nome: {self.nome.value}\n"
                f"📞 Telefone: {telefone_fmt}\n"
                f"✍️ Solicitado por: {interaction.user.mention}"
            ),
            color=discord.Color.gold()
        )
        botao = discord.ui.Button(label="Aprovar Registro", style=discord.ButtonStyle.green)
        botao.callback = aprovar_callback
        view = discord.ui.View()
        view.add_item(botao)
        embed_pendente.set_footer(text="Aguarde a aprovação do registro.")
        embed_pendente.set_thumbnail(url=interaction.user.display_avatar.url)


# ❌ Modal de Demissão
class DemitirModal(discord.ui.Modal, title="Digite o ID discord do membro"):
    discord_id = discord.ui.TextInput(label="ID do Discord", placeholder="123456789012345678", max_length=18)

    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def on_submit(self, interaction: discord.Interaction):
        try:
            did = int(self.discord_id.value)
        except:
            return await interaction.response.send_message("❌ ID inválido.", ephemeral=True)

        usr = buscar_registro_por_discord_id(did)
        if not usr:
            return await interaction.response.send_message(f"❌ Usuário com ID `{did}` não registrado.", ephemeral=True)

        async def confirma(inter: discord.Interaction):
            remover_registro(did)
            log_event(str(inter.user), "Demitido", usr['usuario'])

            membro = inter.guild.get_member(did)
            cargo = inter.guild.get_role(Cargo_membro)
            if membro and cargo:
                await membro.remove_roles(cargo, reason="Demitido")

            await inter.response.send_message(f"✅ {usr['usuario']} demitido.", ephemeral=True)

            embed_demissao = discord.Embed(
                title="❌ Registro Removido",
                description=(
                    f"👤 {usr['usuario']}\n"
                    f"🆔 Discord ID: {did}\n"
                    f"👮 Removido por: {inter.user.mention}"
                ),
                color=discord.Color.red()
            )
            await enviar_log(inter.guild, embed=embed_demissao)

        view = discord.ui.View()
        botao = discord.ui.Button(label="Confirmar", style=discord.ButtonStyle.danger)
        botao.callback = confirma
        view.add_item(botao)
        await interaction.response.send_message(f"⚠️ Confirma a demissão de {usr['usuario']}?", view=view, ephemeral=True)

# 🔧 Comandos principais
class Cadastro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def registro(self, ctx):
        view = discord.ui.View()

        async def abrir_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(RegistroModal(self.bot))

        botao = discord.ui.Button(label="Registrar", style=discord.ButtonStyle.green)
        botao.callback = abrir_modal
        view.add_item(botao)
        await ctx.send("Clique no botão abaixo para registrar seus dados:", view=view)

    @commands.command(name='listar_registros')
    async def listar_registros(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Você não tem permissão para usar este comando.")
            return

        registros_aprovados = listar_registros_aprovados()
        if not registros_aprovados:
            await ctx.send("📭 Nenhum registro aprovado encontrado.")
            return

        for i in range(0, len(registros_aprovados), 5):
            bloco = registros_aprovados[i:i+5]
            embed = discord.Embed(
                title="📋 Registros Aprovados",
                description="Lista dos membros aprovados:",
                color=discord.Color.pink()
            )
            for idx, registro in enumerate(bloco, start=i+1):
                embed.add_field(
                    name=f"{idx}. 👤 {registro['usuario']}",
                    value=f"**Nome:** {registro['nome']}\n**ID:** {registro['id']}\n**Telefone:** {registro['telefone']}",
                    inline=False
                )
            await ctx.send(embed=embed)

    @commands.command()
    async def demitir(self, ctx):
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("❌ Você não tem permissão para usar este comando.")
            return

        view = discord.ui.View()

        async def abrir_modal(interaction: discord.Interaction):
            await interaction.response.send_modal(DemitirModal(self.bot))

        botao = discord.ui.Button(label="Aplicar o procedimento?", style=discord.ButtonStyle.danger)
        botao.callback = abrir_modal
        view.add_item(botao)
        await ctx.send("Clique para aplicar o procedimento em alguém:", view=view)

# 🚀 Setup da extensão
async def setup(bot):
    await bot.add_cog(Cadastro(bot))