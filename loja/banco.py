from sqlalchemy.pool import StaticPool
from sqlmodel import Field, SQLModel, create_engine

URL_BANCO = "sqlite:///loja.db"


class ProdutoRegistro(SQLModel, table=True):
    """Uma linha da tabela produto: o produto do jeito que o banco guarda."""
    __tablename__ = "produto"

    id: int | None = Field(default=None, primary_key=True)
    tipo: str
    nome: str = Field(unique=True)
    preco: float
    tamanho: str
    manga: str | None = None
    modelagem: str | None = None

def criar_engine(url=URL_BANCO):
    # check_same_thread é um argumento só do SQLite: outros bancos não o conhecem
    argumentos = {"check_same_thread": False} if url.startswith("sqlite") else {}
    return create_engine(url, connect_args=argumentos)

def engine_em_memoria():
    """Banco que vive só na memória: ideal para testes rápidos."""
    return create_engine("sqlite://", connect_args={"check_same_thread": False},
                          poolclass=StaticPool)

def criar_tabelas(engine):
    SQLModel.metadata.create_all(engine)
