from sqlalchemy.orm import Session
from database.membro_service import verificar_cargo
from database.membro_service import formatar_nome
from database.membro_service import Prisao
from database.adevertencia_service import criar_embed_advertencia
from .models.ticket import Ticket

# 🔹 Membro
def criar_membro(db: Session, dados: dict) -> Membro:
    membro = Membro(**dados)
    db.add(membro)
    db.commit()
    db.refresh(membro)
    return membro

def buscar_membro_por_id(db: Session, membro_id: int) -> Membro:
    return db.query(Membro).filter(Membro.id == membro_id).first()

# 🔹 Prisão
def registrar_prisao(db: Session, dados: dict) -> Prisao:
    prisao = Prisao(**dados)
    db.add(prisao)
    db.commit()
    db.refresh(prisao)
    return prisao

def buscar_prisao_por_id(db: Session, prisao_id: int) -> Prisao:
    return db.query(Prisao).filter(Prisao.id == prisao_id).first()

# 🔹 Advertência
def aplicar_advertencia(db: Session, dados: dict) -> Advertencia:
    advertencia = Advertencia(**dados)
    db.add(advertencia)
    db.commit()
    db.refresh(advertencia)
    return advertencia

def buscar_advertencia_por_id(db: Session, advertencia_id: int) -> Advertencia:
    return db.query(Advertencia).filter(Advertencia.id == advertencia_id).first()

# 🔹 Ticket
def criar_ticket(db: Session, dados: dict) -> Ticket:
    ticket = Ticket(**dados)
    db.add(ticket)
    db.commit()
    db.refresh(ticket)
    return ticket

def buscar_ticket_por_id(db: Session, ticket_id: int) -> Ticket:
    return db.query(Ticket).filter(Ticket.id == ticket_id).first()