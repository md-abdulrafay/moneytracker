from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense, Budget, MonthlyBudget
# Create your views here.
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
import json
from django.http import JsonResponse, HttpResponse
from userpreferences.models import UserPreference
import datetime
from django.core.exceptions import ObjectDoesNotExist
import random
import csv
from expenses.models import Expense
from userincome.models import UserIncome
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt


@login_required(login_url='/authentication/login')
@csrf_exempt
def search_expenses(request):
    if request.method == "POST":
        search_str = json.loads(request.body).get("searchText")
        expenses = Expense.objects.filter(
            description__icontains=search_str, owner=request.user
        ) | Expense.objects.filter(
            category__icontains=search_str, owner=request.user
        ) | Expense.objects.filter(
            amount__icontains=search_str, owner=request.user
        ) | Expense.objects.filter(
            date__icontains=search_str, owner=request.user
        )
        data = expenses.values()
        return JsonResponse(list(data), safe=False)
    return JsonResponse({"error": "Invalid request method"}, status=400)


@login_required(login_url='/authentication/login')
def index(request):
    categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    paginator = Paginator(expenses, 5)
    page_number = request.GET.get('page')
    page_obj = Paginator.get_page(paginator, page_number)
    try:
        currency = UserPreference.objects.get(user=request.user).currency
    except UserPreference.DoesNotExist:
        # Create a default UserPreference object if it does not exist
        UserPreference.objects.create(user=request.user, currency='USD')
        currency = 'USD'
    context = {
        'expenses': expenses,
        'page_obj': page_obj,
        'currency': currency
    }
    return render(request, 'expenses/index.html', context)


@login_required(login_url='/authentication/login')
def add_expense(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'values': request.POST
    }
    if request.method == 'GET':
        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/add_expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user, amount=amount, date=date,
                               category=category, description=description)
        messages.success(request, 'Expense saved successfully')

        return redirect('expenses')


@login_required(login_url='/authentication/login')
def expense_edit(request, id):
    expense = Expense.objects.get(pk=id)
    categories = Category.objects.all()
    context = {
        'expense': expense,
        'values': expense,
        'categories': categories
    }
    if request.method == 'GET':
        return render(request, 'expenses/edit-expense.html', context)
    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request, 'Amount is required')
            return render(request, 'expenses/edit-expense.html', context)
        description = request.POST['description']
        date = request.POST['expense_date']
        category = request.POST['category']

        if not description:
            messages.error(request, 'description is required')
            return render(request, 'expenses/edit-expense.html', context)

        expense.owner = request.user
        expense.amount = amount
        expense. date = date
        expense.category = category
        expense.description = description

        expense.save()
        messages.success(request, 'Expense updated  successfully')

        return redirect('expenses')


def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, 'Expense removed')
    return redirect('expenses')

def get_balance_data(request):
    total_income = UserIncome.objects.filter(owner=request.user).aggregate(total=Sum("amount"))["total"] or 0
    total_expenses = Expense.objects.filter(owner=request.user).aggregate(total=Sum("amount"))["total"] or 0
    balance = total_income - total_expenses
    total_records = Expense.objects.filter(owner=request.user).count()

    return JsonResponse({
        "total_income": total_income,
        "total_expenses": total_expenses,
        "balance": balance,
        "total_records": total_records
    })

def expense_category_summary(request):
    todays_date = datetime.date.today()
    six_months_ago = todays_date - datetime.timedelta(days=30*6)
    start_of_week = todays_date - datetime.timedelta(days=todays_date.weekday())
    start_of_year = datetime.date(todays_date.year, 1, 1)

    expenses = Expense.objects.filter(owner=request.user,
                                      date__gte=six_months_ago, date__lte=todays_date)
    weekly_expenses = Expense.objects.filter(owner=request.user,
                                             date__gte=start_of_week, date__lte=todays_date)
    yearly_expenses = Expense.objects.filter(owner=request.user,
                                             date__gte=start_of_year, date__lte=todays_date)

    finalrep = {}
    category_count = {}
    weekly_rep = {day: 0 for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']}
    yearly_rep = {month: 0 for month in ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']}

    def get_category(expense):
        return expense.category
    category_list = list(set(map(get_category, expenses)))

    def get_expense_category_amount(category):
        amount = 0
        filtered_by_category = expenses.filter(category=category)
        category_count[category] = filtered_by_category.count()

        for item in filtered_by_category:
            amount += item.amount  # Ensure amount is a float
        return amount

    for y in category_list:
        finalrep[y] = get_expense_category_amount(y)

    for expense in weekly_expenses:
        date_str = expense.date.strftime('%A')
        weekly_rep[date_str] += expense.amount

    for expense in yearly_expenses:
        month_str = expense.date.strftime('%B')
        yearly_rep[month_str] += expense.amount

    return JsonResponse({
        'expense_category_data': finalrep,
        'expense_category_count': category_count,
        'weekly_expense_data': weekly_rep,
        'yearly_expense_data': yearly_rep
    }, safe=False)


def stats_view(request):
    return render(request, 'expenses/stats.html')


@login_required(login_url='/authentication/login')
def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=expenses.csv'

    writer = csv.writer(response)
    writer.writerow(['Amount', 'Category', 'Description', 'Date'])

    expenses = Expense.objects.filter(owner=request.user)

    for expense in expenses:
        writer.writerow([expense.amount, expense.category, expense.description, expense.date])

    return response

@login_required(login_url='/authentication/login')
def dashboard_view(request):
    return render(request, 'expenses/dashboard.html')

@login_required(login_url='/authentication/login')
def category_insights_view(request):
    return render(request, 'expenses/category_insights.html')

@login_required(login_url='/authentication/login')
def set_budget(request):
    if request.method == "POST":
        if "category" in request.POST and request.POST["category"] != "all":
            category_id = request.POST["category"]
            amount = request.POST["amount"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            
            category = Category.objects.get(id=category_id)
            budget, created = Budget.objects.get_or_create(
                owner=request.user, category=category, defaults={"amount": amount, "start_date": start_date, "end_date": end_date}
            )
            if not created:
                budget.amount = amount
                budget.start_date = start_date
                budget.end_date = end_date
                budget.save()

            request.session['budget_message'] = "Category budget set successfully!"
        else:
            amount = request.POST["amount"]
            start_date = request.POST["start_date"]
            end_date = request.POST["end_date"]
            
            monthly_budget, created = MonthlyBudget.objects.get_or_create(
                owner=request.user, defaults={"amount": amount, "start_date": start_date, "end_date": end_date}
            )
            if not created:
                monthly_budget.amount = amount
                monthly_budget.start_date = start_date
                monthly_budget.end_date = end_date
                monthly_budget.save()

            request.session['budget_message'] = "Monthly budget set successfully!"

        return redirect("budget-summary")

    categories = Category.objects.all()
    return render(request, "expenses/set_budget.html", {"categories": categories})

def reset_expired_budgets(user):
    today = datetime.date.today()
    expired_budgets = Budget.objects.filter(owner=user, end_date__lt=today)
    expired_monthly_budgets = MonthlyBudget.objects.filter(owner=user, end_date__lt=today)
    reset_message = None

    if expired_budgets.exists() or expired_monthly_budgets.exists():
        reset_message = "Some budgets have been reset as their end date has exceeded."

    for budget in expired_budgets:
        budget.amount = 0
        budget.save()

    for monthly_budget in expired_monthly_budgets:
        monthly_budget.amount = 0
        monthly_budget.save()

    return reset_message

@login_required(login_url='/authentication/login')
def budget_summary(request):
    reset_message = reset_expired_budgets(request.user)  # Reset expired budgets

    budgets = Budget.objects.filter(owner=request.user)
    
    # Fetch total spending per category using category names (since Expense.category is a string)
    expenses = Expense.objects.filter(owner=request.user).values("category").annotate(total_spent=Sum("amount"))
    
    # Create a mapping from category names (Expense model) to their total spent
    expense_dict = {e["category"]: e["total_spent"] for e in expenses}

    for budget in budgets:
        # Match category name (not ID) to correctly get spent amount
        budget.spent = expense_dict.get(budget.category.name, 0)
        budget.remaining = budget.amount - budget.spent

    try:
        monthly_budget = MonthlyBudget.objects.get(owner=request.user)
    except MonthlyBudget.DoesNotExist:
        monthly_budget = None

    total_spent = Expense.objects.filter(owner=request.user, date__month=datetime.date.today().month).aggregate(total=Sum("amount"))["total"] or 0
    remaining = monthly_budget.amount - total_spent if monthly_budget else 0

    budget_message = request.session.pop('budget_message', None)

    return render(request, "expenses/budget_summary.html", {
        "budgets": budgets,
        "monthly_budget": monthly_budget,
        "total_spent": total_spent,
        "remaining": remaining,
        "budget_message": budget_message,
        "reset_message": reset_message
    })

@login_required(login_url='/authentication/login')
def edit_budget(request, id):
    budget = Budget.objects.get(pk=id)
    categories = Category.objects.all()
    if request.method == "POST":
        budget.amount = request.POST["amount"]
        budget.start_date = request.POST["start_date"]
        budget.end_date = request.POST["end_date"]
        budget.save()
        messages.success(request, "Budget updated successfully!")
        return redirect("budget-summary")
    return render(request, "expenses/edit_budget.html", {"budget": budget, "categories": categories})

@login_required(login_url='/authentication/login')
def delete_budget(request, id):
    budget = Budget.objects.get(pk=id)
    budget.delete()
    messages.success(request, "Budget deleted successfully!")
    return redirect("budget-summary")

@login_required(login_url='/authentication/login')
def edit_monthly_budget(request, id):
    monthly_budget = MonthlyBudget.objects.get(pk=id)
    if request.method == "POST":
        monthly_budget.amount = request.POST.get("amount", monthly_budget.amount)
        monthly_budget.start_date = request.POST.get("start_date", monthly_budget.start_date)
        monthly_budget.end_date = request.POST.get("end_date", monthly_budget.end_date)
        monthly_budget.save()
        messages.success(request, "Monthly budget updated successfully!")
        return redirect("budget-summary")
    return render(request, "expenses/edit_monthly_budget.html", {"monthly_budget": monthly_budget})

@login_required(login_url='/authentication/login')
def delete_monthly_budget(request, id):
    monthly_budget = MonthlyBudget.objects.get(pk=id)
    monthly_budget.delete()
    messages.success(request, "Monthly budget deleted successfully!")
    return redirect("budget-summary")

