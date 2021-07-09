class Package:
    def __init__(self, id, delivery_address, deadline, weight, special_notes, delivery_status):
        self.id = id
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status

    def get_id(self):
        return self.id
    
    def __repr__(self):
        return self.id + ', ' + self.delivery_address + ', ' + self.deadline + ', ' + self.weight + ', ' + self.special_notes + ', ' + str(self.delivery_status or '')