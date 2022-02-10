from django.urls import include, path

from .custom_router import CustomRouter
from .views import WalletInitViewSet, WalletViewset


router = CustomRouter()
router.register('init', WalletInitViewSet, basename='WalletInit')
router.register('wallet', WalletViewset, basename='Wallet')

urlpatterns = [
    path('', include(router.urls)),
]