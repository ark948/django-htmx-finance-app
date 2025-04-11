import plotly.express as px
from django.db.models import QuerySet, Sum


def plot_income_expenses_bar_chart(qs):
    x_vals = ['Income', 'Expenditure']

    # sum up the total income and expenditure
    total_income = qs.filter(type='income').aggregate(
        total=Sum('amount')
    )['total']
    total_expenses = qs.filter(type='expense').aggregate(
        total=Sum('amount')
    )['total']

    fig = px.bar(x=x_vals, y=[total_income, total_expenses])

    return fig