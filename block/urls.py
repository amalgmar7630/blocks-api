from django.urls import path

from block import views

app_name = "block"

urlpatterns = [
    path(r'blocks', views.ListBlocksApiView.as_view()),
    path('blocks/<str:hash>/', views.DetailBlocksApiView.as_view()),
    path('blocks/<str:hash>/transactions/', views.ListTransactionsApiView.as_view())
]
