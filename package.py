import math
class Package:
    def __init__(self, id=None, delivery_address=None, deadline=None, weight=None, special_notes=None, timestamp=None, delivery_status=None):
        self.id = id
        self.delivery_address = delivery_address
        self.deadline = deadline
        self.weight = weight
        self.special_notes = special_notes
        self.timestamp = timestamp
        self.delivery_status = delivery_status

    def get_id(self):
        return self.id

    def get_address(self):
        return self.delivery_address

    def set_status(self, status):
        self.delivery_status = status

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_timestamp(self):
        return self.timestamp

    def format_time(self, timestamp):
        if timestamp != None:
            hours = math.floor(timestamp)
            minutes = math.floor(round(timestamp - math.floor(timestamp),2)*60)
            if minutes < 10:
                minutes = '0'+str(minutes)
            return str(hours) + ':' + str(minutes)
    
    def __repr__(self):
        return self.delivery_address + ', ' + str(self.format_time(self.timestamp) or '') + ', ' + str(self.delivery_status or '')
