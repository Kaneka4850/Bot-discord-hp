# 🤖 Bot Hospital

**Bot Hospital** é um bot desenvolvido em Python com `discord.py` para auxiliar na organização de **hospitais em servidores de FiveM (GTA RP)**. Ele automatiza registros, tickets de atendimento, convocação de membros, advertências e muito mais, otimizando a rotina de gestão hospitalar em servidores RP.

---

## ✨ Funcionalidades

- 📋 Registro de membros com aprovação manual
- 🧾 Listagem de membros aprovados
- ❌ Demissão de membros (admin)
- 📢 Convocação de membros
- ⚠️ Sistema de advertência
- 💬 Criação de canais privados de trabalho (tickets)
- 📜 Comando de ajuda com todos os comandos disponíveis

---

## 📚 Comandos disponíveis

Use todos os comandos com o prefixo `!`

| Comando             | Descrição                                               |
|---------------------|----------------------------------------------------------|
| `!registro`         | Inicia o processo de registro.                           |
| `!listar_registros` | Lista todos os registros aprovados.                      |
| `!demitir`          | Demite um agente (somente admins).                       |
| `!convocar`         | Convoca um membro para uma reunião.                      |
| `!advertir`         | Aplica uma advertência a um membro.                      |
| `!comandos`         | Lista todos os comandos disponíveis.                     |
| `!ticket`           | Abre seu chat privado e sua aba de farm.                 |

---

## ⚙️ Tecnologias Utilizadas

- [Python](https://www.python.org/) 3.10+
- [discord.py](https://discordpy.readthedocs.io/)
- [SQLAlchemy](https://www.sqlalchemy.org/) + SQLite
- [python-dotenv](https://pypi.org/project/python-dotenv/)

---

## 🧰 Requisitos

- Python 3.10 ou superior
- Conta de desenvolvedor no Discord (com bot criado)
- Permissões de administrador no servidor onde o bot será usado

---

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/bot-hospital.git
cd bot-hospital
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Crie um arquivo .env com suas configurações:
```bash
DISCORD_TOKEN=seu_token_aqui
```
4. Execute o bot:
```bash
python main.py
```





