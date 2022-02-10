from rest_framework import serializers
from .models import Wallet, WalletTransaction

class WalletSerializer(serializers.ModelSerializer):
    owned_by = serializers.CharField(source='owner')
    
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'enabled_at', 'balance']
        
    
class WalletDepositSerializer(serializers.ModelSerializer):
    deposited_by = serializers.CharField(source='wallet.owner')
    amount = serializers.IntegerField(source='wallet.balance')
    status = serializers.ReadOnlyField(default='success')
    
    class Meta:
        model = WalletTransaction
        fields = ['id', 'deposited_by', 'status', 'deposited_at', 'amount', 'reference_id']
        
        
class WalletWithdrawalSerializer(serializers.ModelSerializer):
    withdrawn_by = serializers.CharField(source='wallet.owner')
    amount = serializers.IntegerField(source='wallet.balance')
    status = serializers.ReadOnlyField(default='success')
    
    class Meta:
        model = WalletTransaction
        fields = ['id', 'withdrawn_by', 'status', 'withdrawn_at', 'amount', 'reference_id']
        
        
        
class WalletDsiabledSerializer(serializers.ModelSerializer):
    owned_by = serializers.CharField(source='owner')
    
    class Meta:
        model = Wallet
        fields = ['id', 'owned_by', 'status', 'disabled_at', 'balance']