from django.shortcuts import render, redirect
from .utils import servidor_online
import requests

API_URL = "http://127.0.0.1:8001/clientes/"

def home(request):
    return render(request, "sistema_de_vendas/home.html")

def listar_clientes(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    response = requests.get(API_URL)
    clientes = response.json()
    return render(request, "sistema_de_vendas/listar.html", {"clientes": clientes})

def adicionar_cliente(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    if request.method == "POST":
        data = {
            "nome": request.POST["nome"],
            "idade": int(request.POST["idade"]),
            "usuario": request.POST["usuario"],
            "senha": request.POST["senha"],
        }
        requests.post(API_URL, json=data)
        return redirect("listar_clientes")
    return render(request, "sistema_de_vendas/adicionar.html")

def verificar_status(request):
    try:
        response = requests.get("http://127.0.0.1:8001/status/", timeout=3)
        status = response.json()
    except requests.exceptions.RequestException:
        status = {"status": "Servidor desligado"}
    return render(request, "sistema_de_vendas/status.html", {"status": status})


def cliente_por_id(request, cliente_id):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    response = requests.get(f"{API_URL}{cliente_id}")
    if response.status_code == 404:
        return render(request, "sistema_de_vendas/erro.html", {"mensagem": "Cliente não encontrado"})
    cliente = response.json()
    return render(request, "sistema_de_vendas/cliente.html", {"cliente": cliente})


def buscar_cliente(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    cliente = None
    erro = None
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")
        try:
            response = requests.get(f"{API_URL}{cliente_id}")
            if response.status_code == 404:
                erro = "Cliente não encontrado"
            else:
                cliente = response.json()
        except requests.exceptions.RequestException:
            erro = "Erro ao conectar com o servidor"
    return render(request, "sistema_de_vendas/buscar_cliente.html", {"cliente": cliente, "erro": erro})


def cliente_mais_antigo(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    response = requests.get(f"{API_URL}mais_antigo/")
    if response.status_code == 404:
        return render(request, "sistema_de_vendas/erro.html", {"mensagem": "Nenhum cliente cadastrado"})
    cliente = response.json()
    return render(request, "sistema_de_vendas/cliente.html", {"cliente": cliente})

def atualizar_cliente(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    cliente = None
    erro = None

    if request.method == "POST":
        # Se vier o ID do cliente, buscar os dados
        if "cliente_id" in request.POST and "nome" not in request.POST:
            cliente_id = request.POST["cliente_id"]
            response = requests.get(f"{API_URL}{cliente_id}")
            if response.status_code == 404:
                erro = "Cliente não encontrado"
            else:
                cliente = response.json()

        # Se vier os dados do formulário, atualizar
        elif "nome" in request.POST:
            cliente_id = request.POST["cliente_id"]
            data = {
                "nome": request.POST["nome"],
                "idade": int(request.POST["idade"]),
                "usuario": request.POST["usuario"],
                "senha": request.POST["senha"],
            }
            requests.put(f"{API_URL}{cliente_id}", json=data)
            return redirect("listar_clientes")

    return render(request, "sistema_de_vendas/atualizar.html", {"cliente": cliente, "erro": erro})


def remover_cliente_por_id(request):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    erro = None
    if request.method == "POST":
        cliente_id = request.POST.get("cliente_id")  # pega o ID digitado
        response = requests.delete(f"{API_URL}{cliente_id}")
        if response.status_code == 404:
            erro = "Cliente não encontrado"
        else:
            return redirect("home")  # cliente removido com sucesso
    return render(request, "sistema_de_vendas/remover_cliente.html", {"erro": erro})


def remover_cliente_confirmar(request, cliente_id):
    if not servidor_online():
        return render(request, "sistema_de_vendas/manutencao.html")
    
    requests.delete(f"{API_URL}{cliente_id}")
    return redirect("home")
