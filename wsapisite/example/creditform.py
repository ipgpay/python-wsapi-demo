from django import forms
import os

from .wsapi import WSAPI

# set these in some secure way in your environment rather than in source code.
# os.environ['WSAPI_CLIENT_ID'] = '...'
# os.environ['WSAPI_API_KEY'] = '...'
# os.environ['WSAPI_API_HOST'] = 'https://my.ipgpay.com'


class CreditForm(forms.Form):
    order_id = forms.CharField()
    trans_id = forms.CharField()
    amount = forms.CharField()
    reason = forms.CharField()
    reference = forms.CharField()

    def __init__(self, request, *args, **kwargs):
        client_id = os.environ.get('WSAPI_CLIENT_ID', '')
        api_key = os.environ.get('WSAPI_API_KEY', '')
        api_host = os.environ.get('WSAPI_API_HOST', '')

        self.api = WSAPI(client_id, api_key, api_host)
        self.request = request

        super(CreditForm, self).__init__(*args, **kwargs)

    def credit_order(self):
        form_data = self.cleaned_data
        settlement_data = self.api.order_credit(form_data)

        self.request.session['last_credit'] = settlement_data.toJSON()

    def clean(self):
        return self.cleaned_data
