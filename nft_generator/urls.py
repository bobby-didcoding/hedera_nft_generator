
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
    path('nft-generator/<str:id>/', views.NFTGeneratorView.as_view(), name="nft-generator"),
    path('nft-from-artwork-generator/<str:id>/', views.NFTFromArtworkGeneratorView.as_view(), name="nft-from-artwork-generator"),
    path('nfts/', views.NFTSView.as_view(), name="nfts"),
    path('nft/<str:id>/', views.NFTView.as_view(), name='nft'),
    path('token/', views.TokenView.as_view(), name="token"),
    path('tokens/', views.TokensView.as_view(), name="tokens"),
    path('minting/<str:id>/', views.MintView.as_view(), name="minting"),
    path('associate/<str:id>/', views.AssociateView.as_view(), name="associate"),
    path('transfer/<str:id>/', views.TransferView.as_view(), name="transfer"),
    path('accounts/', views.AccountsView.as_view(), name="accounts"),
    path('account/<str:id>/', views.AccountView.as_view(), name="account"),
    path('send-to-ipfs/<str:id>/', views.send_to_ipfs, name="send-to-ipfs"),
    path('create-from-traits/<str:id>/', views.create_from_traits, name="create_from_traits"),
    ]
 
