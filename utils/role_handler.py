async def alinhar_cargo(member, cargo_alvo, cargos_remover=[]):
    try:
        if cargo_alvo not in member.roles:
            await member.add_roles(cargo_alvo)
        if cargos_remover:
            for cargo in cargos_remover:
                if cargo in member.roles:
                    await member.remove_roles(cargo)
        return True
    except Exception:
        return False