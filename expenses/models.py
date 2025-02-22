from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.


class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=266)

    def __str__(self):
        return self.category

    class Meta:
        ordering: ['-date']


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name
    
class Budget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.FloatField()  # Budget amount
    start_date = models.DateField(default=now)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.owner.username} - {self.category.name} - {self.amount}"

class MonthlyBudget(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()  # Total monthly budget amount
    start_date = models.DateField(default=now)
    end_date = models.DateField()

    def __str__(self):
        return f"{self.owner.username} - {self.amount}"

