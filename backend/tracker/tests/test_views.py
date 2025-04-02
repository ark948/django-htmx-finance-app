import pytest
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