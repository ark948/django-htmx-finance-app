import pytest
from datetime import datetime, timedelta
from django.test.client import Client
from django.urls import reverse



@pytest.mark.django_db
def test_total_values_appear_on_list_page(user_transactions, client: Client):
    user = user_transactions[0].user
    client.force_login(user)

    income_total = sum( t.amount for t in user_transactions if t.type == "income" )
    expense_total = sum( t.amount for t in user_transactions if t.type == "expense" )
    net = income_total - expense_total

    response = client.get(reverse('tracker:transactions-list'))
    assert response.context['total_income'] == income_total
    assert response.context['total_expenses'] == expense_total
    assert response.context['net_income'] == net


@pytest.mark.django_db
def test_transaction_type_filter(user_transactions, client: Client):
    user = user_transactions[0].user
    client.force_login(user)

    # income check
    GET_params = {'transaction_type': 'income'}
    resposne = client.get(reverse('tracker:transactions-list'), GET_params)

    qs = resposne.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'income'


    # expense check
    GET_params = {'transaction_type': 'expense'}
    resposne = client.get(reverse('tracker:transactions-list'), GET_params)

    qs = resposne.context['filter'].qs

    for transaction in qs:
        assert transaction.type == 'expense'


@pytest.mark.django_db
def test_transaction_start_end_date_filter(user_transactions, client: Client):
    user = user_transactions[0].user
    client.force_login(user)

    start_date_cutoff = datetime.now().date() - timedelta(days=120)
    GET_params = {'start_date': start_date_cutoff}
    resposne = client.get(reverse('tracker:transactions-list'), GET_params)

    qs = resposne.context['filter'].qs

    for transaction in qs:
        assert transaction.date >= start_date_cutoff

    end_date_cutoff = datetime.now().date() - timedelta(days=20)
    GET_params = {'end_date': end_date_cutoff}
    resposne = client.get(reverse('tracker:transactions-list'), GET_params)

    qs = resposne.context['filter'].qs

    for transaction in qs:
        assert transaction.date <= end_date_cutoff


# write a test for both start date and end date (exercise)