import unittest
import manipulation as man
import collections as col
import random as rand
import itertools as itt
import helper as hpr


class TestManipulation(unittest.TestCase):
    def setUp(self):
        self.col1 = [i for i in range(0, 50)]
        self.col2 = [i for i in range(100, 150)]
        self.col3 = [i for i in range(0, 3)]
        self.col4 = [i for i in range(10, 13)]
        self.col5 = [i for i in range(0, 5)]
        self.col6 = [i for i in range(0, 6)]
        self.tb1 = {'col1': self.col1}
        self.tb2 = {'col2': self.col2}
        self.tb3 = {'col3': self.col3, 'col4': self.col4}
        self.tb4 = {'col5': self.col5}
        self.tb5 = {'col6': self.col6}
        # Testing reduce table
        self.tb6 = {'col1': self.col1, 'col2': self.col2, 'col3': self.col3,
                    'col4': self.col4, 'col5': self.col5}
        # col_indexes for testing joining filtered column indexes
        self.overlap1 = [i for i in range(0, 50)]
        self.overlap2 = [i for i in range(25, 75)]
        self.noverlap1 = [i for i in range(0, 50)]
        self.noverlap2 = [i for i in range(100, 150)]
        # tb1 with overlap, tb2 without overlap
        self.tbA_name = 'tbA'
        self.tbB_name = 'tbB'
        self.ind1 = {self.tbA_name: self.overlap1,
                     self.tbB_name: self.noverlap1}
        self.ind2 = {self.tbA_name: self.overlap2,
                     self.tbB_name: self.noverlap2}
        self.tbA = {'colA1': [str(i) for i in range(0, 1000)],
                    'colA2': [str(i) for i in range(0, 1000)],
                    'colA3': [str(i) for i in range(0, 1000)]}
        self.tbB = {'colB1': [str(i) for i in range(0, 1000)]}
        self.tables = {self.tbA_name: self.tbA, self.tbB_name: self.tbB}
        # list with duplicates
        rand_lst = [str(i) for i in range(0, 10000)]
        # 9 duplicates
        self.a_locations = [0, 100, 200, 300, 400, 500, 600, 700, 800]
        # 10 duplicates
        self.b_locations = [3000, 3100, 3200, 3300, 3400, 3500, 3600,
                            4500, 5000, 5500]
        self.dup_src = rand_lst.copy()
        for loc in self.a_locations:
            self.dup_src.insert(loc, 'a')
        for loc in self.b_locations:
            self.dup_src.insert(loc, 'b')
        # 9 duplicates
        self.c_locations = [400, 500, 1000, 1100, 1200, 1300, 1400, 1500, 1600]
        # 10 duplicates
        self.d_locations = [4500, 5000, 5500, 5600, 5700, 5800, 5900, 6000,
                            6100, 6200, 6300]
        self.dup_src2 = rand_lst.copy()
        for loc in self.c_locations:
            self.dup_src2.insert(loc, 'c')
        for loc in self.d_locations:
            self.dup_src2.insert(loc, 'd')
        # For checking duplicate removals
        self.col41 = [str(i) for i in range(0, 1000) for __ in range(0, 2)]
        self.col42 = [str(i) for i in range(0, 500) for __ in range(0, 4)]
        self.col43 = [str(i) for i in range(0, 250) for __ in range(0, 8)]
        self.tb41 = {'col1': self.col41,
                     'col2': self.col42,
                     'col3': self.col43}
        self.e_col41 = [str(i) for i in range(0, 1000)]
        self.e_col42 = [str(i) for i in range(0, 500) for __ in range(0, 2)]
        self.e_col43 = [str(i) for i in range(0, 250) for __ in range(0, 4)]
        # tables for testing union, intersect and left outer intersect
        self.col51_str = ['a', 'b', 'c', 'd', 'e']
        self.col52_int = [1, 2, 3, 4, 5]
        self.col53_float = [0.1, 0.2, 0.3, 0.4, 0.5]
        # three rows are repeated
        self.col54_str = ['a', 'b', 'c', 'i', 'j']
        self.col55_int = [1, 2, 3, 9, 10]
        self.col56_float = [0.1, 0.2, 0.3, 0.9, 1.0]
        self.tb51 = {'str': self.col51_str,
                     'int': self.col52_int,
                     'float': self.col53_float}
        self.tb51_order = ['str', 'int', 'float']
        self.tb52 = {'str': self.col54_str,
                     'int': self.col55_int,
                     'float': self.col56_float}
        self.tb52_order = ['str', 'int', 'float']

    def test_duplicate_entries(self):
        # Double the original list size, i.e. each item is duplicated once
        test = list(man.duplicate(self.col1, 100))
        expected = [i for i in range(0, 50) for __ in range(0, 2)]
        self.assertEqual(test, expected)

    def test_cal_combined_size(self):
        expected = 2500
        test = man.combined_size((self.tb1, self.tb2))
        self.assertEqual(expected, test)

    def test_combine_one_table(self):
        test = man.combine([self.tb1])
        self.assertEqual(self.col1, list(test['col1']))

    def test_combine_two_tables(self):
        combined_col1 = [i for i in range(0, 50) for __ in range(0, 50)]
        combined_col2 = [i for i in range(100, 150) for __ in range(0, 50)]
        test = man.combine((self.tb1, self.tb2))
        # Check combined_col1
        self.assertEqual(combined_col1, list(test['col1']))
        # Check combined_col2
        self.assertEqual(combined_col2, list(test['col2']))

    def test_combine_three_tables(self):
        combined_col3 = [i for i in range(0, 3) for __ in range(0, 30)]
        combined_col4 = [i for i in range(10, 13) for __ in range(0, 30)]
        combined_col5 = [i for i in range(0, 5) for __ in range(0, 18)]
        combined_col6 = [i for i in range(0, 6) for __ in range(0, 15)]
        test = man.combine((self.tb3, self.tb4, self.tb5))
        # Check combined_col3
        self.assertEqual(combined_col3, list(test['col3']))
        # Check combined_col4
        self.assertEqual(combined_col4, list(test['col4']))
        # Check combined_col5
        self.assertEqual(combined_col5, list(test['col5']))
        # Check combined_col6
        self.assertEqual(combined_col6, list(test['col6']))

    def test_reduce_table(self):
        exp = {'col3': self.col3, 'col5': self.col5}
        test = man.reduce_tb(self.tb6, ['col3', 'col5'])
        self.assertIsNone(test.get('col1', None))
        self.assertIsNone(test.get('col2', None))
        self.assertIsNone(test.get('col4', None))
        self.assertIsNotNone(test.get('col3', None))
        self.assertIsNotNone(test.get('col5', None))
        self.assertEqual(exp, test)

    def test_split_exprn_no_brackets(self):
        no_bracks = 'Hello world'
        exp_atomic = [no_bracks]
        exp_conn = []
        test_atomic, test_conn = man.split_exprn(no_bracks)
        self.assertEqual(exp_atomic, test_atomic)
        self.assertEqual(exp_conn, test_conn)

    def test_split_exprn_single_exprn(self):
        one_brack = '(Hello world)'
        exp_atomic = ['Hello world']
        exp_conn = []
        test_atomic, test_conn = man.split_exprn(one_brack)
        self.assertEqual(exp_atomic, test_atomic)
        self.assertEqual(exp_conn, test_conn)

    def test_split_exprn_two_sub_exprn(self):
        two_sub_exprn = '((Hello world) Y (Bye world))'
        exp_atomic = ['Hello world', 'Bye world']
        exp_conn = [' Y ']
        test_atomic, test_conn = man.split_exprn(two_sub_exprn)
        self.assertEqual(exp_atomic, test_atomic)
        self.assertEqual(exp_conn, test_conn)

    def test_split_exprn_outside_exprn(self):
        two_atomics = "((EXISTE (EMPRESTA estadistica_nombre DE estadisticas))"\
                      " Y (pokemon_nombre PARECIO A 'pikachu'))"
        exp_atomic = ['EXISTE (EMPRESTA estadistica_nombre DE estadisticas)',
                      "pokemon_nombre PARECIO A 'pikachu'"]
        exp_conn = [' Y ']
        test_atomic, test_conn = man.split_exprn(two_atomics)
        self.assertEqual(exp_atomic, test_atomic)
        self.assertEqual(exp_conn, test_conn)

    def test_split_exprn_inner_and(self):
        exprn = '((encuentro_pokemon_id = pokemon_id) Y ' \
                '(encuentro_min ENTRE (30 Y 60)))'
        expected = ['encuentro_pokemon_id = pokemon_id',
                    'encuentro_min ENTRE (30 Y 60)']
        exp_conn = [' Y ']
        test_atomic, test_conn = man.split_exprn(exprn)
        self.assertEqual(test_atomic, expected)
        self.assertEqual(test_conn, exp_conn)

    def test_clean_exprn_empty(self):
        empty = ''
        exp = ''
        self.assertEqual(exp, man.clean_exprn(empty))

    def test_clean_exprn_single_start_brack(self):
        single = '(Hello world'
        expected = 'Hello world'
        self.assertEqual(expected, man.clean_exprn(single))

    def test_clean_exprn_brack_pair(self):
        pair = '(Hello world)'
        expected = 'Hello world'
        self.assertEqual(expected, man.clean_exprn(pair))

    def test_clean_exprn_multi_bracks(self):
        multi = '(((Hello world)'
        expected = 'Hello world'
        self.assertEqual(expected, man.clean_exprn(multi))

    def test_clean_exprn_preserve_necessary_brack(self):
        exprn = '(((EXISTE (Hello world en mi casa)))'
        expected = 'EXISTE (Hello world en mi casa)'
        self.assertEqual(expected, man.clean_exprn(exprn))

    def test_join_filt_indexes_AND(self):
        expected_tb1 = {self.tbA_name: [i for i in range(25, 50)]}
        expected_tb2 = {self.tbB_name: []}
        test = man.join_filt_indexes([self.tbA_name, self.tbB_name],
                                     self.ind1, self.ind2, ' Y ')
        test_tb1 = test[self.tbA_name]
        test_tb2 = test[self.tbB_name]
        self.assertEqual(test_tb1, expected_tb1[self.tbA_name])
        self.assertEqual(test_tb2, expected_tb2[self.tbB_name])

    def test_join_filt_indexes_OR(self):
        expected_tb1 = {self.tbA_name: [i for i in range(0, 75)]}
        expected_tb2 = {self.tbB_name: self.noverlap1 + self.noverlap2}
        test = man.join_filt_indexes([self.tbA_name, self.tbB_name],
                                     self.ind1, self.ind2, ' O ')
        test_tb1 = test[self.tbA_name]
        test_tb2 = test[self.tbB_name]
        self.assertEqual(test_tb1, expected_tb1[self.tbA_name])
        self.assertEqual(test_tb2, expected_tb2[self.tbB_name])

    def test_join_filt_indexes_bool_return_all(self):
        expected_tb1 = {self.tbA_name: self.overlap2}
        expected_tb2 = {self.tbB_name: self.noverlap2}
        test = man.join_filt_indexes([self.tbA_name, self.tbB_name],
                                     True, self.ind2, ' Y ')
        test_tb1 = test[self.tbA_name]
        test_tb2 = test[self.tbB_name]
        self.assertEqual(test_tb1, expected_tb1[self.tbA_name])
        self.assertEqual(test_tb2, expected_tb2[self.tbB_name])

    def test_filter_tables_by_indexes(self):
        filt_indexes = {self.tbA_name: [i for i in range(50, 100, 5)],
                        self.tbB_name: [i for i in range(20, 70, 10)]}
        expected_tba = {'colA1': [str(i) for i in range(50, 100, 5)],
                        'colA2': [str(i) for i in range(50, 100, 5)],
                        'colA3': [str(i) for i in range(50, 100, 5)]}
        expected_tbb = {'colB1': [str(i) for i in range(20, 70, 10)]}
        test_tables = man.filter_tables(self.tables, filt_indexes)
        test_tba = test_tables[self.tbA_name]
        test_tbb = test_tables[self.tbB_name]
        # Check each columns that they match
        self.assertEqual(test_tba['colA1'], expected_tba['colA1'])
        self.assertEqual(test_tba['colA2'], expected_tba['colA2'])
        self.assertEqual(test_tba['colA3'], expected_tba['colA3'])
        self.assertEqual(test_tbb['colB1'], expected_tbb['colB1'])

    def test_filter_tables_by_error_indexes_dont_filter(self):
        filt_indexes = {'Wrong table': [i for i in range(50, 100, 5)],
                        self.tbB_name: [i for i in range(20, 70, 10)]}
        expected_tba = {'colA1': self.tbA['colA1'],
                        'colA2': self.tbA['colA2'],
                        'colA3': self.tbA['colA3']}
        expected_tbb = {'colB1': [str(i) for i in range(20, 70, 10)]}
        test_tables = man.filter_tables(self.tables, filt_indexes)
        test_tba = test_tables[self.tbA_name]
        test_tbb = test_tables[self.tbB_name]
        # Check each columns that they match
        self.assertEqual(test_tba['colA1'], expected_tba['colA1'])
        self.assertEqual(test_tba['colA2'], expected_tba['colA2'])
        self.assertEqual(test_tba['colA3'], expected_tba['colA3'])
        self.assertEqual(test_tbb['colB1'], expected_tbb['colB1'])

    def test_filter_tables_by_empty_indexes_return_all(self):
        filt_indexes = {self.tbA_name: [],
                        self.tbB_name: [i for i in range(20, 70, 10)]}
        expected_tba = {'colA1': self.tbA['colA1'],
                        'colA2': self.tbA['colA2'],
                        'colA3': self.tbA['colA3']}
        expected_tbb = {'colB1': [str(i) for i in range(20, 70, 10)]}
        test_tables = man.filter_tables(self.tables, filt_indexes)
        test_tba = test_tables[self.tbA_name]
        test_tbb = test_tables[self.tbB_name]
        # Check each columns that they match
        self.assertEqual(test_tba['colA1'], expected_tba['colA1'])
        self.assertEqual(test_tba['colA2'], expected_tba['colA2'])
        self.assertEqual(test_tba['colA3'], expected_tba['colA3'])
        self.assertEqual(test_tbb['colB1'], expected_tbb['colB1'])

    def test_get_dup_lst(self):
        dup_indexes = man.get_dup_lst(self.dup_src)
        # There should only be two equivalence classes
        self.assertEqual(len(dup_indexes), 2)
        # Assert the locations of each list
        test_1 = dup_indexes[0]
        test_2 = dup_indexes[1]
        if len(test_1) == 9:
            self.assertEqual(test_1, self.a_locations)
        else:
            self.assertEqual(test_1, self.b_locations)
        if len(test_2) == 9:
            self.assertEqual(test_2, self.a_locations)
        else:
            self.assertEqual(test_2, self.b_locations)

    def test_get_dup_lst_with_prev_lst(self):
        # With a previous list, method should only check the indexes from the
        # previous list. Previous list represent the indexes of duplicates from
        # another column of the same table
        prev_lst = [self.a_locations, self.b_locations]
        exp_c_locs = [400, 500]
        exp_d_locs = [4500, 5000, 5500]
        dup_indexes = man.get_dup_lst(self.dup_src2, prev_lst)
        self.assertEqual(len(dup_indexes), 2)
        test_1 = dup_indexes[0]
        test_2 = dup_indexes[1]
        if len(test_1) == len(exp_c_locs):
            self.assertEqual(test_1, exp_c_locs)
        else:
            self.assertEqual(test_1, exp_d_locs)
        if len(test_2) == len(exp_c_locs):
            self.assertEqual(test_2, exp_c_locs)
        else:
            self.assertEqual(test_2, exp_d_locs)

    def test_remove_duplicate_rows(self):
        # Expected values
        test_tb = man.rmv_dups(self.tb41)
        t_col1 = test_tb['col1']
        t_col2 = test_tb['col2']
        t_col3 = test_tb['col3']
        self.assertEqual(len(t_col1), len(self.e_col41))
        self.assertEqual(len(t_col2), len(self.e_col42))
        self.assertEqual(len(t_col3), len(self.e_col43))
        self.assertEqual(t_col1, self.e_col41)
        self.assertEqual(t_col2, self.e_col42)
        self.assertEqual(t_col3, self.e_col43)

    def test_order_entries(self):
        entries = ['a', 'b', 'c', 'd', 'e']
        indexes = [2, 1, 0, 3, 4]
        expected = ['c', 'b', 'a', 'd', 'e']
        test = man.order_col(entries, indexes)
        self.assertEqual(test, expected)

    def test_order_entries_mismatch_length_throw_value_error(self):
        entries = ['a', 'b', 'c', 'd', 'e']
        indexes = [2, 1, 0, 3]
        self.assertRaises(ValueError, man.order_col, entries, indexes)

    def test_get_ordered_indexes_asc(self):
        entries = ['c', 'e', 'd', 'a', 'b']
        expected = [3, 4, 0, 2, 1]
        test = man.get_sorted_indexes(entries, True)
        self.assertEqual(test, expected)

    def test_get_ordered_indexes_dsc(self):
        entries = ['c', 'e', 'd', 'a', 'b']
        expected = [1, 2, 0, 4, 3]
        test = man.get_sorted_indexes(entries, False)
        self.assertEqual(test, expected)

    def test_unite_tables_with_repeat(self):
        expected = [('a', 1, 0.1), ('b', 2, 0.2), ('c', 3, 0.3), ('d', 4, 0.4),
                    ('e', 5, 0.5), ('a', 1, 0.1), ('b', 2, 0.2), ('c', 3, 0.3),
                    ('i', 9, 0.9), ('j', 10, 1.0)]
        test = man.unite_tables(self.tb51, self.tb52,
                                self.tb51_order, self.tb52_order, True)
        test_tb = test[0]
        # Check column entries, row order may be different, but change is
        # uniform across all columns
        str_col = test_tb['str']
        int_col = test_tb['int']
        float_col = test_tb['float']
        i = str_col.index('a')
        j = str_col.index('b')
        k = str_col.index('c')
        l = str_col.index('d')
        m = str_col.index('e')
        n = str_col.index('i')
        o = str_col.index('j')
        # Same row as a
        self.assertEqual(int_col[i], 1)
        self.assertEqual(float_col[i], 0.1)
        # Same row as b
        self.assertEqual(int_col[j], 2)
        self.assertEqual(float_col[j], 0.2)
        # Same row as c
        self.assertEqual(int_col[k], 3)
        self.assertEqual(float_col[k], 0.3)
        # Same row as d
        self.assertEqual(int_col[l], 4)
        self.assertEqual(float_col[l], 0.4)
        # Same row as e
        self.assertEqual(int_col[m], 5)
        self.assertEqual(float_col[m], 0.5)
        # Same row as n
        self.assertEqual(int_col[n], 9)
        self.assertEqual(float_col[n], 0.9)
        # Same row as o
        self.assertEqual(int_col[o], 10)
        self.assertEqual(float_col[o], 1.0)
        # Count that there are repeats
        counter_str = col.Counter(str_col)
        self.assertEqual(counter_str['a'], 2)
        self.assertEqual(counter_str['b'], 2)
        self.assertEqual(counter_str['c'], 2)
        counter_int = col.Counter(int_col)
        self.assertEqual(counter_int[1], 2)
        self.assertEqual(counter_int[2], 2)
        self.assertEqual(counter_int[3], 2)
        counter_float = col.Counter(float_col)
        self.assertEqual(counter_float[0.1], 2)
        self.assertEqual(counter_float[0.2], 2)
        self.assertEqual(counter_float[0.3], 2)

    def test_unite_tables_no_repeat(self):
        expected = [('a', 1, 0.1), ('b', 2, 0.2), ('c', 3, 0.3), ('d', 4, 0.4),
                    ('e', 5, 0.5), ('i', 9, 0.9), ('j', 10, 1.0)]
        test = man.unite_tables(self.tb51, self.tb52,
                                self.tb51_order, self.tb52_order, False)
        test_tb = test[0]
        # Check column entries, row order may be different, but change is
        # uniform across all columns
        str_col = test_tb['str']
        int_col = test_tb['int']
        float_col = test_tb['float']
        i = str_col.index('a')
        j = str_col.index('b')
        k = str_col.index('c')
        l = str_col.index('d')
        m = str_col.index('e')
        n = str_col.index('i')
        o = str_col.index('j')
        # Same row as a
        self.assertEqual(int_col[i], 1)
        self.assertEqual(float_col[i], 0.1)
        # Same row as b
        self.assertEqual(int_col[j], 2)
        self.assertEqual(float_col[j], 0.2)
        # Same row as c
        self.assertEqual(int_col[k], 3)
        self.assertEqual(float_col[k], 0.3)
        # Same row as d
        self.assertEqual(int_col[l], 4)
        self.assertEqual(float_col[l], 0.4)
        # Same row as e
        self.assertEqual(int_col[m], 5)
        self.assertEqual(float_col[m], 0.5)
        # Same row as n
        self.assertEqual(int_col[n], 9)
        self.assertEqual(float_col[n], 0.9)
        # Same row as o
        self.assertEqual(int_col[o], 10)
        self.assertEqual(float_col[o], 1.0)

    def test_unite_tables_unequal_columns_raise_error(self):
        tb_with_col_removed = self.tb52
        del tb_with_col_removed['str']
        self.assertRaises(hpr.InvalidQueryError, man.unite_tables,
                          self.tb51, tb_with_col_removed,
                          self.tb51_order, self.tb52_order, False)

    def test_unite_tables_unequal_type_raise_error(self):
        tb_with_different_typed_column_values = self.tb52
        tb_with_different_typed_column_values['str'] = self.col53_float
        self.assertRaises(hpr.InvalidQueryError, man.unite_tables,
                          self.tb51, tb_with_different_typed_column_values,
                          self.tb51_order, self.tb52_order, False)

    def test_intersect_tables_unequal_columns_raise_error(self):
        tb_with_col_removed = self.tb52
        del tb_with_col_removed['str']
        self.assertRaises(hpr.InvalidQueryError, man.intersect_tables,
                          self.tb51, tb_with_col_removed,
                          self.tb51_order, self.tb52_order)

    def test_intersect_tables_unequal_type_raise_error(self):
        tb_with_different_typed_column_values = self.tb52
        tb_with_different_typed_column_values['str'] = self.col53_float
        self.assertRaises(hpr.InvalidQueryError, man.intersect_tables,
                          self.tb51, tb_with_different_typed_column_values,
                          self.tb51_order, self.tb52_order)

    def test_intersect_tables(self):
        test = man.intersect_tables(self.tb51, self.tb52,
                                    self.tb51_order, self.tb52_order)
        test_tb = test[0]
        # Check column entries, row order may be different, but change is
        # uniform across all columns
        str_col = test_tb['str']
        int_col = test_tb['int']
        float_col = test_tb['float']
        i = str_col.index('a')
        j = str_col.index('b')
        k = str_col.index('c')
        # Same row as a
        self.assertEqual(int_col[i], 1)
        self.assertEqual(float_col[i], 0.1)
        # Same row as b
        self.assertEqual(int_col[j], 2)
        self.assertEqual(float_col[j], 0.2)
        # Same row as c
        self.assertEqual(int_col[k], 3)
        self.assertEqual(float_col[k], 0.3)

    def test_intersect_tables_no_intersect(self):
        no_intersect = {'str': ['z'], 'int': [100], 'float': [0.05]}
        test = man.intersect_tables(self.tb51, no_intersect,
                                    self.tb51_order, self.tb52_order)
        self.assertEqual(set(test[0]), set())

    def test_left_intersect_tables_unequal_columns_raise_error(self):
        tb_with_col_removed = self.tb52
        del tb_with_col_removed['str']
        self.assertRaises(hpr.InvalidQueryError, man.left_outer_intersect,
                          self.tb51, tb_with_col_removed,
                          self.tb51_order, self.tb52_order)

    def test_left_intersect_tables_unequal_type_raise_error(self):
        tb_with_different_typed_column_values = self.tb52
        tb_with_different_typed_column_values['str'] = self.col53_float
        self.assertRaises(hpr.InvalidQueryError, man.left_outer_intersect,
                          self.tb51, tb_with_different_typed_column_values,
                          self.tb51_order, self.tb52_order)

    def test_left_outer_intersect(self):
        expected = {'str': ['d', 'e'],
                    'int': [4, 5],
                    'float': [0.4, 0.5]}
        test = man.left_outer_intersect(self.tb51, self.tb52,
                                        self.tb51_order, self.tb52_order)
        test_tb = test[0]
        # Check column entries, row order may be different, but change is
        # uniform across all columns
        str_col = test_tb['str']
        int_col = test_tb['int']
        float_col = test_tb['float']
        i = str_col.index('d')
        j = str_col.index('e')
        # Same row as d
        self.assertEqual(int_col[i], 4)
        self.assertEqual(float_col[i], 0.4)
        # Same row as e
        self.assertEqual(int_col[j], 5)
        self.assertEqual(float_col[j], 0.5)

    def test_left_outer_intersect_no_intersect(self):
        all_intersect = self.tb52
        all_intersect['str'].extend(['d', 'e'])
        all_intersect['int'].extend([4, 5])
        all_intersect['float'].extend([0.4, 0.5])
        test = man.left_outer_intersect(self.tb51, all_intersect,
                                        self.tb51_order, self.tb52_order)
        self.assertEqual(test[0], {})

    def test_convert_rows_to_tb(self):
        rows = [('a', 1, 0.1), ('b', 2, 0.2), ('c', 3, 0.3), ('d', 4, 0.4),
                ('e', 5, 0.5)]
        expected = self.tb51
        test = man.rows_to_tb(rows, self.tb51_order)
        self.assertEqual(test, expected)


man_suite = unittest.TestLoader().loadTestsFromTestCase(TestManipulation)
unittest.TextTestRunner().run(man_suite)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestManipulation())
    return suite
