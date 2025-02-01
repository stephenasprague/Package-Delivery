class ChainingHashTable:
    # initialize hash table and set initial size
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # define insert function
    def insert(self, key, item):
        # hash key to find bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # search bucket for key, return True if key found
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = item
                return True

        # insert key into bucket
        key_value = [key, item]
        bucket_list.append(key_value)

    # define search function
    def search(self, key):
        # hash key to find bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # return value if key is found, return None if not found
        for key_value in bucket_list:
            if key_value[0] == key:
                return key_value[1]
        return None

    # define remove function
    def remove(self, key):
        # hash key to find bucket
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # remove key-value pair if key is found
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove([kv[0], kv[1]])

