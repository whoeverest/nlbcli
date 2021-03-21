import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser_name')
login_parser = subparsers.add_parser(
    'login', help='Log in and save your credentials.')

# accounts
accounts_parser = subparsers.add_parser(
    'accounts', help='List accounts, get account details...')
accounts_parser.add_argument('account_id', nargs="?")

# cards
cards_parser = subparsers.add_parser('cards', help='List cards...')

# transactions parser
transactions_parser = subparsers.add_parser(
    'transactions', help='List and filter transactions, get transaction details...')
transactions_parser.add_argument('account_id')

parsed_args = parser.parse_args()
