# references:
# http://www.tutorialspoint.com/python
# https://docs.python.org/2/library/shelve.html?highlight=dictionary
import shelve
import os


class KeyColumnValueStore:

    def __init__(self, path=None):
        self._store = {}
        self._key = 'shelve_key'
        self._path = path

        # Load from file if it exist and contains data
        if self._path != None:
            self._path = os.path.abspath(path)
            self.load()
            
    
    # Support loading a dataset from disk
    def load(self):
        ds = shelve.open(self._path)
        if ds.has_key(self._key):
            self._store = ds[self._key]

    # Support for persisting the data to disk
    def persist(self):
        if self._path:
            ds = shelve.open(self._path)
            ds[self._key] = self._store
            ds.close()

    # Sets the value at the given key/column
    def set(self, key, col, val):
        if key in self._store:
            self._store[key][col] = val
        else:
            self._store[key] = {col: val}
        self.persist()

    # Return the value at the specified key/column 
    def get(self, key, col):
        if self._store.get(key) is None:
            return None
        else:
            return self._store.get(key).get(col)

    # Returns a sorted list of column/value tuples
    def get_key(self, key):
        if key in self._store:
            return sorted(self._store[key].items())
        else:
            return []

    # Returns a set containing all of the keys in the store
    def get_keys(self):
        return self._store.keys()

    # Removes a column/value from the given key
    def delete(self, key, col):
        if self._store.get(key) is None:
            return None
        del self._store[key][col]
        self.persist()

    # Removes all data associated with the given key
    def delete_key(self, key):
        if self._store.get(key) is None:
            return None
        del self._store[key]
        self.persist()


    # returns a sorted list of column/value tuples where the column
    # values are between the start and stop values, inclusive of the
    # start and stop values. Start and/or stop can be None values,
    # leaving the slice open ended in that direction
    def get_slice(self, key, start = None, stop = None):
        if self._store[key] == None:
            return []
        # must be sorted list
        my_list = sorted(self._store[key])
        start_index = self.get_start_index(my_list, start)
        stop_index = self.get_stop_index(my_list, start_index, stop)
        return [(item, self.get(key,item)) for item in my_list[start_index:stop_index]]


    ### Private methods

    # assuming the list contains the start value
    def get_start_index(self, my_list, column_to_start = None):
        if column_to_start == None:
            return 0
        # NOTE: Python's try/except block is extremely efficient 
        # if no exceptions are raised.
        # Currently assuming the list contains the start value almost all the time
        # if not the case, use if statements
        try:
            return my_list.index(column_to_start)
        except ValueError:
            return 0

    # get stop index (added 1 to include stop column)
    def get_stop_index(self, my_list, start_index, column_to_stop):
        if column_to_stop == None:
            return start_index + 3
        else:
            try:
                return my_list.index(column_to_stop) + 1
            except ValueError:
                # prevent index from being out of range
                if (start_index+2) < len(my_list):
                    return start_index + 3
                else:
                    return len(my_list)



    # Getter for the whole store
    def get_store(self):
        return self._store

