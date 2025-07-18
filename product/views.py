from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Product,Review
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .filters import ProductsFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.db.models import Avg
from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
@swagger_auto_schema(tags=["Products"])
def get_all_products(request):
    filterset = ProductsFilter(request.GET, queryset=Product.objects.all().order_by('id'))
    count = filterset.qs.count()
    queryset = filterset.qs  
    serializer = ProductSerializer(queryset, many=True)
    return Response({"products": serializer.data, "count": count})


@api_view(['GET'])
@swagger_auto_schema(tags=["Products"])
def get_by_id_product(request,pk):
    products = get_object_or_404(Product,id=pk)
    serializer = ProductSerializer(products,many=False)
    print(products)
    return Response({"product":serializer.data})

@api_view(['POST'])
@swagger_auto_schema(tags=["Products"])
@permission_classes([IsAuthenticated, IsAdminUser])
def new_product(request):
    serializer = ProductSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response({"product": serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@swagger_auto_schema(tags=["Products"])
@permission_classes([IsAuthenticated, IsAdminUser])
def update_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user and not request.user.is_superuser:
        return Response({"error": "Sorry, you can't update"}, status=status.HTTP_403_FORBIDDEN)

    serializer = ProductSerializer(product, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response({"product": serializer.data})
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def delete_product(request, pk):
    product = get_object_or_404(Product, id=pk)

    if product.user != request.user and not request.user.is_superuser:
        return Response({"error": "Sorry, you can't delete"}, status=status.HTTP_403_FORBIDDEN)

    product.delete()
    return Response({"details": "Done"}, status=status.HTTP_200_OK)
  
# Reviews 
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
    data = request.data
    review = product.reviews.filter(user=user)
    
    if data['rating'] <= 0 or data['rating'] > 5:
        return Response({"Please select between 1 and 5 "},
                        status=status.HTTP_400_BAD_REQUEST)
    elif review.exists():
        new_review = {'rating':data['rating'], 'comment':data['comment']}
        review.update(**new_review)
    
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()

        return Response({'details':'Product review updated'})
    else:
        Review.objects.create(
            user=user,
            product=product,
            rating= data['rating'],
            comment= data['comment']
        )
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        product.ratings = rating['avg_ratings']
        product.save()
        return Response({'details':'Product review created'})
    

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_review(request,pk):
    user = request.user
    product = get_object_or_404(Product,id=pk)
   
    review = product.reviews.filter(user=user)
   
 
    if review.exists():
        review.delete()
        rating = product.reviews.aggregate(avg_ratings = Avg('rating'))
        if rating['avg_ratings'] is None:
            rating['avg_ratings'] = 0
            product.ratings = rating['avg_ratings']
            product.save()
            return Response({'details':'Product review deleted'})
    else:
        return Response({'error':'Review not found'},status=status.HTTP_404_NOT_FOUND)
