from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.response import Response
from .models import Product
from rest_framework import status
from .serializers import ProductSerializers
from .filtters import ProductFilter
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg
from .models import Product, Review  # Import both Product and Review models


@api_view(['GET'])
def get_all_products(request):
    filterset = ProductFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    resPage = 2
    paginator = PageNumberPagination()
    paginator.page_size = resPage
    queryset = paginator.paginate_queryset(filterset.qs, request)
    serializer = ProductSerializers(queryset, many=True)
    return Response({"products": serializer.data, "per_page": resPage, "count": count})

@api_view(['GET'])
def get_by_id_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerializers(product)
    return Response({"product": serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated,IsAdminUser])
def new_product(request):
    serializer = ProductSerializers(data=request.data)
    if serializer.is_valid():
        product = serializer.save(user=request.user)
        res = ProductSerializers(product)
        return Response({"product": res.data})
    else:
        return Response(serializer.errors)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated,IsAdminUser])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    # Check if the product belongs to the authenticated user
    if product.user != request.user:
        return Response(
            {"error": "Sorry, you cannot update this product."},
            status=status.HTTP_403_FORBIDDEN
        )

    # Handle the update for the fields

    product.name = request.data['name']
    product.description = request.data['description']
    product.price = request.data['price']
    product.brand = request.data['brand']
    product.category = request.data['category']
    product.rating = request.data['rating']
    product.stock = request.data['stock']

    # Validate and save the updated product
    serializer = ProductSerializers(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"product": serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)







@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    # تحقق من أن المنتج يخص المستخدم المصادق عليه
    if product.user != request.user:
        return Response(
            {"error": "Sorry, you cannot delete this product."},
            status=status.HTTP_403_FORBIDDEN
        )

    # حذف المنتج
    product.delete()
    # إعادة استجابة بنجاح الحذف
    return Response({"message": "Product deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request, pk):
    product = get_object_or_404(Product, id=pk)
    user = request.user
    data = request.data
    review = product.reviews.filter(user=user)

    # Check if the rating is between 1 and 5
    if data['rating'] <= 0 or data['rating'] > 6:
        return Response({"error": 'Please select a rating between 1 to 6 only.'},
                        status=status.HTTP_400_BAD_REQUEST)

    # If the user has already reviewed this product, update the existing review
    elif review.exists():
        new_review = {'ratings': data['rating'], 'comment': data['comment']}
        review.update(**new_review)

        # Update the product's average rating
        rating = product.reviews.aggregate(avg_rating=Avg('ratings'))
        product.rating = rating['avg_rating']
        product.save()

        return Response({'details': 'Product review updated'})

    # If the user hasn't reviewed the product yet, create a new review
    else:
        Review.objects.create(
            user=user,
            product=product,
            ratings=data['rating'],  # Corrected to use 'ratings'
            comment=data['comment']
        )
        # Update the product's average rating
        rating = product.reviews.aggregate(avg_rating=Avg('ratings'))
        product.rating = rating['avg_rating',3]
        product.save()

        return Response({'details': 'Product review created'})


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsAdminUser])
def delete_review(request, pk):
    user = request.user
    product = get_object_or_404(Product, id=pk)

    # Find the user's review for the product
    review = product.reviews.filter(user=user)

    if review.exists():
        # Delete the review
        review.delete()

        # Recalculate and update the product's average rating
        rating = product.reviews.aggregate(avg_rating=Avg('ratings'))
        if rating['avg_rating'] is None:
            product.rating = 0
        else:
            product.rating = round(rating['avg_rating'], 1)
        product.save()

        return Response({'details': 'Product review deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({'error': 'Review not found for this user.'}, status=status.HTTP_404_NOT_FOUND)















#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # products = Product.objects.all()
    # serializer = ProductSerializers(products,many=True)
    # print(products)




