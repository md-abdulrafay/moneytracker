from django.urls import path
from . import views
from .views import get_balance_data
from .views import set_budget, budget_summary, edit_budget, delete_budget, edit_monthly_budget, delete_monthly_budget

from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', views.index, name='expenses'),
    path('add/', views.add_expense, name='add-expenses'),
    path('edit/<int:id>/', views.expense_edit, name='expense-edit'),
    path('delete/<int:id>/', views.delete_expense, name='expense-delete'),
    path('search-expenses/', csrf_exempt(views.search_expenses), name='search_expenses'),
    path('expense_category_summary/', views.expense_category_summary, name='expense_category_summary'),
    path('stats/', views.stats_view, name='stats'),
    path('export-expenses-csv/', views.export_csv, name='export-expenses-csv'),
    path("api/balance/", get_balance_data, name="balance-api"),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('category_insights/', views.category_insights_view, name='category_insights'),
    path("set-budget/", set_budget, name="set-budget"),
    path("budget-summary/", budget_summary, name="budget-summary"),
    path("edit-budget/<int:id>/", edit_budget, name="edit-budget"),
    path("delete-budget/<int:id>/", delete_budget, name="delete-budget"),
    path("edit-monthly-budget/<int:id>/", edit_monthly_budget, name="edit-monthly-budget"),
    path("delete-monthly-budget/<int:id>/", delete_monthly_budget, name="delete-monthly-budget"),
]
