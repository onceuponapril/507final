import unittest
from fn import *

#
class TestDatabase(unittest.TestCase):

    def test_eat_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = 'SELECT City FROM EAT'
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertIn(('Ann Arbor',), result_list)
        self.assertEqual(len(result_list), )

        sql = '''
            SELECT Price,Rating,Address
            FROM EAT
            WHERE Name="TK WU"
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(result_list[0][3], )
        self.assertEqual(result_list[0][3], 4.0)

        conn.close()

    def test_ride_table(self):
        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        sql = '''
            SELECT Destination_geo
            FROM RIDE
            WHERE Destination="TK WU"
        '''
        result = cur.execute(sql).fetchall()
        self.assertEqual(result, )



#         conn.close()
#
#     def test_joins(self):
#         conn = sqlite3.connect(DBNAME)
#         cur = conn.cursor()
#
#         sql = '''
#             SELECT Alpha2
#             FROM Bars
#                 JOIN Countries
#                 ON Bars.CompanyLocationId=Countries.Id
#             WHERE SpecificBeanBarName="Hacienda Victoria"
#                 AND Company="Arete"
#         '''
#         results = cur.execute(sql)
#         result_list = results.fetchall()
#         self.assertIn(('US',), result_list)
#         conn.close()

class TestAccessData(unittest.TestCase):

    def test_google_lyft(self):
        resultA=google_map('North Quad,Ann Arbor')
        resultB=google_map('TK WU,Ann Arbor')

        self.assertEqual(results[0], )
        self.assertEqual(results[1], )
        lyft_result=estmate_cost(resultA,resultB)
        self.assertEqual(lyft_result['es_time'], )
        self.assertEqual(lyft_result['es_distance'], )
        self.assertEqual(lyft_result['es_cost_max'], )
        self.assertEqual(lyft_result['es_cost_min'], )


    def test_yelp_data(self):
        yelpdt=Yelpeat('Ann Arbor')
        results=yelpdt.scrape_data()
        self.assertEqual(results[0][name], )
        self.assertEqual(results[0][rating], )
        self.assertEqual(results[0][address], )
        self.assertEqual(results[0][price], )


class TestStoreData(unittest.TestCase):


    def test_company_search(self):
        results = process_command('companies region=Europe ratings top=5')
        self.assertEqual(results[1][0], 'Idilio (Felchlin)')

        results = process_command('companies country=US bars_sold top=5')
        self.assertTrue(results[0][0] == 'Fresco' and results[0][2] == 26)

        results = process_command('companies cocoa top=5')
        self.assertEqual(results[0][0], 'Videri')
        self.assertGreater(results[0][2], 0.79)

class TestProcessData(unittest.TestCase):

    def test_eat_process(self):
        result=Yelpeat().get_data()
        self.assertEqual(results[1][0],'Uganda')

    def test_ride_process(self):
        resultA=lyft_data().create_table
        self.assertIn(resultA[0][2], 764)
        self.assertEqual(resultA[1][0], 'France')
        resultB=lyft_data().sort_table


class TestRegionSearch(unittest.TestCase):

    def test_region_search(self):
        results = process_command('regions sources bars_sold top=5')
        self.assertEqual(results[0][0], 'Americas')
        self.assertEqual(results[3][1], 66)
        self.assertEqual(len(results), 4)

        results = process_command('regions sellers ratings top=10')
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0][0], 'Oceania')
        self.assertGreater(results[3][1], 3.0)

unittest.main()
