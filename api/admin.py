from django.contrib import admin
from .models import Table, Category, InventoryItem, Customer, Order, OrderItem, Bill, DailyExpense, DailyTracker, Expense, Income, Employee, Role, SalaryRecord

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(SalaryRecord)
class SalaryRecordAdmin(admin.ModelAdmin):
    list_display = ('employee_name', 'amount', 'payment_type', 'payment_mode', 'date')
    list_filter = ('payment_type', 'payment_mode', 'date')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'phone', 'salary', 'status')
    list_filter = ('role', 'status')

@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date')
    list_filter = ('category', 'date')

@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'category', 'date')
    list_filter = ('category', 'date')

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'status')
    list_filter = ('status',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'is_available')
    list_filter = ('is_available', 'category')
    search_fields = ('name',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email')
    search_fields = ('name', 'phone')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'customer', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'quantity', 'price')

@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment_method', 'amount_paid', 'created_at')
    list_filter = ('payment_method',)

@admin.register(DailyExpense)
class DailyExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'total')
    list_filter = ('date',)
    
@admin.register(DailyTracker)
class DailyTrackerAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_sale', 'swiggy', 'total_expense', 'cash_balance')
    list_filter = ('date',)
