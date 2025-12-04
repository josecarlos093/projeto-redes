# fast_api/main.py
import os
import django

# Inicializa o Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "setup.settings")
django.setup()

from fastapi import FastAPI, HTTPException
from sistema_de_vendas.models import Cliente
from pydantic import BaseModel
from datetime import date
import bcrypt


app = FastAPI()

# --- Função para criptografar a senha ---
def hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode(), bcrypt.gensalt()).decode()


# Schema usado para criação e atualização
class ClienteSchema(BaseModel):
    nome: str
    idade: int
    usuario: str
    senha: str


# ---------------- ROTAS ----------------

# LISTAR TODOS
@app.get("/clientes/")
def listar_clientes():
    return [
        {
            "id": c.id,
            "nome": c.nome,
            "idade": c.idade,
            "usuario": c.usuario,
            "senha": c.senha,  # hash da senha
            "tempo_cadastro": c.tempo_cadastro,
        }
        for c in Cliente.objects.all()
    ]


# OBTER POR ID
@app.get("/clientes/{cliente_id}")
def obter_cliente(cliente_id: int):
    try:
        c = Cliente.objects.get(id=cliente_id)
        return {
            "id": c.id,
            "nome": c.nome,
            "idade": c.idade,
            "usuario": c.usuario,
            "senha": c.senha,  # hash
            "tempo_cadastro": c.tempo_cadastro,
        }
    except Cliente.DoesNotExist:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")


# CRIAR CLIENTE (com senha criptografada)
@app.post("/clientes/")
def criar_cliente(cliente: ClienteSchema):

    senha_hash = hash_senha(cliente.senha)

    c = Cliente.objects.create(
        nome=cliente.nome,
        idade=cliente.idade,
        usuario=cliente.usuario,
        senha=senha_hash,
    )

    return {
        "id": c.id,
        "nome": c.nome,
        "idade": c.idade,
        "usuario": c.usuario,
        "senha": c.senha,  # hash
        "tempo_cadastro": c.tempo_cadastro,
    }


# ATUALIZAR CLIENTE (com senha criptografada)
@app.put("/clientes/{cliente_id}")
def atualizar_cliente(cliente_id: int, cliente: ClienteSchema):
    try:
        c = Cliente.objects.get(id=cliente_id)

        senha_hash = hash_senha(cliente.senha)

        c.nome = cliente.nome
        c.idade = cliente.idade
        c.usuario = cliente.usuario
        c.senha = senha_hash
        c.save()

        return {
            "id": c.id,
            "nome": c.nome,
            "idade": c.idade,
            "usuario": c.usuario,
            "senha": c.senha,  # hash
            "tempo_cadastro": c.tempo_cadastro,
        }

    except Cliente.DoesNotExist:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")


# REMOVER CLIENTE
@app.delete("/clientes/{cliente_id}")
def remover_cliente(cliente_id: int):
    try:
        c = Cliente.objects.get(id=cliente_id)
        c.delete()
        return {"detail": "Cliente removido"}
    except Cliente.DoesNotExist:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")


# STATUS DO SERVIDOR
@app.get("/status/")
def verificar_status():
    return {"status": "Servidor ativo", "data": str(date.today())}


# CLIENTE MAIS ANTIGO
@app.get("/clientes/mais_antigo/")
def cliente_mais_antigo():
    c = Cliente.objects.order_by("tempo_cadastro").first()
    if c:
        return {
            "id": c.id,
            "nome": c.nome,
            "idade": c.idade,
            "usuario": c.usuario,
            "senha": c.senha,  # hash
            "tempo_cadastro": c.tempo_cadastro,
        }
    else:
        raise HTTPException(status_code=404, detail="Nenhum cliente cadastrado")
