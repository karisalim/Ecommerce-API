# from rest_framework import serializers
# from .models import Order,OrderItem
#
# class OrderSerializers(serializers.ModelSerializer):
#     orderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)
#     class Meta:
#         model = Order
#         fields = '__all__'
#
# def get_order_items(self,obj):
#     order_items = obj.orderitems.all()
#     serializer = OrderSerializers(order_items,many=True)
#     return serializer.data
#
#
#
# class OrderItemSerializers(serializers.ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = '__all__'

from rest_framework import serializers
from .models import Order, OrderItem

class OrderSerializers(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(method_name="get_order_items", read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_order_items(self, obj):  # تعديل: تم نقل الطريقة داخل الكلاس
        order_items = obj.orderitems.all()
        serializer = OrderItemSerializers(order_items, many=True)
        return serializer.data

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
