from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='/django/')),  # redireciona raiz para /django/
    path('admin/', admin.site.urls),
    path('django/', include('sistema_de_vendas.urls')),  # monta Django em /django/
]