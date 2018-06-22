import json
from xml.etree import ElementTree

# <order>
#     <order_id>29852831</order_id>
#     <order_total>100.00</order_total>
#     <test_transaction>1</test_transaction>
#     <order_datetime>2018-06-01 07:15:07</order_datetime>
#     <order_status>Paid</order_status>
#     <customer_id>532301</customer_id>
#     <cart>
#         <item>
#             <id>55038171</id>
#             <code />
#             <name>Example item</name>
#             <description />
#             <qty>1</qty>
#             <digital>1</digital>
#             <discount>0</discount>
#             <predefined>0</predefined>
#             <unit_price>100.00</unit_price>
#         </item>
#     </cart>
#     <transaction>
#         <type>sale</type>
#         <response>A</response>
#         <response_code>OP000</response_code>
#         <response_text>ApproveTEST</response_text>
#         <trans_id>625070511</trans_id>
#         <account_id>571961</account_id>
#     </transaction>
# </order>


class Order(object):
    order_id = None
    order_total = None
    test_transaction = None
    order_datetime = None
    order_status = None
    customer_id = None

    items = None

    transaction = None

    # noinspection PyPep8Naming
    def toJSON(self):
        return json.dumps(self, cls=OrderEncoder, sort_keys=True, indent=4)

    @staticmethod
    def from_xml(xml_data):
        dom = ElementTree.XML(xml_data)

        order = Order()
        order.items = []
        fields = ['order_id', 'order_total', 'test_transaction', 'order_datetime', 'order_status', 'customer_id']
        item_fields = ['id', 'code', 'name', 'description', 'qty', 'digital', 'discount', 'predefined', 'unit_price']
        transaction_fields = ['type', 'response', 'response_code', 'response_text', 'trans_id', 'account_id']

        for field in fields:
            setattr(order, field, dom.find(field).text)

        for item_node in dom.find('cart').findall('item'):
            item = dict()
            for field in item_fields:
                item[field] = item_node.find(field).text
            order.items.append(item)

        transaction = dict()
        transaction_node = dom.find('transaction')
        for field in transaction_fields:
            value = transaction_node.find(field).text
            transaction[field] = value
        order.transaction = transaction

        return order


class OrderEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Order):
            data = obj.__dict__
            data['items'] = obj.items
            return data
        return json.JSONEncoder.default(self, obj)
