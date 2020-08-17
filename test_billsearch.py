import unittest

from billsearch import *
from datasource import *

class TestBillSearch(unittest.TestCase):
    '''
    These tests are intended to do some basic sanity checks on the data
    handler and the main billsearch file.
    '''

    # Test Data Source
    def test_default_file_exists(self):
        ds = DataSource()
        self.assertTrue(ds.find_file_dir())

    def test_non_existent_file(self):
        ds = DataSource(file_dir = 'hello_world.zip')
        self.assertFalse(ds.find_file_dir())

    def test_ds_iter_not_empty(self):
        ds = DataSource()
        self.assertTrue(ds.get_iter())

    def test_clean_text(self):
        self.assertEqual(clean_text('<p>Hello world!    </p>'), \
                                    'Hello world!')


    # Test Bill Search
    def test_simple_match_easy(self):
        ds = DataSource()
        expr = 'American \w+ Bureau'
        matches = simple_matches(ds,expr)
        self.assertEqual(len(matches),1)

        for bill_id,_ in matches.items():
            self.assertEqual(bill_id,'SRES 39')

    def test_simple_match_bogus_expr(self):
        ds = DataSource()
        expr = 'w\++3^sd'
        self.assertFalse(simple_matches(ds,expr))
        
    def test_matches_with_substrings_easy(self):
        ds = DataSource()
        expr = 'American \w+ Bureau'
        matches = matches_with_substrings(ds,expr)
        self.assertEqual(len(matches),1)

    def test_matches_with_substrings_bogus_expr(self):
        ds = DataSource()
        expr = '()rtvse/-'
        self.assertFalse(matches_with_substrings(ds,expr))

    def test_display_matching_substring_no_match(self):
        string = 'Hello World'
        matches = []
        display_match = display_matching_substring((string,matches))
        self.assertEqual(display_match,'Hello World\n')

    def test_display_matching_substring_match(self):
        string = 'Hello World'
        matches = [(3,7)]
        display_match = display_matching_substring((string,matches))
        self.assertEqual(display_match,'Hel{}lo W{}orld\n' \
                                        .format('\033[4m','\033[0m'))

if __name__ == '__main__':
    unittest.main()