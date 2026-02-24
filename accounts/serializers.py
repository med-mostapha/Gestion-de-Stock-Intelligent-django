# serializers.py
from rest_framework import serializers
from .models import User, Category, Product

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password']
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    # These will be populated by the View's annotation
    is_low_stock = serializers.BooleanField(read_only=True)
    has_expiry = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'quantity', 'min_threshold',
            'expiration_date', 'category', 'is_low_stock',
            'has_expiry', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


    def validate_category(self, value):
        # Ensure 'request' exists in context
        request = self.context.get('request')
        if not request:
            return value

        # Critical Security Check: Does the user own the category they are assigning?
        if value.owner != request.user:
            raise serializers.ValidationError(
                "Access Denied: You cannot assign products to a category you do not own."
            )
        return value