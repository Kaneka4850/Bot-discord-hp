import discord

class MenuPersistente(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="📋 Abrir Formulário de Prisão", style=discord.ButtonStyle.green, custom_id="abrir_formulario_prisao")
    async def abrir_formulario(self, interaction: discord.Interaction, button: discord.ui.Button):
        from cogs.registro_prisao import FormularioPrisao
        await interaction.response.send_modal(FormularioPrisao())