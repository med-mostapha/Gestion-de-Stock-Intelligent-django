from django.utils import timezone
from rest_framework import generics
from django.db import models
from django.db.models import F
from django.db.models import Sum

from .serializers import UserRegisterSerializer,ProductSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import CategorySerializer
from rest_framework.permissions import IsAuthenticated
from .models import User,Category,Product

# User
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # _ => true if first login and false if not and have old token
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            "token": token.key
        })

# Category
class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
    
# Product
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(category__owner=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(category__owner=self.request.user)

    def get_serializer_context(self):
        return {'request': self.request}

# Products alert (list men le products li 3ado var9in)
class ProductAlertView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        products = Product.objects.filter(category__owner=user)

        low_stock = products.filter(quantity__lte=models.F('min_threshold'))

        expired = products.filter(
            expiration_date__isnull=False,
            expiration_date__lte=timezone.now().date()
        )

        serializer = ProductSerializer

        return Response({
            "low_stock": serializer(low_stock, many=True, context={'request': request}).data,
            "expired": serializer(expired, many=True, context={'request': request}).data,
        })

# Dashboard analytics
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = timezone.now().date()

        products = Product.objects.filter(category__owner=user)
        categories = Category.objects.filter(owner=user)

        low_stock_count = products.filter(
            quantity__lte=F('min_threshold')
        ).count()

        expired_count = products.filter(
            expiration_date__isnull=False,
            expiration_date__lte=today
        ).count()

        total_stock = products.aggregate(
            total=Sum('quantity')
        )['total'] or 0


        data = {
            "counts": {
                "total_products": products.count(),
                "total_categories": categories.count(),
                "low_stock": low_stock_count,
                "expired_products": expired_count
            },
            "stock": {
                "total_stock": total_stock
            }
        }

        return Response(data)
