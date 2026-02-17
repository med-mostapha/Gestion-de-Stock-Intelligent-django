from rest_framework import serializers
from .models import User , Category ,Product


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            phone=validated_data.get('phone'),
            password=validated_data['password']
        )
        return user

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProductSerializer(serializers.ModelSerializer):

    is_low_stock = serializers.SerializerMethodField()
    has_expiry = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'price',
            'quantity',
            'min_threshold',
            'expiration_date',
            'category',
            'is_low_stock',
            'has_expiry',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'is_low_stock', 'has_expiry']

    def get_is_low_stock(self, obj):
        return obj.is_low_stock()

    def get_has_expiry(self, obj):
        return obj.has_expiry()

    def validate_category(self, value):
        request = self.context['request']

        if value.owner != request.user:
            raise serializers.ValidationError(
                "You cannot add a product to a category you do not own."
            )

        return value
