from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Table, Category, InventoryItem, Customer, Order, OrderItem, Bill
from .serializers import (
    UserSerializer, TableSerializer, CategorySerializer,
    InventoryItemSerializer, CustomerSerializer, OrderSerializer,
    OrderItemSerializer, BillSerializer
)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

class BillViewSet(viewsets.ModelViewSet):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([AllowAny])
def hello_world(request):
    return Response({"message": "Hello from Django backend!"})
