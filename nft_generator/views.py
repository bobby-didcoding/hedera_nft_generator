# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.views import generic
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.decorators import method_decorator

from apis.hedera.utils import AccountManager

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .models import NoneFungibleToken, Token, Account
from .tasks import create_nft, mint_nft, associate_account, transfer_nft, create_ipfs_cid,create_new_from_traits,create_nft_from_artwork
from .forms import NFTForm, TokenForm, MintingForm,AssociateForm, TransferForm
from .decorators import redirect_if_no_token


class HomeView(generic.TemplateView):
    """
    TemplateView used for our home page.

    **Template:**

    :template:`nft_generator/index.html`
    """
    template_name = "nft_generator/index.html"
    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class NFTGeneratorView(generic.FormView):
    """
    FormView to create NFT artwork.

    An instance of :form:`NFTForm`.

    **Template:**

    :template:`nft_generator/nft_generator.html`
    """
    form_class = NFTForm
    template_name = "nft_generator/nft_generator.html"
    success_url = '/nfts'
    
    def form_valid(self, form):
        quantity = form.cleaned_data.get('quantity')
        
        token = Token.objects.get(id =self.kwargs['id'])
        if quantity > token.get_remaining_supply:
            messages.error(self.request, f"You have {token.get_remaining_supply} remaining supply")
        else:
            messages.success(self.request, f"You have generated {quantity} piece(s) of NFT artwork. You now need to mint them.")
            create_nft.delay(quantity, token.id)

        return super().form_valid(form)

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = Token.objects.get(id = self.kwargs['id'])
        return context

   
class NFTFromArtworkGeneratorView(generic.FormView):
    """
    FormView to create NFT from pre made artwork.

    An instance of :form:`NFTForm`.

    **Template:**

    :template:`nft_generator/nft_from_artwork_generator.html`
    """
    form_class = NFTForm
    template_name = "nft_generator/nft_from_artwork_generator.html"
    success_url = '/nfts'
    
    def form_valid(self, form):
        quantity = form.cleaned_data.get('quantity')
        
        token = Token.objects.get(id =self.kwargs['id'])
        if quantity > token.get_remaining_supply:
            messages.error(self.request, f"You have {token.get_remaining_supply} remaining supply")
        else:
            create_nft_from_artwork.delay(token.id)
            messages.success(self.request, f"Your artwork is ready. You now need to mint them.")
        return super().form_valid(form)

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["token"] = Token.objects.get(id = self.kwargs['id'])
        return context

   
        
class NFTView(generic.DetailView):
    """
    DetailView that displays individual NFT.

    An instance of :model:`nft_generator.NoneFungibleToken`.

    **Template:**

    :template:`nft_generator/nft.html`
    """
    template_name = "nft_generator/nft.html"
    model = NoneFungibleToken

    def get_object(self):
        return NoneFungibleToken.objects.get(id = self.kwargs["id"])

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class NFTSView(generic.ListView):
    """
    Listview that displays all NFT's in database.

    Queryset of :model:`nft_generator.NoneFungibleToken`.

    **Template:**

    :template:`nft_generator/nfts.html`
    """
    template_name = "nft_generator/nfts.html"
    model = NoneFungibleToken
    paginate_by = 50

    def get_queryset(self, **kwargs):
        objects = self.model.objects.filter(account__isnull=True)
        token_id = self.request.GET.get('token_id', None)
        if token_id:
            token = Token.objects.get(id = token_id)
            objects = self.model.objects.filter(token = token)
        account_id = self.request.GET.get('account_id', None)
        if account_id:
            account = Account.objects.get(id = account_id)
            objects = self.model.objects.filter(account = account)
        object_list = sorted(objects, key = lambda r: r.overall_rarity)
        return object_list
    
    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token_id = self.request.GET.get("token_id", None)
        context["token_id"] = token_id
        return context



class TokenView(generic.FormView):
    """
    FormView to a create new Tokens (project).

    An instance of :form:`TokenForm`.

    **Template:**

    :template:`nft_generator/token.html`
    """
    form_class = TokenForm
    template_name = "nft_generator/token.html"
    success_url = '/tokens/'
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)




class TokensView(generic.ListView):
    """
    Listview that displays all tokens in database.

    Queryset of :model:`nft_generator.Token`.

    **Template:**

    :template:`nft_generator/tokens.html`
    """
    template_name = "nft_generator/tokens.html"
    model = Token
    paginate_by = 50

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)




class MintView(generic.FormView):
    """
    FormView to mint all un-minted NFT objects.

    An instance of :form:`MintingForm`.

    **Template:**

    :template:`nft_generator/minting.html`
    """
    form_class = MintingForm
    template_name = "nft_generator/minting.html"
    success_url = '/nfts'
    
    def form_valid(self, form):
        mint = form.cleaned_data.get('mint')
        if mint == 'Yes':
            mint_nft(Token.objects.get(id = self.kwargs['id']))
            messages.success(self.request, "All NFT's have been processed")
        else:
            messages.success(self.request, "No NFT's were minted")
        return super().form_valid(form)

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(id = self.kwargs['id'])
        context["token"] = token
        context["nfts"] = NoneFungibleToken.objects.filter(minted=False, token = token)
        return context



class AssociateView(generic.FormView):
    """
    FormView to a associate an Account to a Token.

    An instance of :form:`AssociateForm`.

    **Template:**

    :template:`nft_generator/associate.html`
    """
    form_class = AssociateForm
    template_name = "nft_generator/associate.html"
    success_url = '/nfts'
    
    def form_valid(self, form):
        associate = form.cleaned_data.get('associate')
        account = form.cleaned_data.get('account')
        if associate == 'Yes':
            token_id = self.kwargs['id']
            associate_account(token_id, account.account_id)
            messages.success(self.request, "Account has been associated")
            token = Token.objects.get(id = token_id)
            token.associated_accounts.add(account)
            token.save()
        else:
            messages.success(self.request, "No accounts have been associated")
        
        return super().form_valid(form)

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token = Token.objects.get(id = self.kwargs['id'])
        context["token"] = token
        return context 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        token = Token.objects.get(id = self.kwargs['id'])
        associated_account_ids = [a.id for a in token.associated_accounts.all()]
        accounts = Account.objects.exclude(id__in=associated_account_ids)
        kwargs.update({'accounts': accounts})
        return kwargs



class TransferView(generic.FormView):
    """
    FormView to a transfer an NFT to an associated Account.

    An instance of :form:`TransferForm`.

    **Template:**

    :template:`nft_generator/transfer.html`
    """
    form_class = TransferForm
    template_name = "nft_generator/transfer.html"
    success_url = '/nfts'
    
    def form_valid(self, form):
        transfer = form.cleaned_data.get('transfer')
        account = form.cleaned_data.get('account')
        if transfer == 'Yes':
            nft_id = self.kwargs['id']
            transfer_nft(nft_id, account.id)
            messages.success(self.request, "NFT is being transferred")
            nft = NoneFungibleToken.objects.get(id = nft_id)
            nft.account = account
            nft.save()
        else:
            messages.success(self.request, "NFT has not been transferred")
        
        return super().form_valid(form)

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nft = NoneFungibleToken.objects.get(id = self.kwargs['id'])
        context["nft"] = nft
        return context 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        nft = NoneFungibleToken.objects.get(id = self.kwargs['id'])
        associated_account_ids = [a.id for a in nft.token.associated_accounts.all()]
        accounts = Account.objects.filter(id__in=associated_account_ids)
        kwargs.update({'accounts': accounts})
        return kwargs




class AccountsView(generic.ListView):
    """
    Listview that displays all Accounts in database.

    Queryset of :model:`nft_generator.Account`.

    **Template:**

    :template:`nft_generator/accounts.html`
    """
    template_name = "nft_generator/accounts.html"
    model = Account
    paginate_by = 50

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)



class AccountView(generic.ListView):
    """
    Listview that displays all NFT's for an Account.

    Queryset of :model:`nft_generator.NoneFungibleToken`.

    **Template:**

    :template:`nft_generator/account.html`
    """
    template_name = "nft_generator/account.html"
    model = NoneFungibleToken
    paginate_by = 50

    @method_decorator(redirect_if_no_token)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        object_list = NoneFungibleToken.objects.filter(account__id = self.kwargs['id'])
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = Account.objects.get(id = self.kwargs['id'])
        manager = AccountManager(account = object)
        balance_response = manager.query_account_balance()
        info_response = manager.query_account_info()
        object.nft_balance = int(info_response["nfts"])
        object.hbar_balance = balance_response["hbars"]
        object.save()
        context["object"] = object
        return context 


def send_to_ipfs(request, id):
    """
    view to handel admin NFT creation
    """
    create_ipfs_cid(id)

    return redirect(request.GET.get("url"))

def create_from_traits(request, id):
    """
    view to handel admin NFT creation from trait list
    """
    create_new_from_traits(id)

    return redirect(request.GET.get("url"))


def create_from_own_artwork(request, id):
    """
    view to handel admin NFT creation from trait list
    """
    create_from_own_artwork(id)

    return redirect(request.GET.get("url"))