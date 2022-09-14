# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django import forms

# --------------------------------------------------------------
# App imports
# --------------------------------------------------------------
from .models import Token, Account


class NFTForm(forms.Form):
	
	quantity = forms.IntegerField(required=True,
		widget=forms.NumberInput(attrs={
			'placeholder': '*Quantity..',
			'class': 'form-control'
			}))

	
	class Meta:
		fields = ('quantity',)


class MintingForm(forms.Form):
	
	mint = forms.CharField(max_length=3, required=True, 
		widget=forms.Select(attrs={"class": "selection form-control"}, choices=(('No', 'No'),('Yes', 'Yes'))))
	class Meta:
		fields = ('mint',)


class AssociateForm(forms.Form):
	
	account = forms.ModelChoiceField(
		required=True,
		queryset=Account.objects.all(),
		empty_label="Select account"
	)
	associate = forms.CharField(max_length=3, required=True, 
		widget=forms.Select(attrs={"class": "selection form-control"}, choices=(('No', 'No'),('Yes', 'Yes'))))
	class Meta:
		fields = ('account','associate')

	def __init__(self, *args, **kwargs):
		accounts = kwargs.pop('accounts')   # get the owner object from kwargs
		super().__init__(*args, **kwargs)
		# assign owner to the field; note the use of .queryset on the field
		self.fields['account'].queryset = accounts 


class TokenForm(forms.ModelForm):

	company_name = forms.CharField(max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': '*Company name..',
			'class': 'form-control'}))
	
	name = forms.CharField(max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': '*Token name..',
			'class': 'form-control'}))

	symbol = forms.CharField(max_length=3,
		widget=forms.TextInput(attrs={
			'placeholder': '*Token symbol..',
			'class': 'form-control'}))

	description = forms.CharField(max_length=100,
		widget=forms.TextInput(attrs={
			'placeholder': '*Token description..',
			'class': 'form-control'}))


	max_supply = forms.IntegerField(required=True,
		widget=forms.NumberInput(attrs={
			'placeholder': '*Maximum supply..',
			'class': 'form-control'
			}))

	class Meta:
		model = Token
		fields = ('company_name','name','symbol','description','max_supply')


class TransferForm(forms.Form):
	
	account = forms.ModelChoiceField(
		required=True,
		queryset=Account.objects.all(),
		empty_label="Select account"
	)
	transfer = forms.CharField(max_length=3, required=True, 
		widget=forms.Select(attrs={"class": "selection form-control"}, choices=(('No', 'No'),('Yes', 'Yes'))))
	class Meta:
		fields = ('account','transfer')

	def __init__(self, *args, **kwargs):
		accounts = kwargs.pop('accounts')   # get the owner object from kwargs
		super().__init__(*args, **kwargs)
		# assign owner to the field; note the use of .queryset on the field
		self.fields['account'].queryset = accounts 