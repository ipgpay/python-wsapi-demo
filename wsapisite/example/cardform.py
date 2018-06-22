from django import forms
from django.forms import ValidationError
import os

# from .wsapi.wsapi import WSAPI
from .wsapi import WSAPI

# set these in some secure way in your environment rather than in source code.
# os.environ['WSAPI_CLIENT_ID'] = '...'
# os.environ['WSAPI_API_KEY'] = '...'
# os.environ['WSAPI_API_HOST'] = 'https://my.ipgpay.com'


class CardForm(forms.Form):
    card_number = forms.CharField()
    exp_month = forms.CharField()
    exp_year = forms.CharField()
    cvv = forms.CharField()
    card_holder_name = forms.CharField()
    payment_trans_type = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        client_id = os.environ.get('WSAPI_CLIENT_ID', '')
        api_key = os.environ.get('WSAPI_API_KEY', '')
        api_host = os.environ.get('WSAPI_API_HOST', '')

        self.api = WSAPI(client_id, api_key, api_host)
        self.request = request

        super(CardForm, self).__init__(*args, **kwargs)

    def submit_order(self):
        cart = [
            {'qty': 1, 'name': 'Example item', 'unit_price_USD': '10.00', 'digital': '1'}
        ]
        card = self.cleaned_data

        # customer needs to be filled in
        customer = {
            'id': 123456,
            'email': 'test@example.com'
        }

        order_data = self.api.order_submit(cart, card, customer, 'USD')
        self.request.session['last_order'] = order_data.toJSON()
        self.request.session['last_order_is_auth'] = card['payment_trans_type'] == 'auth'
        self.request.session['last_settlement'] = None
        self.request.session['last_credit'] = None

    def clean(self):
        if self.cleaned_data.get('card_number', '') == '':
            raise ValidationError('Invalid PAN')

        return self.cleaned_data
