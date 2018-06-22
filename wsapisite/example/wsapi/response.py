import json
from xml.etree import ElementTree

# Example approval
# <settle>
#         <response>A</response>
#         <response_code>OP000</response_code>
#         <response_text>ApproveTEST</response_text>
#         <trans_id>625070511</trans_id>
# </settle>
#
# Example decline
# <settle>
#         <response>D</response>
#         <response_code>OP123</response_code>
#         <response_text>Order already settled</response_text>
#         <trans_id />
# </settle>


class Response(object):
    response = None
    responsecode = None
    responsetext = None
    trans_id = None

    # noinspection PyPep8Naming
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @staticmethod
    def from_xml(xml_data):
        dom = ElementTree.XML(xml_data)

        settlement = Response()
        fields = ['response', 'responsecode', 'responsetext', 'trans_id']

        for field in fields:
            if dom.find(field) is None:
                continue

            setattr(settlement, field, dom.find(field).text)

        return settlement
