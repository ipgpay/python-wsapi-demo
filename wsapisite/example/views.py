from django.views.generic import FormView, TemplateView
import json

from .cardform import CardForm
from .settleform import SettleForm
from .creditform import CreditForm


class OrderIndexView(TemplateView):
    template_name = 'index.html'


class OrderSubmitView(FormView):

    initial = {
        'card_number': '4111111111111111',
        'exp_month': '12',
        'exp_year': '20',
        'cvv': '123',
        'card_holder_name': 'Valued Cardholder',
        'trans_type': 'wut'
    }
    template_name = 'form.html'
    form_class = CardForm
    success_url = '/order/receipt/'

    def form_valid(self, form):
        form.submit_order()
        return super().form_valid(form)

    def get_form_kwargs(self):
        # enforce the trans type to be sale or auth only.
        trans_type = 'sale' if self.request.GET.get('type', '') == 'sale' else 'auth'
        self.initial['payment_trans_type'] = trans_type

        kwargs = super(OrderSubmitView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class OrderSettleView(FormView):

    initial = {
        'notify': '0'
    }

    template_name = 'settle.html'
    form_class = SettleForm
    success_url = '/order/receipt/'

    def form_valid(self, form):
        form.settle_order()

        return super(OrderSettleView, self).form_valid(form)

    def get_form_kwargs(self):
        order = json.loads(self.request.session['last_order'])
        self.initial['order_id'] = order['order_id']
        self.initial['amount'] = order['order_total']

        kwargs = super(OrderSettleView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class OrderCreditView(FormView):

    template_name = 'credit.html'
    form_class = CreditForm
    success_url = '/order/receipt/'

    def form_valid(self, form):
        form.credit_order()

        return super(OrderCreditView, self).form_valid(form)

    def get_form_kwargs(self):
        order = json.loads(self.request.session['last_order'])
        self.initial['order_id'] = order['order_id']
        self.initial['amount'] = order['order_total']

        # if previous order was an auth, we need to settle using the SETTLEMENT TRANS ID.
        # otherwise, we can use the SALE TRANS ID.
        if order['transaction']['type'] == 'auth':
            last_settle = json.loads(self.request.session['last_settlement'])
            self.initial['trans_id'] = last_settle['trans_id']
        else:
            self.initial['trans_id'] = order['transaction']['trans_id']

        self.initial['reason'] = 'credited via wsapi'
        self.initial['reference'] = 'merchant-custom-ref'

        kwargs = super(OrderCreditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class OrderReceiptView(TemplateView):
    template_name = 'receipt.html'
