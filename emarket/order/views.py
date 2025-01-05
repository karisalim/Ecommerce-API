from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from .models import Order,OrderItem
from product.models import Product
from rest_framework import status
from .serializers import OrderSerializers,OrderItemSerializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    # Get the authenticated user
    user = request.user

    # Fetch the specific order for the user
    order = get_object_or_404(Order, id=pk, user=user)

    # Serialize the single order
    serializer = OrderSerializers(order, many=False)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_orders(request):
    # Get the authenticated user
    user = request.user

    # Fetch all orders for the user
    orders = Order.objects.filter(user=user).order_by('-created_at')

    # Serialize the orders
    serializer = OrderSerializers(orders, many=True)

    # Return the serialized data
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated,IsAdminUser])
def process_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk, user=user)
    order.status = request.data.get('status', order.status)  # Update only if 'status' is provided
    order.save()
    serializer = OrderSerializers(order, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request, pk):
    user = request.user
    order = get_object_or_404(Order, id=pk, user=user)
    order.delete()
    return Response({'details': "Order has been deleted!"}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_Items']

    if not order_items or len(order_items) == 0:
        return Response({'error': 'No Order received'}, status=status.HTTP_400_BAD_REQUEST)

    # حساب المجموع الكلي
    total_amount = sum(item['price'] * item['quantity'] for item in order_items)

    # إنشاء الطلب
    order = Order.objects.create(
        user=user,
        city=data['city'],
        phone_no=data['phone_no'],
        zip_code=data['zip_code'],
        country=data['country'],
        total_amount=total_amount,
    )

    # إضافة العناصر إلى الطلب
    for i in order_items:
        product = Product.objects.get(id=i['product'])
        item = OrderItem.objects.create(
            product=product,
            order=order,  # تم الإصلاح هنا
            name=product.name,
            quantity=i['quantity'],
            price=i['price'],
        )
        # تقليل المخزون
        product.stock -= item.quantity
        product.save()

    # تسلسل الطلب
    serializer = OrderSerializers(order, many=False)
    return Response(serializer.data)


















