from django.urls import path
from . import views

app_name = 'budget_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/sheets/update-budget/', views.update_budget, name='update_budget'),
    path('api/sheets/add-expense/', views.add_expense, name='add_expense'),
    path('api/sheets/sync/', views.sync_sheets, name='sync_sheets'),
]