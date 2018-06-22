import requests
from .cards import Cards
from .order import Order
from . import InvalidQueryException
from .response import Response


class WSAPI(object):

    def __init__(self, client_id, api_key, api_host):
        self.client_id = client_id
        self.api_key = api_key
        self.api_host = api_host

    def customer_get_cards(self, customer_id, customer_email, is_test=False):
        form_data = {
            'client_id': self.client_id,
            'api_key': self.api_key,
            'test_transaction': '1' if is_test else '0',
            'customer_id': customer_id,
            'email': customer_email
        }
        request_url = '{}/service/customer/getcards'.format(self.api_host)
        res = requests.post(request_url, data=form_data)
        try:
            data = Cards.from_xml(res.text)
        except InvalidQueryException:
            data = None

        return data

    def order_submit(self, cart, card, customer, currency):
        data = dict()

        # populate generic order related fields
        data['client_id'] = self.client_id
        data['api_key'] = self.api_key
        data['order_currency'] = currency
        data['ip_address'] = '127.0.0.1'
        data['order_reference'] = 'reference'
        data['test_transaction'] = '1'

        # populate the item related fields
        for index, item in enumerate(cart):
            for field in item.keys():
                param = 'item_{}_{}'.format(index + 1, field)
                data[param] = item[field]

        for field in customer:
            param = 'customer_{}'.format(field)
            data[param] = customer[field]

        # NOTE: When submitting orders via One Time Token, only this part is different.
        # Transmitting the card data in raw format REQUIRES PCI compliance.
        data['payment_type'] = 'creditcard'
        for field in card:
            data[field] = card[field]

        request_url = '{}/service/order/submit'.format(self.api_host)
        res = requests.post(request_url, data=data)
        try:
            order = Order.from_xml(res.text)
        except InvalidQueryException:
            order = None

        return order

    def order_settle(self, form_data):
        data = dict()
        data['client_id'] = self.client_id
        data['api_key'] = self.api_key
        data['order_id'] = form_data['order_id']
        data['amount'] = form_data['amount']

        request_url = '{}/service/order/settle'.format(self.api_host)
        res = requests.post(request_url, data=data)
        try:
            settle = Response.from_xml(res.text)
        except InvalidQueryException:
            settle = None

        return settle

    def order_credit(self, form_data):
        data = dict()
        data['client_id'] = self.client_id
        data['api_key'] = self.api_key
        data['order_id'] = form_data['order_id']
        data['trans_id'] = form_data['trans_id']
        data['amount'] = form_data['amount']
        data['reason'] = form_data['reason']
        data['reference'] = form_data['reference']

        request_url = '{}/service/order/credit'.format(self.api_host)
        res = requests.post(request_url, data=data)
        try:
            settle = Response.from_xml(res.text)
        except InvalidQueryException:
            settle = None

        return settle

    def __repr__(self):
        return 'Web Services API'
