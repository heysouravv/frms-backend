from rest_framework import generics, permissions, status
from rest_framework.response import Response
import boto3
import csv
import uuid
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
    BranchStockSerializer,
    CustomerSerializer,
    SupplierSerializer,
    ImportJobSerializer
)
from .models import (
    CustomUser,
    Company,
    Branch,
    Product,
    BranchStock,
    ProductPriceHistory,
    Customer,
    Supplier,
    ImportJob
)
from .permissions import (
    IsSuperuser,
    IsAdmin,
    IsCashier,
    IsFinance
)
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from rest_framework.response import Response
from rest_framework import generics, permissions, status

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
        return ProductPriceHistory.objects.filter(product__company=user.company).select_related('product')

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

# views.py
class CustomerListCreateView(generics.ListCreateAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCashier]

    def get_queryset(self):
        branch = self.request.user.branch
        return Customer.objects.filter(branch=branch)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(branch=branch)

class CustomerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated, IsCashier]

    def get_queryset(self):
        branch = self.request.user.branch
        return Customer.objects.filter(branch=branch)

class SupplierListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        branch = self.request.user.branch
        return Supplier.objects.filter(branch=branch)

    def perform_create(self, serializer):
        branch = self.request.user.branch
        serializer.save(branch=branch)

class SupplierRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def get_queryset(self):
        branch = self.request.user.branch
        return Supplier.objects.filter(branch=branch)

class BulkImportView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        file_path = request.data.get('file_path')
        if not file_path:
            return Response({'error': 'File path is required.'}, status=status.HTTP_400_BAD_REQUEST)

        job_id = str(uuid.uuid4())
        import_job = ImportJob.objects.create(job_id=job_id, status='pending')

        # Run the import process in the background
        transaction.on_commit(lambda: self.perform_import(file_path, job_id))

        serializer = ImportJobSerializer(import_job)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    @staticmethod
    def perform_import(file_path, job_id):
        import_job = ImportJob.objects.get(job_id=job_id)
        import_job.status = 'processing'
        import_job.save()

        try:
            s3 = boto3.client('s3')
            bucket_name = 'your-bucket-name'  # Replace with your AWS S3 bucket name
            object_key = file_path

            csv_file = s3.get_object(Bucket=bucket_name, Key=object_key)
            csv_content = csv_file['Body'].read().decode('utf-8')

            reader = csv.DictReader(csv_content.splitlines())

            products = []
            for row in reader:
                product_data = {
                    'name': row['name'],
                    'description': row['description'],
                    'price': row['price'],
                    # Add more fields as per your Product model
                }
                product_serializer = ProductSerializer(data=product_data)
                if product_serializer.is_valid():
                    products.append(product_serializer.save())
                else:
                    import_job.status = 'failed'
                    import_job.error_message = str(product_serializer.errors)
                    import_job.save()
                    return

            Product.objects.bulk_create(products)

            import_job.status = 'completed'
            import_job.save()
        except Exception as e:
            import_job.status = 'failed'
            import_job.error_message = str(e)
            import_job.save()

class ImportJobStatusView(generics.RetrieveAPIView):
    queryset = ImportJob.objects.all()
    serializer_class = ImportJobSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    lookup_field = 'job_id'
