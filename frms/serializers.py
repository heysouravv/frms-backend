from rest_framework import serializers
from .models import (
    CustomUser,
    Company,
    Branch,
    Product,
    ProductPriceHistory,
    BranchStock,
    Sale,
    Customer,
    Supplier,
    ImportJob
)
from django.contrib.auth import authenticate


class BranchStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = BranchStock
        fields = ['id', 'branch', 'product', 'quantity']


class BranchSerializer(serializers.ModelSerializer):
    cashiers = serializers.SerializerMethodField()
    finance_users = serializers.SerializerMethodField()

    class Meta:
        model = Branch
        fields = ['id', 'name', 'cashiers', 'finance_users']

    def get_cashiers(self, obj):
        cashiers = CustomUser.objects.filter(branch=obj, role='cashier')
        return CashierFinanceSerializer(cashiers, many=True).data

    def get_finance_users(self, obj):
        finance_users = CustomUser.objects.filter(branch=obj, role='finance')
        return CashierFinanceSerializer(finance_users, many=True).data

class ProductSerializer(serializers.ModelSerializer):
    branches = BranchSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']

class ProductPriceHistorySerializer(serializers.ModelSerializer):
    old_price = serializers.SerializerMethodField()
    new_price = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()
    product_details = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = ProductPriceHistory
        fields = ['old_price', 'new_price', 'effective_date', 'updated_at', 'product_details']

    def get_old_price(self, obj):
        return obj.product.price

    def get_new_price(self, obj):
        return obj.price

    def get_updated_at(self, obj):
        return obj.product.updated_at

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), required=False)
    branch = serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all(), required=False)
    role = serializers.ChoiceField(choices=CustomUser.USER_ROLES)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'role', 'company', 'branch')

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            company=validated_data.get('company'),
            branch=validated_data.get('branch')
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if user:
                data['user'] = user
            else:
                raise serializers.ValidationError('Invalid username or password.')
        else:
            raise serializers.ValidationError('Must include username and password.')

        return data

class CashierFinanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class UserTreeSerializer(serializers.ModelSerializer):
    admin = serializers.SerializerMethodField()
    branches = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role', 'admin', 'branches']

    def get_admin(self, obj):
        admin = CustomUser.objects.filter(company=obj.company, role='admin').first()
        if admin:
            return {
                'id': admin.id,
                'username': admin.username,
                'email': admin.email
            }
        return None

    def get_branches(self, obj):
        branches = Branch.objects.filter(company=obj.company)
        return BranchSerializer(branches, many=True).data

class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sale
        fields = ['id', 'product', 'quantity', 'price', 'customer', 'branch', 'sale_date']
        read_only_fields = ['branch', 'sale_date']

# serializers.py
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'email', 'phone', 'address', 'branch']
        read_only_fields = ['branch']

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address', 'branch']
        read_only_fields = ['branch']

class ImportJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportJob
        fields = ['job_id', 'status', 'error_message', 'created_at', 'updated_at']
