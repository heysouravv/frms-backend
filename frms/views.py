from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt import serializers
from .serializers import (
    BranchStockSerializer,
    UserRegistrationSerializer,
    CompanySerializer,
    BranchSerializer,
    UserLoginSerializer,
    UserTreeSerializer,
    ProductSerializer,
    ProductPriceHistorySerializer,
    BranchStockSerializer
)
from .models import (
    CustomUser,
    Company,
    Branch,
    Product,
    BranchStock,
    ProductPriceHistory
)
from .permissions import (
    IsSuperuser,
    IsAdmin,
    IsCashier,
    IsFinance
)
from rest_framework.permissions import IsAuthenticated

class CompanyCreateView(generics.CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsSuperuser]

class BranchCreateView(generics.CreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsSuperuser]

    def perform_create(self, serializer):
        company_id = self.request.data.get('company')
        if company_id:
            company = Company.objects.get(id=company_id)
            serializer.save(company=company)
        else:
            raise serializers.ValidationError("Company ID is required.")

class AdminUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsSuperuser]

    def perform_create(self, serializer):
        company = self.request.data.get('company')
        branch = self.request.data.get('branch')
        serializer.save(company_id=company, branch_id=branch)

class FinanceCashierUserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdmin]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(company=user.company, branch=user.branch)

class UserLoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = TokenObtainPairSerializer.get_token(user)
        access_token = refresh.access_token

        response_data = {
            'refresh': str(refresh),
            'access': str(access_token),
        }
        return Response(response_data, status=status.HTTP_200_OK)

class UserTreeView(generics.ListAPIView):
    serializer_class = UserTreeSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_queryset(self):
        user = self.request.user
        company = user.company
        return CustomUser.objects.filter(company=company)


class ProductListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsCashier]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(company=user.company)

    def perform_create(self, serializer):
        user = self.request.user
        product = serializer.save(company=user.company)
        BranchStock.objects.create(branch=user.branch, product=product, quantity=product.quantity)

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsCashier]

    def get_queryset(self):
        user = self.request.user
        return Product.objects.filter(company=user.company)

    def perform_update(self, serializer):
        old_price = self.get_object().price
        new_price = serializer.validated_data.get('price', old_price)

        if old_price != new_price:
            ProductPriceHistory.objects.create(
                product=self.get_object(),
                price=new_price
            )

        serializer.save()

class ProductPriceHistoryListCreateView(generics.ListCreateAPIView):
    serializer_class = ProductPriceHistorySerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsFinance]

    def get_queryset(self):
        user = self.request.user
        return ProductPriceHistory.objects.filter(product__company=user.company)

class BranchStockListCreateView(generics.ListCreateAPIView):
    serializer_class = BranchStockSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsCashier]

    def get_queryset(self):
        user = self.request.user
        queryset = BranchStock.objects.filter(branch__company=user.company)
        branch_id = self.request.query_params.get('branch')
        if branch_id:
            queryset = queryset.filter(branch_id=branch_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(branch=user.branch)

class BranchStockRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BranchStockSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin | IsCashier]

    def get_queryset(self):
        user = self.request.user
        return BranchStock.objects.filter(branch__company=user.company)
