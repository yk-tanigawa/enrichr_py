# -*- coding: utf-8 -*-

import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import enrichr_py

class BasicTestSuite(unittest.TestCase):
    """Basic test cases."""

    def test(self):
        query_name = 'sample_fuzzy_gene_list'
        gene_set_name = 'KEGG_2016'

        query_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', '{}.txt'.format(query_name)))
        with open(query_file) as f:
            query_txt = f.read()
        try:
            query = enrichr_py.Enrichr(query_txt, query_name)
            query.enrich(gene_set_name)
        except:
            raise()

        assert True


if __name__ == '__main__':
    unittest.main()
