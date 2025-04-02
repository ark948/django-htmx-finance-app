from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required


from .models import Transaction
from .filters import TransactionFilter

# Create your views here.

def index(request: HttpRequest) -> HttpResponse:
    response = render(request, "tracker/index.html", {})
    return response



@login_required
def transactions_list(request):
    # django-filter FilterSet will provide a form automatically
    # in template we'll render that form, using widget-tweaks we'll introduce custom class to benefit from tailwindcss and daisyui
    transaction_filter = TransactionFilter(
        request.GET,
        # without specifying "select_related('category')", a separate sql query is made for every transaction object
        # which is terrible performance (n+1 problem)
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
            'filter': transaction_filter,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses
        }
    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)
    return render(request, 'tracker/transactions-list.html', context)