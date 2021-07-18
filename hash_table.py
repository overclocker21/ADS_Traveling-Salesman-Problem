# In HashMap key is usually int or string but value can be anything.
# O(1) for add, get, delete

# Array is used to store the data under the hood
# Implementation from Joe James: https://www.youtube.com/watch?v=9HFbhPscPU0

class HashMap:
    def __init__(self, size):
        self.size = size
        #init array with name map
        self.map = [None] * size

    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        
        return hash % self.size

    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    pair[1] = value
                    return True
            self.map[key_hash].append(key_value)
            return True

    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None
    
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True

    def print(self):
        print('Printing map')
        for item in self.map:
            if item is not None:
                print(str(item))

    def getMap(self):
        return self.map

# h = HashMap(4)

# h.add('Bob', 'Stone')
# h.add('Pratik', 'Kurtik')

# h.print()

# h.delete('Pratik')

# h.print()