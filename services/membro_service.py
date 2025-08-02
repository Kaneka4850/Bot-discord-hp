from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///membros.db"

Base = declarative_base()
engine = create_engine(DATABASE_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Membro(Base):
    __tablename__ = "membros"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    telefone = Column(String, nullable=False)
    usuario = Column(String, nullable=False)
    discord_id = Column(Integer, unique=True, nullable=False)
    aprovado = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)

def adicionar_registro(registro: dict):
    with SessionLocal() as session:
        membro = session.query(Membro).filter_by(discord_id=registro["discord_id"]).first()
        if membro:
            # Atualiza dados se já existir
            membro.nome = registro["nome"]
            membro.user_id = registro["id"]
            membro.telefone = registro["telefone"]
            membro.usuario = registro["usuario"]
            membro.aprovado = registro.get("aprovado", False)
        else:
            membro = Membro(
                nome=registro["nome"],
                user_id=registro["id"],
                telefone=registro["telefone"],
                usuario=registro["usuario"],
                discord_id=registro["discord_id"],
                aprovado=registro.get("aprovado", False)
            )
            session.add(membro)
        session.commit()

def aprovar_registro(discord_id: int):
    with SessionLocal() as session:
        membro = session.query(Membro).filter_by(discord_id=discord_id).first()
        if membro:
            membro.aprovado = True
            session.commit()

def listar_registros_aprovados():
    with SessionLocal() as session:
        membros = session.query(Membro).filter_by(aprovado=True).all()
        return [
            {
                "nome": m.nome,
                "id": m.user_id,
                "telefone": m.telefone,
                "usuario": m.usuario,
                "discord_id": m.discord_id,
                "aprovado": m.aprovado
            }
            for m in membros
        ]

def remover_registro(discord_id: int):
    with SessionLocal() as session:
        membro = session.query(Membro).filter_by(discord_id=discord_id).first()
        if membro:
            session.delete(membro)
            session.commit()

def buscar_registro_por_discord_id(discord_id: int):
    with SessionLocal() as session:
        membro = session.query(Membro).filter_by(discord_id=discord_id).first()
        if membro:
            return {
                "nome": membro.nome,
                "id": membro.user_id,
                "telefone": membro.telefone,
                "usuario": membro.usuario,
                "discord_id": membro.discord_id,
                "aprovado": membro.aprovado
            }
        return None