from rest_framework import serializers
from .models import Table, Category, InventoryItem, Customer, Order, OrderItem, Bill, DailyExpense, DailyTracker, Expense, Income, Employee, Role, SalaryRecord

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class SalaryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalaryRecord
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = '__all__'
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryField(serializers.SlugRelatedField):
    def to_internal_value(self, data):
        if not data:
            return None
        if isinstance(data, int) or (isinstance(data, str) and str(data).isdigit()):
            try:
                return Category.objects.get(pk=int(data))
            except Category.DoesNotExist:
                pass
        category, _ = Category.objects.get_or_create(name=str(data).strip())
        return category

class InventoryItemSerializer(serializers.ModelSerializer):
    category = CategoryField(slug_field='name', queryset=Category.objects.all(), required=False, allow_null=True)
    category_name = serializers.ReadOnlyField(source='category.name')

    class Meta:
        model = InventoryItem
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'

class OrderItemSerializer(serializers.ModelSerializer):
    item_name = serializers.ReadOnlyField(source='item.name')

    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'item', 'item_name', 'quantity', 'price']
        read_only_fields = ['id', 'item_name', 'price']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.ReadOnlyField(source='table.number')
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Order
        fields = '__all__'

class BillSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(source='order.items', many=True, read_only=True)

    class Meta:
        model = Bill
        fields = '__all__'

class DailyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyExpense
        fields = '__all__'
        read_only_fields = ['total']

class DailyTrackerSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyTracker
        fields = '__all__'
