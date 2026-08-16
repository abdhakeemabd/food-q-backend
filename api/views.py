from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.conf import settings
from .models import Table, Category, InventoryItem, Customer, Order, OrderItem, Bill, DailyExpense, DailyTracker, Expense, Income, Employee, Role, SalaryRecord
from .serializers import (
    UserSerializer, TableSerializer, CategorySerializer,
    InventoryItemSerializer, CustomerSerializer, OrderSerializer,
    OrderItemSerializer, BillSerializer, DailyExpenseSerializer, DailyTrackerSerializer,
    ExpenseSerializer, IncomeSerializer, EmployeeSerializer, RoleSerializer, SalaryRecordSerializer
)

BasePermission = AllowAny

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [BasePermission]

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [BasePermission]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [BasePermission]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [BasePermission]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [BasePermission]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [BasePermission]

    @action(detail=True, methods=['post'])
    def checkout(self, request, pk=None):
        order = self.get_object()
        
        if order.status == 'completed':
            return Response({'error': 'Order is already completed'}, status=status.HTTP_400_BAD_REQUEST)
            
        if not order.items.exists():
            return Response({'error': 'Cannot checkout an empty order'}, status=status.HTTP_400_BAD_REQUEST)

        payment_method = request.data.get('payment_method', 'cash')
        
        # Create the bill
        bill, created = Bill.objects.get_or_create(
            order=order,
            defaults={
                'payment_method': payment_method,
                'amount_paid': order.total_amount
            }
        )
        
        # Update order status
        order.status = 'completed'
        order.save()
        
        # Free up the table if one is assigned
        if order.table:
            order.table.status = 'available'
            order.table.save()
            
        return Response({
            'message': 'Order checked out successfully',
            'bill_id': bill.id
        })

class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [BasePermission]

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [BasePermission]

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Normalize payment_method (e.g. 'Cash' -> 'cash', 'UPI' -> 'upi', 'Card' -> 'card')
        pm = str(data.get('payment_method') or data.get('paymentMethod') or 'cash').lower()
        if pm not in ['cash', 'card', 'upi']:
            pm = 'cash'
        data['payment_method'] = pm

        # Map totalAmount / amount_paid
        amount = data.get('amount_paid') or data.get('totalAmount') or data.get('total') or 0
        data['amount_paid'] = amount

        # Handle order association
        order_id = data.get('order') or data.get('order_id')
        
        if not order_id:
            # If converting KOT/Cart to Bill directly without existing DRF order ID
            table_id = data.get('tableId') or data.get('table_id') or data.get('table')
            table = None
            if table_id:
                try:
                    table = Table.objects.get(pk=int(table_id))
                    table.status = 'available'
                    table.save()
                except (Table.DoesNotExist, ValueError, TypeError):
                    table = None
                    
            order = Order.objects.create(
                table=table,
                total_amount=amount,
                status='completed'
            )
            
            # Create OrderItems if items array passed
            items = data.get('items', [])
            if isinstance(items, list):
                for item_data in items:
                    item_id = item_data.get('id') or item_data.get('item_id')
                    qty = item_data.get('qty') or item_data.get('quantity') or 1
                    price = item_data.get('price') or 0
                    if item_id:
                        try:
                            inv_item = InventoryItem.objects.get(pk=int(item_id))
                            OrderItem.objects.create(
                                order=order,
                                item=inv_item,
                                quantity=qty,
                                price=price
                            )
                        except (InventoryItem.DoesNotExist, ValueError, TypeError):
                            pass

            data['order'] = order.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    return Response({"message": "Hello from Django backend!"})

class DailyExpenseViewSet(viewsets.ModelViewSet):
    queryset = DailyExpense.objects.all()
    serializer_class = DailyExpenseSerializer
    permission_classes = [BasePermission]

class DailyTrackerViewSet(viewsets.ModelViewSet):
    queryset = DailyTracker.objects.all()
    serializer_class = DailyTrackerSerializer
    permission_classes = [BasePermission]

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [BasePermission]

class IncomeViewSet(viewsets.ModelViewSet):
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer
    permission_classes = [BasePermission]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [BasePermission]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [BasePermission]

class SalaryRecordViewSet(viewsets.ModelViewSet):
    queryset = SalaryRecord.objects.all()
    serializer_class = SalaryRecordSerializer
    permission_classes = [BasePermission]
