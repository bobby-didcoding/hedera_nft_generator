
# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.urls import path

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from . import views
 
app_name = "nft_generator"
 
urlpatterns = [
    path('', views.HomeView.as_view(), name="home"),
    path('nft-generator/<str:name>/', views.NFTGeneratorView.as_view(), name="nft-generator"),
    path('nfts/', views.NFTSView.as_view(), name="nfts"),
    path('nft/<slug:slug>/', views.NFTView.as_view(), name='nft'),
    path('token/', views.TokenView.as_view(), name="token"),
    path('tokens/', views.TokensView.as_view(), name="tokens"),
    path('minting/<str:name>/', views.MintView.as_view(), name="minting"),
    path('associate/<str:name>/', views.AssociateView.as_view(), name="associate"),
    path('transfer/<slug:slug>/', views.TransferView.as_view(), name="transfer"),
    path('accounts/', views.AccountsView.as_view(), name="accounts"),
    path('account/<str:account_id>/', views.AccountView.as_view(), name="account"),
    ]
 
