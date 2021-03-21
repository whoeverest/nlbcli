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
transactions_parser.add_argument(
    '--start', required=False, default="21.02.2021")  # todo: base on today's date
transactions_parser.add_argument(
    '--end', required=False, default="21.03.2021")  # todo: base on today's date
transactions_parser.add_argument(
    '--type', choices=['in', 'out'], required=False)
transactions_parser.add_argument('--name', required=False)
parsed_args = parser.parse_args()
