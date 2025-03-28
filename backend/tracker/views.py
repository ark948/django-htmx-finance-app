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
    transaction_filter = TransactionFilter(
        request=request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    context = {'filter': transaction_filter}
    if request.htmx:
        response = render(request, "tracker/partials/transactions-container.html", context)
        return response
    response = render(request, "tracker/transactions-list.html", context)
    return response