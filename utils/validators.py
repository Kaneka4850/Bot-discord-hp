def validar_nome(nome: str) -> bool:
    return nome.isalpha() and len(nome) >= 3

def validar_idade(idade: int) -> bool:
    return 18 <= idade <= 70

def validar_cargo(cargo: str, permitidos: list) -> bool:
    return cargo.lower() in [c.lower() for c in permitidos]