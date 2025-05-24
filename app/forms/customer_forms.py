class GameSearchForm:
    def __init__(self, formdata):
        self.search_query = formdata.get('search_query', '')
        self.submit = formdata.get('submit', None)

class ShippingForm:
    def __init__(self, formdata):
        self.shipping_address = formdata.get('shipping_address', '')
        self.phone_number = formdata.get('phone_number', '')
        self.special_instructions = formdata.get('special_instructions', '')
        self.submit = formdata.get('submit', None)
