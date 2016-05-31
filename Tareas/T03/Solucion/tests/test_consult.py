import unittest
import consult
import database as db
import manipulation as man
import random as rand
import helper as hpr
from tests import test_queries as tquery
import collections as col


class TestConsult(unittest.TestCase):
    def setUp(self):
        # Simple expression
        self.e1 = 'EMPRESTA Persona, AnoNac DE personas;'
        # Long expression
        self.e2 = 'EMPRESTA AnoNac DE personas ' \
                  'ONDE (AnoNac < 1995) ' \
                  'ORDENATELOS X AnoNac PA RIBA;'
        # Expression with all keywords
        self.e3 = '(EMPRESTA AnoNac DE personas ' \
                  'ONDE (AnoNac < 1995) ' \
                  'ORDENATELOS X AnoNac PA RIBA) ' \
                  'UNETELO CN ' \
                  '(EMPRESTA AnoNac DE personas ' \
                  'ONDE (AnoNac > 1990));'
        # Testing conditional expressions
        # Comparators
        # '=' 'O'
        self.e4 = 'EMPRESTA Persona,AnoNac,Sexo DE personas ' \
                  'ONDE (Persona = 10046101) O (Persona = 10002004);'
        # '<' '>='
        self.e5 = 'EMPRESTA Persona,AnoNac,Sexo DE personas ' \
                  'ONDE (Persona < 10004101) Y (Persona >= 10002004);'
        # '>' '!='
        self.e6 = 'EMPRESTA Id, Comuna DE comunas ' \
                  'ONDE (Id > 337) Y (Comuna != "PADRE HURTADO");'
        # 'Y' '<=''PARECIO A'
        self.e7 = 'EMPRESTA Id,Comuna DE comunas ' \
                  'ONDE (Id <= 19) Y (Comuna PARECIO A "C");'
        # Set up files for test queries, test_tb is a dictionary
        tname1, tb1 = db.read_table('personas.csv')
        self.personas_tb = {tname1: tb1}
        tname2, tb2 = db.read_table('comunas.csv')
        self.comunas_tb = {tname2: tb2}
        tname3, tb3 = db.read_table("src/pokemon.csv")
        self.pokemon_tb = {tname3[4:]: tb3}
        tname4, tb4 = db.read_table('src/poke_estadisticas.csv')
        self.poke_estad_tb = {tname4[4:]: tb4}
        tname5, tb5 = db.read_table('src/estadisticas.csv')
        self.estad_tb = {tname5[4:]: tb5}
        tname6, tb6 = db.read_table('src/encuentros.csv')
        self.encuentros_tb = {tname6[4:]: tb6}
        self.tables = {}
        self.tables.update(self.personas_tb)
        self.tables.update(self.comunas_tb)
        self.tables.update(self.pokemon_tb)
        self.tables.update(self.poke_estad_tb)
        self.tables.update(self.estad_tb)
        self.tables.update(self.encuentros_tb)
        # set up testing column
        self.col1_name = 'col1'
        self.col1_vals = [i for i in range(100, 200)]
        self.col2_name = 'col2'
        self.col2_vals = [i for i in range(150, 250)]
        self.col3_name = 'col3'
        self.col3_vals = [str(i) + str(i + 1) for i in range(0, 10000)]
        # set up tables for testing ORDENATELOS and SOLO
        self.per_col = [10001001, 10001002, 10001003, 10002001, 10002002,
                        10002003, 10002004, 10002005, 10003001]
        self.nac_col = [1958, 1956, 1982, 1954, 1961, 1977, 1981, 1995, 1933]
        self.sex_col = [1, 2, 2, 1, 2, 1, 1, 1, 1]
        self.unordered_tb = {'Persona': self.per_col,
                             'AnoNac': self.nac_col,
                             'Sexo': self.sex_col}
        # Set up tables for testing join query results
        self.jcol1 = ['a', 'b', 'c']
        self.jcol2 = ['b', 'c', 'd']
        self.jcol3 = ['c', 'd', 'e']
        self.jtb1 = {'col1': self.jcol1}
        self.jtb2 = {'col1': self.jcol2}
        self.jtb3 = {'col1': self.jcol3}
        # Set up tables for testing get grouping
        self.gcol1 = ['a', 'b', 'a', 'c', 'c', 'b']
        self.gtb1 = {'col1': self.gcol1}
        # Set up tables for testing do_col_func
        self.dcol1 = ['a', 'a', 'b', 'b', 'c', 'c']
        self.dcol2 = [1, 3, 2, 4, 5, 7]
        self.dtb1 = {'col1': self.dcol1, 'col2': self.dcol2}

    def test_query_with_conditional_comparators(self):
        exp_e4 = ['10002004 | 1981 | 1',
                  '10046101 | 1950 | 1']
        t_e4 = man.printable(consult.raw_query(self.e4, self.personas_tb))
        for s in exp_e4:
            self.assertIn(s, t_e4, '\nRaw query failed: \n'
                          'Expected:\n{0}\n'
                          'Test:\n{1}'.format(exp_e4, t_e4))
        exp_e5 = ['10003001 | 1933 | 1',
                  '10002004 | 1981 | 1',
                  '10002005 | 1995 | 1']
        t_e5 = man.printable(consult.raw_query(self.e5, self.personas_tb))
        for s in exp_e5:
            self.assertIn(s, t_e5, '\nRaw query failed: \n'
                          'Expected:\n{0}\n'
                          'Test:\n{1}'.format(exp_e5, t_e5))
        exp_e6 = ['338 | EL BOSQUE', '998 | NO ESPECIFICA']
        t_e6 = man.printable(consult.raw_query(self.e6, self.comunas_tb))
        for s in exp_e6:
            self.assertIn(s, t_e6, '\nRaw query failed: \n'
                          'Expected:\n{0}\n'
                          'Test:\n{1}'.format(exp_e6, t_e6))
        exp_e7 = ['10 | CALAMA', '13 | COPIAPO']
        t_e7 = man.printable(consult.raw_query(self.e7, self.comunas_tb))
        for s in exp_e7:
            self.assertIn(s, t_e7, '\nRaw query on e5 failed: \n'
                         'Expected:\n{0}\n'
                         'Test:\n{1}'.format(exp_e7, t_e7))

# ------------------------ TESTING QUERIES ------------------------------------#
    def test_query_one(self):
        test = list(consult.raw_query(tquery.query1, self.tables))[:15]
        test_rows = [row[0] for row in test]
        # Check the first 15 rows
        self.assertEqual(test_rows, tquery.query1_res)

    def test_query_two(self):
        test = list(consult.raw_query(tquery.query2, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(test_rows, tquery.query2_res)

    def test_query_three(self):
        test = list(consult.raw_query(tquery.query3, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(test_rows, tquery.query3_res)

    def test_query_four(self):
        test = list(consult.raw_query(tquery.query4, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(test_rows, tquery.query4_res)

    def test_query_five(self):
        test = list(consult.raw_query(tquery.query5, self.tables))[:15]
        test_rows = [row[0] for row in test]
        self.assertEqual(test_rows, tquery.query5_res)

    def test_query_six(self):
        test = list(consult.raw_query(tquery.query6, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(test_rows, tquery.query6_res)

    def test_query_seven(self):
        test = list(consult.raw_query(tquery.query7, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(set(test_rows), set(tquery.query7_res))

    def test_query_eight(self):
        test = list(consult.raw_query(tquery.query8, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(set(test_rows), set(tquery.query8_res))

    def test_query_nine(self):
        test = list(consult.raw_query(tquery.query9, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(set(test_rows), set(tquery.query9_res))

    def test_query_extra(self):
        query = 'EMPRESTA estadistica_nombre DE estadisticas;'
        test = list(consult.raw_query(query, self.tables))
        self.assertIsNotNone(test)

    def test_query_extra_two(self):
        query = 'EMPRESTA pokemon_id DE pokemon ONDE ' \
                '(EXISTE (EMPRESTA estadistica_nombre DE estadisticas));'
        test = list(consult.raw_query(query, self.tables))
        self.assertIsNotNone(test)

    def test_query_ten(self):
        test = list(consult.raw_query(tquery.query10, self.tables))
        test_rows = [row[0] for row in test]
        self.assertEqual(set(test_rows), set(tquery.query10_res))
# -----------------------------------------------------------------------------#

    def query_result_A(self):
        # Generates a fake query result
        col1_entries = [i for i in range(0, 1000)]
        col2_entries = [chr(i) for i in range(0, 1000)]
        return {'num_A': col1_entries, 'str_A': col2_entries}

    def query_result_B(self):
        # Generates a fake query result
        col1_entries = [i for i in range(1000, 0, -1)]
        col2_entries = [chr(i) for i in range(1000, 0, -1)]
        return {'num_B': col1_entries, 'str_B': col2_entries}

    def test_union_two_query_results(self):
        query_a = self.query_result_A()
        query_b = self.query_result_B()
        results = (query_a, query_b)
        # Convert to a list for testing
        test = list(consult.unite_tables(results))
        # Check number of rows
        expected_len = len(query_a['num_A']) + len(query_a['str_A']) + \
                       len(query_b['num_B']) + len(query_b['str_B'])
        self.assertEqual(len(test), expected_len)
        # Check that the test result has all the entries
        query_A_not_in_test = list(filter(lambda x: x not in test,
                                          query_a['num_A'] + query_a['str_A']))
        query_B_not_in_test = list(filter(lambda x: x not in test,
                                          query_b['num_B'] + query_b['str_B']))
        # ALl entries in query A should be in test
        self.assertEqual(len(query_A_not_in_test), 0)
        # ALl entries in query B should be in test
        self.assertEqual(len(query_B_not_in_test), 0)

    def test_interval_for_emp_de_exprn(self):
        # Strip ';' from expression
        self.e1 = self.e1.strip(';')
        # E: 0, _D: 24 and last char is 36
        expected = [(0, self.e1.index(' D')), (self.e1.index(' D'), 36)]
        test = consult.get_exprn_intervals(self.e1)
        self.assertEqual(test, expected,
                         'Split interval failed: '
                         '\n(expected) {0} \n(test) {1}'.format(expected, test))

    def test_interval_for_long_exprn(self):
        # Strip ';' from expression
        self.e2 = self.e2.strip(';')
        expected = [(0, 15), (15, 27), (27, 48), (48, 77)]
        test = consult.get_exprn_intervals(self.e2)
        self.assertEqual(test, expected,
                         'Split interval failed: '
                         '\n(expected) {0} \n(test) {1}'.format(expected, test))

    def test_pass_valid_exprn(self):
        test = consult.check_query(self.e1)
        self.assertTrue(test)

    def test_fail_invalid_exprn(self):
        # None case
        self.assertRaises(ValueError, consult.check_query, None)
        # Invalid query case
        invalid1 = 'EMPRESTA Persona De personas;'
        self.assertRaises(ValueError, consult.check_query, invalid1)
        # Invalid query without DE
        invalid2 = 'EMPRESTA Persona personas;'
        self.assertRaises(ValueError, consult.check_query, invalid2)

    def test_emp_without_col_funcs(self):
        query = 'EMPRESTA Persona, AnoNac, Sexo'
        cols, col_func = consult.emp(query)
        expected_cols = ['Persona', 'AnoNac', 'Sexo']
        expected_func = {'DIVERGENTE': False}
        self.assertEqual(expected_cols, cols)
        self.assertEqual(expected_func, col_func)

    def test_emp_with_divergente(self):
        query = 'EMPRESTA DIVERGENTE pokemon_nombre'
        cols, col_func = consult.emp(query)
        expected_cols = ['pokemon_nombre']
        expected_func = {'DIVERGENTE': True}
        self.assertEqual(expected_cols, cols)
        self.assertEqual(expected_func, col_func)

    def test_emp_with_col_func(self):
        query = 'EMPRESTA MIN(pokemon_experiencia_base), CONTEA(nombre)'
        cols, col_func = consult.emp(query)
        expected_cols = ['pokemon_experiencia_base', 'nombre']
        expected_func = {'DIVERGENTE': False,
                         'pokemon_experiencia_base': 'MIN',
                         'nombre': 'CONTEA'}
        self.assertEqual(expected_cols, cols)
        self.assertEqual(expected_func, col_func)

    def test_emp_de(self):
        tables = [self.personas_tb['personas'], self.comunas_tb['comunas']]
        cols = ['Persona', 'Id']
        # the new size will be len(Persona) * len(Id)
        expected_size = len(self.personas_tb['personas']['Persona']) * \
            len(self.comunas_tb['comunas']['Id'])
        test = consult.emp_de_two(tables, cols, {})
        # Check that the test table has the columns
        self.assertIsNotNone(test.get('Persona', None))
        self.assertIsNotNone(test.get('Id', None))
        # Check that the test table only has two columns
        self.assertEqual(len(test.keys()), 2)
        # check the size of the columns
        self.assertEqual(len(list(test.get('Persona', None))), expected_size)

    def test_filter_by_val_lteq(self):
        # less than or equal to 110
        lt = 110
        test = consult.filter_by_val(self.col1_name, self.col1_vals, '<=', lt)
        expected = [i for i in range(0, 11)]
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_gteq(self):
        # greater than or equal to 190
        gt = 190
        test = consult.filter_by_val(self.col1_name, self.col1_vals, '>=', gt)
        expected = [i for i in range(90, 100)]
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_neq(self):
        # not equal 105
        neq = 105
        test = consult.filter_by_val(self.col1_name, self.col1_vals, '!=', neq)
        expected = [i for i in range(0, 100)]
        expected.pop(5)
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_eq(self):
        # equal 125
        eq = 125
        test = consult.filter_by_val(self.col1_name, self.col1_vals, '=', eq)
        expected = [25]
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_lt(self):
        # less than 10
        lt = 110
        test = consult.filter_by_val(self.col1_name, self.col1_vals, '<', lt)
        expected = [i for i in range(0, 10)]
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_gt(self):
        # greater than 10
        gt = 190
        test = consult.filter_by_val(self.col1_name, self.col1_vals,
                                     '>', gt)
        expected = [i for i in range(91, 100)]
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_val_like(self):
        # like
        like = 'Hello'
        num = 30
        expected = []
        # Add like words into list
        list_len = len(self.col3_vals)
        start_index = rand.randint(0, list_len)
        for i in range(0, num):
            word = ''
            if i % 2 == 0:
                word = like
            else:
                word = str(i) + like + str(i + 2)
            index = start_index + i*i
            expected.append(index)
            self.col3_vals.insert(index, word)
        test = consult.filter_by_val(self.col3_name, self.col3_vals,
                                     'PARECIO A', like)
        self.assertEqual(test[self.col3_name], expected)

    def test_filter_by_val_list(self):
        expected = [i for i in range(50, 100)]
        test = consult.filter_by_val_list(self.col1_name, self.col1_vals,
                                          self.col2_vals)
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_empty_val_list(self):
        expected = []
        test = consult.filter_by_val_list(self.col1_name, self.col1_vals, [])
        self.assertEqual(test[self.col1_name], expected)

    def test_filter_by_col(self):
        expected_col1 = [i for i in range(50, 100)]
        expected_col2 = [i for i in range(0, 50)]
        test = consult.filter_by_col(self.col1_name, self.col1_vals,
                                     self.col2_name, self.col2_vals)
        self.assertEqual(test[self.col1_name], expected_col1)
        self.assertEqual(test[self.col2_name], expected_col2)

    def test_filter_by_col_range(self):
        expected = [i for i in range(10, 20)]
        range_start = 109
        range_end = 120
        test = consult.filter_by_range(self.col1_name, self.col1_vals,
                                       range_start, range_end)
        self.assertEqual(test[self.col1_name], expected)

    def test_split_clauses(self):
        cond1 = 'pokemon_id = poke_estadisticas_pokemon_id'
        e1 = ('pokemon_id', '=', 'poke_estadisticas_pokemon_id')
        t1 = consult.split_clauses(cond1)
        self.assertEqual(t1[0], e1[0])
        self.assertEqual(t1[1], e1[1])
        self.assertEqual(t1[2], e1[2])
        cond2 = 'encuentro_min ENTRE (30 Y 60)'
        e2 = ('encuentro_min', 'ENTRE', '(30 Y 60)')
        t2 = consult.split_clauses(cond2)
        self.assertEqual(t2[0], e2[0])
        self.assertEqual(t2[1], e2[1])
        self.assertEqual(t2[2], e2[2])
        cond4 = "pokemon_nombre PARECIO A 'mega'"
        e4 = ('pokemon_nombre', 'PARECIO A', "'mega'")
        t4 = consult.split_clauses(cond4)
        self.assertEqual(t4[0], e4[0])
        self.assertEqual(t4[1], e4[1])
        self.assertEqual(t4[2], e4[2])
        '''
        cond3 = 'EXISTE (EMPRESTA estadistica_nombre DE estadisticas)'
        e3 = True
        t3 = consult.split_clauses(cond3)
        self.assertEqual(t3, e3)
        '''

    def test_eval_cond_val(self):
        tb = self.pokemon_tb['pokemon']
        cond1 = 'pokemon_id_especie <= 151'
        col1 = tb['pokemon_id_especie']
        expected1 = [index for index, val in enumerate(col1) if val <= 151]
        test1 = consult.eval_cond(cond1, self.tables)
        test_col_entries1 = test1['pokemon']
        self.assertEqual(test_col_entries1, expected1)
        # Testing for string condition
        cond2 = "pokemon_nombre PARECIO A 'mega'"
        col2 = tb['pokemon_nombre']
        expected2 = [index for index, val in enumerate(col2) if 'mega' in val]
        test2 = consult.eval_cond(cond2, self.tables)
        test_col_entries2 = test2['pokemon']
        self.assertEqual(test_col_entries2, expected2)

    def test_eval_cond_range(self):
        cond = 'pokemon_experiencia_base ENTRE (100 Y 150)'
        tb = self.pokemon_tb['pokemon']
        col = tb['pokemon_experiencia_base']
        expected = [index for index, val in enumerate(col)
                    if not (val <= 100 or val >= 150)]
        test = consult.eval_cond(cond, self.tables)
        test_col_entries = test['pokemon']
        self.assertEqual(test_col_entries, expected)

    def test_eval_cond_col_to_col(self):
        cond = 'pokemon_id = poke_estadisticas_pokemon_id'
        estad_tb = self.poke_estad_tb['poke_estadisticas']
        poke_tb = self.pokemon_tb['pokemon']
        poke_col = poke_tb['pokemon_id']
        estad_col = estad_tb['poke_estadisticas_pokemon_id']
        expected_poke = [index for index, val in enumerate(poke_col)
                         if val in estad_col]
        expected_estad = [index for index, val in enumerate(estad_col)
                          if val in poke_col]
        test = consult.eval_cond(cond, self.tables)
        test_poke = test['pokemon']
        test_estad = test['poke_estadisticas']
        self.assertEqual(test_poke, expected_poke)
        self.assertEqual(test_estad, expected_estad)

    def test_eval_cond_exist_cond(self):
        cond = 'EXISTE (EMPRESTA estadistica_nombre DE estadisticas)'
        self.assertTrue(consult.eval_cond(cond, self.tables))

    def test_eval_cond_inner_query(self):
        cond = 'pokemon_id EN ' \
               '(EMPRESTA pokemon_id DE pokemon ONDE (pokemon_id != 2))'
        poke_tb = self.pokemon_tb['pokemon']
        poke_col = poke_tb['pokemon_id']
        not_two = list(filter(lambda x: x != 2, poke_col))
        expected_poke = [index for index, val in enumerate(poke_col)
                         if val in not_two]
        test = consult.eval_cond(cond, self.tables)
        test_poke = test['pokemon']
        self.assertEqual(test_poke, expected_poke)

    def test_existe_cond_True(self):
        cond = 'EMPRESTA estadistica_nombre DE estadisticas'
        test = consult.exist_condition(cond, self.tables)
        self.assertTrue(test)

    def test_existe_cond_False(self):
        cond = 'EMPRESTA pokemon_nombre DE estadisticas'
        test = consult.exist_condition(cond, self.tables)
        self.assertFalse(test)

    def test_query_by_neq(self):
        cond = 'EMPRESTA pokemon_id DE pokemon ONDE (pokemon_id != 2)'
        result_tb, col_order = consult.atomic_query(cond, self.tables)
        test_col = list(result_tb['pokemon_id'])
        self.assertNotIn(2, test_col)

    def test_filter_by_neq(self):
        poke_tb = self.pokemon_tb['pokemon']
        poke_col = poke_tb['pokemon_id']
        test = consult.filter_by_val('pokemon', poke_col, '!=', 2)
        test_col = test['pokemon']
        # pokemon_id 2 is at index 1, since it goes 0, 1, 2...
        self.assertNotIn(1, test_col)

    def test_eval_cond_neq(self):
        cond = 'pokemon_id != 2'
        test = consult.eval_cond(cond, self.tables)
        test_col = test['pokemon']
        # pokemon_id 2 is at index 1, since it goes 0, 1, 2...
        self.assertNotIn(1, test_col)

    def test_eval_onde_neq(self):
        cond = 'pokemon_id != 2'
        test = consult.eval_onde(cond, self.tables)
        test_col = test['pokemon']['pokemon_id']
        self.assertNotIn(2, test_col)

    def test_filter_by_query(self):
        cond = 'EMPRESTA pokemon_id DE pokemon ONDE (pokemon_id != 2)'
        poke_tb = self.pokemon_tb['pokemon']
        poke_col = poke_tb['pokemon_id']
        not_two = list(filter(lambda x: x != 2, poke_col))
        expected_poke = [index for index, val in enumerate(poke_col)
                         if val in not_two]
        test = consult.filter_by_query('pokemon', 'pokemon_id', poke_col,
                                       cond, self.tables)
        test_poke = test['pokemon']
        self.assertEqual(test_poke, expected_poke)

    def test_filter_by_invalid_query_throw_error(self):
        cond = 'EMPRESTA estadistica_nombre DE estadisticas'
        poke_tb = self.pokemon_tb['pokemon']
        poke_col = poke_tb['pokemon_id']
        self.assertRaises(hpr.InvalidQueryError,
                          consult.filter_by_query,
                          'pokemon', 'pokemon_id', poke_col, cond, self.tables)

    def test_ordenar(self):
        self.per_exp = [10003001, 10002001, 10001002, 10001001, 10002002,
                        10002003, 10002004, 10001003, 10002005]
        self.nac_exp = [1933, 1954, 1956, 1958, 1961, 1977, 1981, 1982, 1995]
        self.sex_exp = [1, 1, 2, 1, 2, 1, 1, 2, 1]
        line = 'AnoNac PA RIBA'
        test = consult.order_cols(line, [self.unordered_tb])[0]
        self.assertEqual(test['AnoNac'], self.nac_exp)
        self.assertEqual(test['Persona'], self.per_exp)
        self.assertEqual(test['Sexo'], self.sex_exp)

    def test_cut_off_cols(self):
        self.per_exp = [10001001, 10001002, 10001003, 10002001, 10002002]
        self.nac_exp = [1958, 1956, 1982, 1954, 1961]
        self.sex_exp = [1, 2, 2, 1, 2]
        line = ' 5 '
        test = consult.cutoff_rows(line, self.unordered_tb)
        self.assertEqual(test['Persona'], self.per_exp)
        self.assertEqual(test['AnoNac'], self.nac_exp)
        self.assertEqual(test['Sexo'], self.sex_exp)

    def test_cut_off_cols_raise_error_if_cannot_parse_line(self):
        line = ' invalid '
        self.assertRaises(hpr.InvalidQueryError, consult.cutoff_rows,
                          line, self.unordered_tb)

    def test_unite_three_tables_no_repeats(self):
        results = [(self.jtb1, ['col1']), (self.jtb2, ['col1']),
                   (self.jtb3, ['col1'])]
        joins = [' UNETELO CN ', ' UNETELO CN ']
        test = consult.join_query_res(results, joins)
        test_tb = test[0]
        # Check for repeats
        test_col = test_tb['col1']
        counter = col.Counter(test_col)
        self.assertEqual(counter['a'], 1)
        self.assertEqual(counter['b'], 1)
        self.assertEqual(counter['c'], 1)
        self.assertEqual(counter['d'], 1)
        self.assertEqual(counter['e'], 1)

    def test_unite_three_tables_with_repeats(self):
        results = [(self.jtb1, ['col1']), (self.jtb2, ['col1']),
                   (self.jtb3, ['col1'])]
        joins = [' UNETELO TODO CN ', ' UNETELO TODO CN ']
        test = consult.join_query_res(results, joins)
        test_tb = test[0]
        # Check for repeats
        test_col = test_tb['col1']
        counter = col.Counter(test_col)
        self.assertEqual(counter['a'], 1)
        self.assertEqual(counter['b'], 2)
        self.assertEqual(counter['c'], 3)
        self.assertEqual(counter['d'], 2)
        self.assertEqual(counter['e'], 1)

    def test_unite_three_tables_intersect(self):
        results = [(self.jtb1, ['col1']), (self.jtb2, ['col1']),
                   (self.jtb3, ['col1'])]
        joins = [' COMUN CN ', ' COMUN CN ']
        test = consult.join_query_res(results, joins)
        test_tb = test[0]
        # Check for repeats
        test_col = test_tb['col1']
        counter = col.Counter(test_col)
        self.assertEqual(counter['a'], 0)
        self.assertEqual(counter['b'], 0)
        self.assertEqual(counter['c'], 1)
        self.assertEqual(counter['d'], 0)
        self.assertEqual(counter['e'], 0)

    def test_unite_then_intersect_tables(self):
        results = [(self.jtb1, ['col1']), (self.jtb2, ['col1']),
                   (self.jtb3, ['col1'])]
        joins = [' UNETELO TODO CN ', ' COMUN CN ']
        test = consult.join_query_res(results, joins)
        test_tb = test[0]
        # Check for repeats
        test_col = test_tb['col1']
        counter = col.Counter(test_col)
        self.assertEqual(counter['a'], 0)
        self.assertEqual(counter['b'], 0)
        self.assertEqual(counter['c'], 1)
        self.assertEqual(counter['d'], 1)
        self.assertEqual(counter['e'], 0)

    def test_get_grouping(self):
        expected = [[0, 2], [1, 5], [3, 4]]
        test = consult.get_grouping('col1', self.gtb1)
        self.assertIn(expected[0], test)
        self.assertIn(expected[1], test)
        self.assertIn(expected[2], test)

    def test_get_grouping_no_col_raise_error(self):
        self.assertRaises(hpr.InvalidQueryError, consult.get_grouping,
                          'col2', self.gtb1)

    def test_do_col_func_with_grouping(self):
        # The averages of col2 which are integers
        expected = [2, 3, 6]
        # grouping is done by col1, which are letters
        # grp1: a, grp2: b, grp3: c
        grouping = [[0, 1], [2, 3], [4, 5]]
        col_func = {'col2': 'PROMEDIO'}
        test = consult.do_col_funcs_two(self.dtb1, col_func, grouping)
        # Assert 2 columns
        self.assertEqual(len(list(test.keys())), 2)
        # Assert col1
        counter = col.Counter(test['col1'])
        self.assertEqual(counter['a'], 1)
        self.assertEqual(counter['b'], 1)
        self.assertEqual(counter['c'], 1)
        self.assertEqual(set(test['col1']), {'a', 'b', 'c'})
        # Assert col2
        self.assertEqual(test['col2'], expected)

    def test_filter_grouping_min(self):
        # Only two of the three groupings meets condition
        expected = [[2, 3], [4, 5]]
        cond = 'MIN(col2) >= 2'
        grouping = [[0, 1], [2, 3], [4, 5]]
        test = consult.filter_grps(cond, self.dtb1, grouping)
        # Assert that there are two groupings
        self.assertEqual(len(test), 2)
        self.assertEqual(test, expected)

    def test_filter_grouping_average(self):
        # Only one of the three groupings meets condition
        expected = [[0, 1]]
        cond = 'PROMEDIO(col2) < 3'
        grouping = [[0, 1], [2, 3], [4, 5]]
        test = consult.filter_grps(cond, self.dtb1, grouping)
        # Assert that there are two groupings
        self.assertEqual(len(test), 1)
        self.assertEqual(test, expected)

consult_suite = unittest.TestLoader().loadTestsFromTestCase(TestConsult)
unittest.TextTestRunner().run(consult_suite)


if __name__ == '__main__':
    # unittest.main()
    pass
