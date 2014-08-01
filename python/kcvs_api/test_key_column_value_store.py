import unittest
from key_column_value_store import *

class TestKeyColumnValueStore(unittest.TestCase):

    def test_set(self):
        # setup
        store = KeyColumnValueStore()

        # execute
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'y')
        store.set('c', 'cc', 'z')
        store.set('c', 'cd', 'x')
        store.set('d', 'de', 'y')
        store.set('d', 'df', 'z')

        # expectations
        results = store.get_store()
        self.assertTrue(results['a']['aa'] == 'x')
        self.assertTrue(results['a']['ab'] == 'y')
        self.assertTrue(results['c']['cc'] == 'z')
        self.assertTrue(results['c']['cd'] == 'x')
        self.assertTrue(results['d']['de'] == 'y')
        self.assertTrue(results['d']['df'] == 'z')

    def test_set_overwrite_column_values(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'aa', 'y')

        results = store.get_store()
        self.assertTrue(results['a']['aa'] == 'y')

    def test_get(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('c', 'cc', 'x')
        store.set('c', 'cd', 'x')
        store.set('d', 'de', 'x')
        store.set('d', 'df', 'x')
        self.assertTrue(store.get('a', 'aa') == 'x')
        self.assertTrue(store.get('a', 'ab') == 'x')
        self.assertTrue(store.get('c', 'cc') == 'x')
        self.assertFalse(store.get('o', 'aa') == 'x')
        self.assertTrue(store.get('o', 'aa') == None)

    def test_get_return_none(self):
        store = KeyColumnValueStore()
        self.assertEqual(store.get('1', 'aa'), None)

    #get_key
    def test_get_key(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('b', 'cc', 'y')
        self.assertTrue(store.get_key('a') == [('aa', 'x'), ('ab', 'x')])

    def test_get_key_must_sort(self):
        store = KeyColumnValueStore()
        store.set('a', 'cc', 'y')
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        self.assertTrue(store.get_key('a') == [('aa', 'x'), ('ab', 'x'), ('cc', 'y')])

    def test_get_key_key_dne(self):
        store = KeyColumnValueStore()
        self.assertTrue(store.get_key('a') == [])

    def test_get_keys(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('b', 'bb', 'y')
        self.assertTrue(store.get_keys(), ['a', 'b'])

    def test_get_keys_return_empty_array_when_empty(self):
        store = KeyColumnValueStore()
        self.assertEqual(store.get_keys(), [])

    def test_delete(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'y')
        store.set('b', 'bb', 'z')
        store.set('d', 'de', 'x')
        store.set('d', 'df', 'x')
        self.assertTrue(store.get('a', 'aa') == 'x')
        store.delete('a', 'aa')
        self.assertTrue(store.get('a', 'aa') == None)
        self.assertTrue(store.get('a', 'ab') == 'y')
        self.assertTrue(store.get('b', 'bb') == 'z')

    # make sure we handle deleting of non existent keys
    def test_delete_non_existent(self):
        store = KeyColumnValueStore()
        self.assertTrue(store.delete('a', 'aa') == None)
        store.set('a', 'ab', 'x')
        self.assertTrue(store.delete('a', 'ab') == None)

    def test_delete_key(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('c', 'cc', 'x')
        store.set('c', 'cd', 'x')
        store.set('d', 'de', 'x')
        store.set('d', 'df', 'x')
        store.delete_key('c')
        self.assertTrue(store.get_key('c') == [])
        self.assertTrue(store.get_key('a') == [('aa', 'x'), ('ab', 'x')])

    def test_delete_key(self):
        store = KeyColumnValueStore()
        self.assertTrue(store.delete_key('a') == None)

    def test_get_slice(self):
        store = KeyColumnValueStore()
        store.set('a', 'aa', 'x')
        store.set('a', 'ab', 'x')
        store.set('a', 'ac', 'x')
        store.set('a', 'ad', 'x')
        store.set('a', 'ae', 'x')
        store.set('a', 'af', 'x')
        store.set('a', 'ag', 'x')
        self.assertTrue(store.get_slice('a', 'ae') == [('ae', 'x'), ('af', 'x'), ('ag', 'x')])
        self.assertTrue(store.get_slice('a', 'ae', None) == [('ae', 'x'), ('af', 'x'), ('ag', 'x')])
        self.assertTrue(store.get_slice('a', None, 'ac') == [('aa', 'x'), ('ab', 'x'), ('ac', 'x')])

    # helper methods
    def test_get_start_index(self):
        my_list = ['aa', 'ab']
        store = KeyColumnValueStore()
        self.assertEqual(store.get_start_index(my_list, 'ab'), 1)
        self.assertEqual(store.get_start_index(my_list, 'cc'), 0)

    def test_get_stop_index(self):
        store = KeyColumnValueStore()
        my_list = ['aa', 'ab', 'ac']
        start_index = 1

        self.assertEqual(store.get_stop_index(my_list, start_index, 'ac'), 3)
        self.assertEqual(store.get_stop_index(my_list, start_index, 'cc'), 3)

    # level 3 - persistance
    def test_persist(self):
        path = '/tmp/codetestdata'
        store = KeyColumnValueStore(path)

        self.assertFalse(os.path.isfile(path))
        # also test the set method
        store.set('a', 'aa', 'x')
        store.persist()
        self.assertTrue(os.path.isfile(path+'.db'))
        store2 = KeyColumnValueStore(path)
        store2.load()
        self.assertTrue(store2.get('a', 'aa') == 'x')

    def test_persist_delete(self):
        path = '/tmp/codetestdata'
        store = KeyColumnValueStore(path)

        store.set('a', 'aa', 'x')
        store.persist()

        store2 = KeyColumnValueStore(path)
        store2.load()

        store.delete('a', 'aa')
        self.assertTrue(store2.get('a', 'aa') == 'x')
        store2.load()
        self.assertTrue(store2.get('a', 'aa') == None)

    def test_persist_delete_key(self):
        path = '/tmp/codetestdata'
        store = KeyColumnValueStore(path)

        store.set('a', 'aa', 'x')
        store.persist()

        store2 = KeyColumnValueStore(path)
        store2.load()
        self.assertTrue(store2.get('a', 'aa') == 'x')

        store.delete_key('a')
        self.assertTrue(store2.get('a', 'aa') == 'x')
        store2.load()
        self.assertTrue(store2.get('a', 'aa') == None)
        self.assertTrue(store2.get_key('a') == [])


# Construct - Only run when this file is called as the main module
if __name__ == '__main__':
    unittest.main()