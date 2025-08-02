def verificar_cargo(membro, cargo_id):
    return membro.guild_permissions.administrator or any(role.id == cargo_id for role in membro.roles)

def formatar_nome(membro):
    return membro.display_name or membro.name