import unittest
import pandas as pd
from io import StringIO
import tempfile
# Mock chardet.detect to always return utf-8 encoding (for simplicity in this example)
import chardet

import sys
sys.path.append('../')
from depot_diffs import read_csv_file, calculate_expected_portfolio, convert_to_float  # Import necessary functions

def mock_detect(*args, **kwargs):
    return {'encoding': 'utf-8'}

chardet.detect = mock_detect

class TestDepotDiffsScript(unittest.TestCase):

    def test_read_csv_file(self):
        csv_content = """WKN;Stück;Wert
    ABC123;10,5;5.000,5
    DEF456;5,5;3.000,3
    """
        # Create a temporary file and write the mock data into it
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
            temp.write(csv_content)
            temp.seek(0)
            df = read_csv_file(temp.name)

        # Assert DataFrame shape and data types
        self.assertEqual(df.shape, (2, 3))
        self.assertEqual(df['Stück'].dtype, float)
        self.assertEqual(df['Wert'].dtype, float)

    def test_calculate_expected_portfolio(self):
        data = {
            'WKN': ['ABC123', 'ABC123', 'DEF456', 'DEF456'],
            'Stück': [10.0, 3.0, 20.0, 5.0],
            'Wert': [1000.0, 300.0, 4000.0, 1000.0],
            'Typ': ['Kauf', 'Verkauf', 'Kauf', 'Verkauf']
        }
        df = pd.DataFrame(data)

        result = calculate_expected_portfolio(df)

        # Expected outcome
        expected_data = {
            'WKN': ['ABC123', 'DEF456'],
            'Expected_Stück': [7.0, 15.0],
            'Avg_Kaufkurs_in_EUR': [100.0, 200.0]  # 1000/10 and 4000/20 respectively
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df, check_dtype=False)


    def convert_to_float(df, column_name):
        df[column_name] = df[column_name].str.replace('.', '')  
        df[column_name] = df[column_name].str.replace(',', '.') 
        df[column_name] = pd.to_numeric(df[column_name], errors='coerce')
        # Ensure the result is float
        df[column_name] = df[column_name].astype(float)

if __name__ == "__main__":
    unittest.main()
