class Package:
    def __init__(self, id=None, delivery_address=None, deadline=None, weight=None, special_notes=None, delivery_status=None):
        self.id = id
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status

    def get_id(self):
        return self.id

    def get_address(self):
        return self.delivery_address

    def set_status(self, status):
        self.delivery_status = status
    
    def __repr__(self):
        return self.delivery_address + ', ' + self.deadline + ', ' + self.weight + ', ' + self.special_notes + ', ' + str(self.delivery_status or '')