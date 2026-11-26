# =============================================================
# Diário da Fada do Dente 🧚
# API em FastAPI + PostgreSQL para o desafio de Docker Compose
# =============================================================

# ---------- Bibliotecas ----------
import os                      # lê as variáveis de ambiente (DB_USER, DB_PASSWORD...)
import random                  # sorteia a mensagem da fada
from contextlib import asynccontextmanager  # permite rodar código quando a API liga
from datetime import date      # tipo "data" (dia em que o dente caiu)
from typing import Literal     # restringe valores aceitos ("cima" ou "baixo")

import psycopg                 # driver que conversa com o PostgreSQL
from fastapi import FastAPI, HTTPException  # FastAPI monta a API; HTTPException devolve erros (ex.: 404)
from psycopg.rows import dict_row           # faz o banco devolver linhas como dicionário (vira JSON fácil)
from pydantic import BaseModel              # valida os dados que chegam nos pedidos

# ---------- Conexão com o banco ----------
# Nada de senha no código: tudo vem de variáveis de ambiente,
# que o Docker Compose vai preencher a partir do arquivo .env.
# os.environ['X'] -> obrigatória (se faltar, a API não sobe e avisa)
# os.environ.get('X', 'padrão') -> opcional, com valor padrão
DB_URL = (
    f"postgresql://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}"
    f"@{os.environ['DB_HOST']}:{os.environ.get('DB_PORT', '5432')}/{os.environ['DB_NAME']}"
)
# Exemplo do resultado: postgresql://fada:senha123@db:5432/fada_do_dente
#                                    usuário  senha  host porta  banco

# Mensagens que a fada sorteia a cada dente registrado
MENSAGENS_DA_FADA = [
    "🧚 A fada voou até aqui e deixou um brilho na janela!",
    "✨ Esse dente vai virar uma estrela no castelo da fada!",
    "🦷 Dente guardado no cofre mágico com sucesso!",
    "🌙 A fada passa hoje à noite, durma cedo!",
    "👑 Mais um dente para a coroa da Rainha das Fadas!",
]


def conectar():
    """Abre uma conexão com o PostgreSQL.
    Usada com 'with', a conexão fecha sozinha no final
    (e faz o commit das alterações, se não houver erro)."""
    return psycopg.connect(DB_URL, row_factory=dict_row)


# ---------- Inicialização ----------
# O 'lifespan' roda UMA vez, quando a API liga (antes do 'yield').
# Aqui ele cria as tabelas, se ainda não existirem.
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield  # daqui para baixo a API fica no ar, atendendo pedidos


# Cria a aplicação. O título aparece no Swagger (/docs).
app = FastAPI(title="Diário da Fada do Dente 🧚", lifespan=lifespan)


# ---------- Modelos (o formato dos dados que a API recebe) ----------
# O Pydantic confere se o pedido veio certo. Se mandarem
# "arcada": "meio", a API recusa sozinha com erro 422.
class Pessoa(BaseModel):
    nome: str


class Dente(BaseModel):
    pessoa_id: int
    data: date                        # formato: "2026-11-24"
    arcada: Literal["cima", "baixo"]  # só aceita esses dois valores
    qual_dente: str                   # ex.: "incisivo central"
    presente: float = 0               # opcional; se não mandar, vale 0


# ---------- Rota inicial ----------
# GET /  -> só uma mensagem de boas-vindas (bom para testar se a API está no ar)
@app.get("/")
def inicio():
    return {"mensagem": "Bem-vindo ao Diário da Fada do Dente! Acesse /docs 🧚"}


# ---------- Pessoas ----------
# POST /pessoas -> cadastra uma criança (C do CRUD)
@app.post("/pessoas", status_code=201)  # 201 = "criado com sucesso"
def criar_pessoa(pessoa: Pessoa):
    with conectar() as conn:
        # %s = espaço reservado: o psycopg encaixa o valor com segurança.
        # NUNCA monte SQL juntando texto (f-string), por causa do SQL injection.
        # RETURNING * devolve a linha criada (com o id novo).
        return conn.execute(
            "INSERT INTO pessoas (nome) VALUES (%s) RETURNING *", (pessoa.nome,)
        ).fetchone()


# GET /pessoas -> lista todas as crianças (R do CRUD)
@app.get("/pessoas")
def listar_pessoas():
    with conectar() as conn:
        return conn.execute("SELECT * FROM pessoas ORDER BY id").fetchall()


# ---------- Dentes (CRUD completo) ----------
# POST /dentes -> registra um dente (C do CRUD)
@app.post("/dentes", status_code=201)
def registrar_dente(dente: Dente):
    with conectar() as conn:
        # Antes de gravar, confere se a criança existe
        if not conn.execute("SELECT 1 FROM pessoas WHERE id = %s", (dente.pessoa_id,)).fetchone():
            raise HTTPException(404, "Essa criança não está no livro da fada!")
        novo = conn.execute(
            """INSERT INTO dentes (pessoa_id, data, arcada, qual_dente, presente)
               VALUES (%s, %s, %s, %s, %s) RETURNING *""",
            (dente.pessoa_id, dente.data, dente.arcada, dente.qual_dente, dente.presente),
        ).fetchone()
    # Responde com o dente gravado + uma mensagem sorteada da fada
    return {"dente": novo, "fada_diz": random.choice(MENSAGENS_DA_FADA)}


# GET /dentes -> lista todos os dentes, com o nome da criança (R do CRUD)
@app.get("/dentes")
def listar_dentes():
    with conectar() as conn:
        # JOIN: junta as duas tabelas usando a chave estrangeira
        # (dentes.pessoa_id = pessoas.id) para trazer o nome junto
        return conn.execute(
            """SELECT d.*, p.nome FROM dentes d
               JOIN pessoas p ON p.id = d.pessoa_id ORDER BY d.data DESC"""
        ).fetchall()


# GET /dentes/{dente_id} -> mostra um dente específico (R do CRUD)
# {dente_id} na rota vira o parâmetro dente_id da função
@app.get("/dentes/{dente_id}")
def buscar_dente(dente_id: int):
    with conectar() as conn:
        dente = conn.execute("SELECT * FROM dentes WHERE id = %s", (dente_id,)).fetchone()
    if not dente:
        raise HTTPException(404, "A fada não encontrou esse dente 🔍")
    return dente


# PUT /dentes/{dente_id} -> atualiza um dente (U do CRUD)
@app.put("/dentes/{dente_id}")
def atualizar_dente(dente_id: int, dente: Dente):
    with conectar() as conn:
        atualizado = conn.execute(
            """UPDATE dentes SET pessoa_id=%s, data=%s, arcada=%s, qual_dente=%s, presente=%s
               WHERE id=%s RETURNING *""",
            (dente.pessoa_id, dente.data, dente.arcada, dente.qual_dente, dente.presente, dente_id),
        ).fetchone()
    if not atualizado:
        raise HTTPException(404, "A fada não encontrou esse dente 🔍")
    return atualizado


# DELETE /dentes/{dente_id} -> apaga um dente (D do CRUD)
@app.delete("/dentes/{dente_id}", status_code=204)  # 204 = "feito, sem conteúdo para devolver"
def apagar_dente(dente_id: int):
    with conectar() as conn:
        apagado = conn.execute("DELETE FROM dentes WHERE id = %s RETURNING id", (dente_id,)).fetchone()
    if not apagado:
        raise HTTPException(404, "A fada não encontrou esse dente 🔍")


# ---------- Diversão ----------
# GET /placar -> ranking: quem perdeu mais dentes e juntou mais "tesouro"
@app.get("/placar")
def placar():
    with conectar() as conn:
        # LEFT JOIN: traz também quem ainda não perdeu nenhum dente (fica com 0)
        # COUNT conta os dentes; SUM soma os presentes; COALESCE troca "vazio" por 0
        # GROUP BY agrupa por criança, para contar e somar de cada uma
        return conn.execute(
            """SELECT p.nome, COUNT(d.id) AS dentes, COALESCE(SUM(d.presente), 0) AS tesouro
               FROM pessoas p LEFT JOIN dentes d ON d.pessoa_id = p.id
               GROUP BY p.nome ORDER BY dentes DESC"""
        ).fetchall()