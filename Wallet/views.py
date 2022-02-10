from datetime import datetime
from rest_framework.viewsets import GenericViewSet
from django.core.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed

from Wallet.serializers import WalletDepositSerializer, WalletDsiabledSerializer, WalletWithdrawalSerializer
from .models import Wallet, WalletTransaction
from .serializers import WalletSerializer
from rest_framework.mixins import UpdateModelMixin


# Create your views here.
class WalletInitViewSet(GenericViewSet):
    
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    
    def create(self, request):
        customer_xid = request.data.get('customer_xid', None)
        wallet = Wallet(owner=customer_xid)
        
        wallet.save()
        
        return Response({
            "data" : {
                "token" : wallet.token
            },
            "status" : "success"
        }, status=status.HTTP_201_CREATED)
        
class WalletViewset(UpdateModelMixin,
                    GenericViewSet):
    def create(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', 'Token x')
        token = auth.split()[1]
        wallet = Wallet.objects.get(token=token)
        
        if wallet.status == 1:
            raise ValidationError("Wallet has been initialized!")
        
        wallet.status = 1
        wallet.enabled_at = datetime.now()
        wallet.save()
        
        serialized = WalletSerializer(wallet)
        
        return Response({
            "status" : "success",
            "data" : {
                "wallet" : serialized.data
            }
        }, status=status.HTTP_201_CREATED)
        
        
    def list(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', 'Token x')
        token = auth.split()[1]
        
        wallet = Wallet.objects.get(token=token)
        
        if wallet.status == 0:
            raise ValidationError("Wallet is disabled")
        
        serialized = WalletSerializer(wallet)
        
        return Response({
            "status" : "success",
            "data" : {
                "wallet" : serialized.data
            }
        }, status=status.HTTP_200_OK)
        
        
    @action(methods=['POST'], detail=False)
    def deposits(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', 'Token x')
        token = auth.split()[1]
        amount = request.data.get('amount', None)
        reference_id = request.data.get('reference_id', None)
        
                
        wallet = Wallet.objects.get(token=token)
        if wallet.status == 0:
            raise ValidationError("Wallet is disabled")
        
        transaction = WalletTransaction.objects.filter(reference_id=reference_id)
        
        if not transaction:
            wallet.balance += int(amount)
            wallet.save()
            transaction = WalletTransaction(wallet=wallet, reference_id=reference_id, deposited_at=datetime.now(), amount=amount)
            transaction.save()
            
            
            serializer = WalletDepositSerializer(transaction)
            
            return Response({
                "status" : "success",
                "data" : {
                    "deposit" : serializer.data
                }
            }, status=status.HTTP_201_CREATED)
            
            
        else:
            raise ValidationError("Duplicate reference id detected!")
        
        
    
    @action(methods=['POST'], detail=False)
    def withdrawals(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', 'Token x')
        token = auth.split()[1]
        amount = request.data.get('amount', None)
        reference_id = request.data.get('reference_id', None)
        
                
        wallet = Wallet.objects.get(token=token)
        if wallet.status == 0:
            raise ValidationError("Wallet is disabled")
        
        transaction = WalletTransaction.objects.filter(reference_id=reference_id)
        
        if not transaction:
            
            if wallet.balance - int(amount) < 0:
                raise ValidationError("Amount must be smaller than current balance!")
            
            wallet.balance -= int(amount)
            wallet.save()
            transaction = WalletTransaction(wallet=wallet, reference_id=reference_id, withdrawn_at=datetime.now(), amount=amount)
            transaction.save()
            
            
            serializer = WalletWithdrawalSerializer(transaction)
            
            return Response({
                "status" : "success",
                "data" : {
                    "withdrawal" : serializer.data
                }
            }, status=status.HTTP_201_CREATED)
            
            
        else:
            raise ValidationError("Duplicate reference id detected!")
        
        
    def update(self, *args, **kwargs):
        raise MethodNotAllowed("POST", detail="Use PATCH")

    def partial_update(self, request):
        auth = request.META.get('HTTP_AUTHORIZATION', 'Token x')
        token = auth.split()[1]
        is_disabled = request.data.get('is_disabled')
        if is_disabled:
            wallet = Wallet.objects.get(token=token)
            
            wallet.status = 0
            wallet.disabled_at = datetime.now()
            wallet.save()
            
            serializer = WalletDsiabledSerializer(wallet)
            
            return Response({
                "status" : "success",
                "data" : {
                    "wallet" : serializer.data
                }
            })