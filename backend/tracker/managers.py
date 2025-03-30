from decimal import Decimal
from django.db import models



class TransactionQuerySet(models.QuerySet):
    def get_expenses(self) -> models.QuerySet:
        return self.filter(type='expense')
    
    def get_income(self) -> models.QuerySet:
        return self.filter(type='income')
    
    def get_total_expenses(self) -> Decimal | int:
        return self.get_expenses().aggregate( total=models.Sum('amount') )['total'] or 0

    def get_total_income(self) -> Decimal | int:
        return self.get_income().aggregate( total=models.Sum('amount') )['total'] or 0