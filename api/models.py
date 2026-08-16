from django.db import models
from django.contrib.auth.models import User

class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
    ]
    number = models.IntegerField(unique=True)
    capacity = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return f"Table {self.number}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Customer(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    table = models.ForeignKey(Table, on_delete=models.SET_NULL, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def update_total(self):
        total = sum(item.quantity * item.price for item in self.items.all())
        self.total_amount = total
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(InventoryItem, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True) # Auto-set from item

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.item.price
        super().save(*args, **kwargs)
        self.order.update_total()

    def delete(self, *args, **kwargs):
        order = self.order
        super().delete(*args, **kwargs)
        order.update_total()

    def __str__(self):
        return f"{self.quantity}x {self.item.name} for Order #{self.order.id}"

class Bill(models.Model):
    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
    ]
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='cash')
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for Order #{self.order.id}"

class DailyExpense(models.Model):
    date = models.DateField(unique=True)
    rent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kalikattan = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    chicken = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    kuboos = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    gas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mandi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pepsi = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    purchase = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    extra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mutton = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    fish = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    vegetable = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    grocery = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dairy = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    eb_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    other = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def save(self, *args, **kwargs):
        self.total = sum([
            self.rent or 0, self.salary or 0, self.kalikattan or 0, self.chicken or 0, 
            self.kuboos or 0, self.gas or 0, self.mandi or 0, self.pepsi or 0, 
            self.purchase or 0, self.bill or 0, self.extra or 0,
            self.mutton or 0, self.fish or 0, self.vegetable or 0, self.grocery or 0,
            self.dairy or 0, self.eb_bill or 0, self.other or 0
        ])
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Daily Expense - {self.date}"

class DailyTracker(models.Model):
    date = models.DateField(unique=True)
    total_sale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    swiggy = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_expense = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"Daily Tracker - {self.date}"

class Expense(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

class Income(models.Model):
    title = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

class Employee(models.Model):
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, default='Staff')
    phone = models.CharField(max_length=20, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    daily_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=20, default='Active')
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.role})"

class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class SalaryRecord(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_payouts', null=True, blank=True)
    employee_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=50, default='Monthly')
    payment_mode = models.CharField(max_length=50, default='Cash')
    date = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee_name} - ₹{self.amount} ({self.date})"
