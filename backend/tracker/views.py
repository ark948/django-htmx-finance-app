from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from django_htmx.http import retarget
from django.core.paginator import Paginator
from django.conf import settings


from .models import Transaction
from .filters import TransactionFilter
from .forms import TransactionForm
from .charting import plot_income_expenses_bar_chart, plot_category_pie_chart
from .resources import TransactionResource

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

    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    transaction_page = paginator.page(1) # first page by default is page 1

    total_income = transaction_filter.qs.get_total_income()
    total_expenses = transaction_filter.qs.get_total_expenses()
    context = {
            'transactions': transaction_page,
            'filter': transaction_filter,
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_income': total_income - total_expenses
        }
    if request.htmx:
        return render(request, 'tracker/partials/transactions-container.html', context)
    return render(request, 'tracker/transactions-list.html', context)



@login_required
def create_transaction(request: HttpRequest):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            context = { 'message': "Transaction was added successfully." }
            return render(request, 'tracker/partials/transaction-success.html', context)
        else:
            context = { 'form': form } # will have errors
            response = render(request, 'tracker/partials/create-transaction.html', context)
            return retarget(response, '#transaction-block')
        
    context = { 'form': TransactionForm() }
    return render(request, 'tracker/partials/create-transaction.html', context)



@login_required
def update_transaction(request: HttpRequest, pk: int):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save()
            context = { 'message': "Transaction was updated successfully." }
            return render(request, 'tracker/partials/transaction-success.html', context=context)
        else:
            context = {
                'form': form, # return form with errors so they can be displayed to user
                'transaction': transaction
            }
            response = render(request, 'tracker/partials/update-transaction.html', context=context)
            return retarget(response, '#transaction-block')
    context = {
        'form': TransactionForm(instance=transaction),
        'transaction': transaction
    }
    return render(request, 'tracker/partials/update-transaction.html', context=context)



@login_required
@require_http_methods(["DELETE"])
def delete_transaction(request: HttpRequest, pk: int):
    transaction = get_object_or_404(Transaction, pk=pk, user=request.user)
    transaction.delete()
    context = { "message": f"Transaction of {transaction.amount} on {transaction.date} was deleted successfully." }
    return render(request, "tracker/partials/transaction-success.html", context)



@login_required
def get_transactions(request: HttpRequest):
    # import time
    # time.sleep(2) # this is just to test the loading indicator
    page = request.GET.get('page', 1) # ?page=2
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    paginator = Paginator(transaction_filter.qs, settings.PAGE_SIZE)
    context = { 'transactions': paginator.page(page) }
    return render( request, 'tracker/partials/transactions-container.html#transaction_list', context )



@login_required
def get_transactions_no_scroll(request: HttpRequest):
    transaction_filter = TransactionFilter( 
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    paginator = Paginator(transaction_filter.qs, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    context = { 'page_obj' : page_obj }
    return render( request, 'tracker/partials/transactions-container-no-scroll.html', context )



@login_required
def get_transactions_no_scroll_partial(request: HttpRequest):
    transaction_filter = TransactionFilter( 
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    paginator = Paginator(transaction_filter.qs, 5)
    page_number = request.GET.get('page', 1)
    context = { 'page_obj' : paginator.get_page(page_number) }
    return render( request, 'tracker/partials/transactions-container-no-scroll.html#test-partial', context )



@login_required
def transactions_charts(request: HttpRequest):
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )
    income_expense_bar = plot_income_expenses_bar_chart(transaction_filter.qs)

    category_income_pie = plot_category_pie_chart(
            transaction_filter.qs.filter(type='income')
        )
    category_expense_pie = plot_category_pie_chart(
            transaction_filter.qs.filter(type='expense')
        )
    context = {
        'filter': transaction_filter,
        'income_expense_barchart': income_expense_bar.to_html(),
        'category_income_pie': category_income_pie.to_html(),
        'category_expense_pie': category_expense_pie.to_html()
    }
    if request.htmx:
        return render(request, "tracker/partials/charts-container.html", context)
    return render(request, "tracker/charts.html", context)



@login_required
def export(request: HttpRequest):
    if request.htmx:
        return HttpResponse( headers={'HX-Redirect': request.get_full_path()} )
    transaction_filter = TransactionFilter(
        request.GET,
        queryset=Transaction.objects.filter(user=request.user).select_related('category')
    )

    data = TransactionResource().export(transaction_filter.qs)
    response = HttpResponse(data.csv)
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    return response