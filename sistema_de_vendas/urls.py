from django.urls import path
from sistema_de_vendas.views import home, listar_clientes, adicionar_cliente, verificar_status, cliente_por_id, cliente_mais_antigo, atualizar_cliente, remover_cliente_por_id, buscar_cliente

urlpatterns = [
    path('', home, name='home'),
    path('listar_clientes/', listar_clientes, name='listar_clientes'),
    path('adicionar/',adicionar_cliente, name='adicionar_cliente'),
    path('status/', verificar_status, name='verificar_status'),
    path('cliente/adicionar/', adicionar_cliente, name='adicionar_cliente'),
    path('cliente/<int:cliente_id>/', cliente_por_id, name='cliente_por_id'),
    path('cliente/buscar/', buscar_cliente, name='buscar_cliente'),
    path('cliente/mais_antigo/', cliente_mais_antigo, name='cliente_mais_antigo'),
    path("cliente/atualizar/", atualizar_cliente, name="atualizar_cliente"),
    path("cliente/remover/", remover_cliente_por_id, name="remover_cliente")
]
