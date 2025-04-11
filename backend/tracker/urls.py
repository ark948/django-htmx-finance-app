from django.urls import path

from . import views

app_name = 'tracker'
urlpatterns = [
    path('transactions-no-scroll-partial/', views.get_transactions_no_scroll_partial, name='no-scroll-partial'),
    path('transactions-no-scroll/', views.get_transactions_no_scroll, name='no-scroll'),
    path('transactions/export/', views.export, name='export'),
    path('transactions-charts', views.transactions_charts, name='transactions-charts'),
    path('transactions/<int:pk>/delete/', views.delete_transaction, name='delete-transaction'),
    path('transactions/<int:pk>/update/', views.update_transaction, name='update-transaction'),
    path('transactions/create', views.create_transaction, name='create-transaction'),
    path("transactions/", views.transactions_list, name='transactions-list'),
    path('get-transactions/', views.get_transactions, name='get-transactions'),
    path("", views.index, name='index'),
]