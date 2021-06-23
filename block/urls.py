from django.urls import path

from block import views

app_name = "block"

urlpatterns = [
    path(r'blocks-api', views.ListBlocksApiView.as_view()),
    path('blocks-api/<str:hash>/', views.DetailBlocksApiView.as_view()),
    path('blocks-api/<str:hash>/transactions/', views.ListTransactionsApiView.as_view())
]
