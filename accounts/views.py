from django.utils import timezone
from django.db import models
from django.db.models import Sum, F, Case, When, BooleanField, DecimalField
from django.contrib.auth import authenticate

from rest_framework import generics, status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import UserRegisterSerializer, ProductSerializer, CategorySerializer
from .models import User, Category, Product

# --- PAGINATION CONFIG ---
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

# --- USER AUTH ---
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
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

# --- CATEGORY VIEWS ---
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
    
# --- PRODUCT VIEWS (With Search, Filter & Pagination) ---
class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    
    # Enable Filtering, Search, and Ordering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name']
    ordering_fields = ['price', 'quantity', 'created_at']

    def get_queryset(self):
        today = timezone.now().date()
        return Product.objects.select_related('category').filter(
            category__owner=self.request.user
        ).annotate(
            is_low_stock=Case(
                When(quantity__lte=F('min_threshold'), then=True),
                default=False, output_field=BooleanField(),
            ),
            has_expiry=Case(
                When(expiration_date__lte=today, then=True),
                default=False, output_field=BooleanField(),
            )
        ).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save()

    def get_serializer_context(self):
        return {'request': self.request}

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        today = timezone.now().date()
        return Product.objects.select_related('category').filter(
            category__owner=self.request.user
        ).annotate(
            is_low_stock=Case(
                When(quantity__lte=F('min_threshold'), then=True),
                default=False, output_field=BooleanField(),
            ),
            has_expiry=Case(
                When(expiration_date__lte=today, then=True),
                default=False, output_field=BooleanField(),
            )
        )

# --- ALERTS VIEW ---
class ProductAlertView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        today = timezone.now().date()
        base_qs = Product.objects.select_related('category').filter(
            category__owner=request.user
        ).annotate(
            is_low_stock=Case(When(quantity__lte=F('min_threshold'), then=True), default=False, output_field=BooleanField()),
            has_expiry=Case(When(expiration_date__lte=today, then=True), default=False, output_field=BooleanField())
        )
        return Response({
            "low_stock": ProductSerializer(base_qs.filter(is_low_stock=True), many=True, context={'request': request}).data,
            "expired": ProductSerializer(base_qs.filter(has_expiry=True), many=True, context={'request': request}).data,
        })

# --- DASHBOARD VIEW ---
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        today = timezone.now().date()
        products = Product.objects.filter(category__owner=user)
        categories = Category.objects.filter(owner=user)

        stats = products.aggregate(
            total_products=models.Count('id'),
            total_stock=Sum('quantity'),
            low_stock_count=Sum(Case(When(quantity__lte=F('min_threshold'), then=1), default=0, output_field=models.IntegerField())),
            expired_count=Sum(Case(When(expiration_date__lte=today, then=1), default=0, output_field=models.IntegerField())),
            total_value=Sum(F('price') * F('quantity'), output_field=DecimalField(max_digits=15, decimal_places=2))
        )

        expired_value = products.filter(expiration_date__lte=today).aggregate(
            val=Sum(F('price') * F('quantity'), output_field=DecimalField(max_digits=15, decimal_places=2))
        )['val'] or 0

        value_by_category = (
            products.values('category__name')
            .annotate(total_value=Sum(F('price') * F('quantity')))
            .order_by('-total_value')
        )

        return Response({
            "counts": {
                "total_products": stats['total_products'] or 0,
                "total_categories": categories.count(),
                "low_stock": stats['low_stock_count'] or 0,
                "expired_products": stats['expired_count'] or 0
            },
            "stock": {"total_stock": stats['total_stock'] or 0},
            "financial": {
                "total_inventory_value": float(stats['total_value'] or 0),
                "expired_inventory_value": float(expired_value),
                "real_inventory_value": float((stats['total_value'] or 0) - expired_value)
            },
            "analytics": [
                {"category": item['category__name'], "total_value": float(item['total_value'] or 0)}
                for item in value_by_category
            ]
        })