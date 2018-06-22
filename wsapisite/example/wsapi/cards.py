# <?xml version="1.0" encoding="UTF-8"?>
# <cards>
#   <num_records>1</num_records>
#   <card>
#       <order_id>28649451</order_id>
#       <card_number>************0010</card_number>
#       <exp_month>05</exp_month>
#       <exp_year>30</exp_year>
#       <type>Visa</type>
#   </card>
# </cards>
from xml.etree import ElementTree
from xml.etree.ElementTree import Element


class Cards(object):
    num_records = 0
    cards = []

    @staticmethod
    def from_xml(xml_data):
        dom = ElementTree.XML(xml_data)

        cards = Cards()
        if isinstance(dom, Element):
            cards.num_records = int(dom.find('num_records').text)
            fields = ['order_id', 'card_number', 'exp_month', 'exp_year', 'type']

            for card in dom.findall('card'):
                new_card = {k: card.find(k).text for k in fields}
                cards.cards.append(new_card)

        return cards
