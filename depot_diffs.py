import pandas as pd
import chardet
import argparse

def read_csv_file(file_path, delimiter=";"):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return pd.read_csv(file_path, delimiter=delimiter, encoding=result['encoding'], thousands='.', decimal=',')

def calculate_expected_portfolio(transactions_df):
    # Convert columns to numeric, handling errors
    transactions_df[['Stück', 'Wert']] = transactions_df[['Stück', 'Wert']].apply(pd.to_numeric, errors='coerce').fillna(0)

    # Calculate expected stocks and average purchase value for each WKN
    expected_portfolio = transactions_df.groupby('WKN').apply(lambda x: pd.Series({
        'Expected_Stück': x[x['Typ'] == 'Kauf']['Stück'].sum() - x[x['Typ'] == 'Verkauf']['Stück'].sum(),
        'Avg_Kaufkurs_in_EUR': x[x['Typ'] == 'Kauf']['Wert'].sum() / x[x['Typ'] == 'Kauf']['Stück'].sum() if x[x['Typ'] == 'Kauf']['Stück'].sum() != 0 else 0
    })).reset_index()
    return expected_portfolio

def convert_to_float(df, column_name):
    # Convert column values from strings to float, replacing commas with dots and handling thousands separators
    df[column_name] = df[column_name].replace('[.,]', '', regex=True).replace(',', '.', regex=True)
    df[column_name] = pd.to_numeric(df[column_name], errors='coerce')

def main():
    parser = argparse.ArgumentParser(description='Compare a stock CSV with trade history CSV(s).')
    parser.add_argument('bestands_csv', help='Path to the stock CSV file')
    parser.add_argument('handels_csv', nargs='+', help='Path to one or multiple trade history CSV files')

    args = parser.parse_args()
    
    depot_df = read_csv_file(args.bestands_csv)
    transactions_dfs = [read_csv_file(file) for file in args.handels_csv]
    transactions_df = pd.concat(transactions_dfs, ignore_index=True)

    # Convert specific columns to float after reading the files
    for column in ['Stück/Nom.', 'Kaufkurs in EUR']:
        convert_to_float(depot_df, column)
    
    expected_portfolio = calculate_expected_portfolio(transactions_df)

    # Merge the expected and actual portfolios based on WKN
    comparison_df = depot_df[['WKN', 'Stück/Nom.', 'Kaufkurs in EUR']].merge(expected_portfolio, on='WKN', how='outer').fillna(0)

    # Find differences
    comparison_df['Diff_Stück'] = comparison_df['Stück/Nom.'] - comparison_df['Expected_Stück']
    comparison_df['Diff_Kaufkurs_in_EUR'] = comparison_df['Kaufkurs in EUR'] - comparison_df['Avg_Kaufkurs_in_EUR']

    # Filter rows with differences
    differences_df = comparison_df[(comparison_df['Diff_Stück'] != 0) | (comparison_df['Diff_Kaufkurs_in_EUR'] != 0)]
    print(differences_df)
    differences_df.to_csv('differences.csv', index=False)

if __name__ == "__main__":
    main()
