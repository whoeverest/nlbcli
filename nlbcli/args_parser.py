import argparse

parser = argparse.ArgumentParser()
main_subparsers = parser.add_subparsers(dest='subparser_name')
login_parser = main_subparsers.add_parser(
    'login', help='Log in and save your credentials.')

# ACCOUNTS
accounts_parser = main_subparsers.add_parser(
    'accounts', help='List accounts')
accounts_parser.add_argument('account_id', nargs="?")
accounts_subparsers = accounts_parser.add_subparsers(
    dest='accounts_subparser_name')

# ACCOUNTS [id] transactions
transactions_parser = accounts_subparsers.add_parser(
    'transactions', help='List and filter transactions')
transactions_parser.add_argument(
    '--start', required=False, default="21.02.2021")  # todo: base on today's date
transactions_parser.add_argument(
    '--end', required=False, default="21.03.2021")  # todo: base on today's date
transactions_parser.add_argument(
    '--type', choices=['in', 'out'], required=False)
transactions_parser.add_argument('--name', required=False)

# ACCOUNTS [id] balance
balance_parser = accounts_subparsers.add_parser(
    'balance', help="Show the balance on the specified account")

# CARDS
cards_parser = main_subparsers.add_parser('cards', help='List cards')
cards_parser.add_argument('card_id', nargs='?')
cards_subparsers = cards_parser.add_subparsers(dest="cards_subparser_name")

# CARDS [id] balance
cards_subparsers.add_parser(
    'balance', help="Show the balance on the specified card")

# CARDS [id] transactions
cards_subparsers.add_parser(
    'transactions', help="List and filter card transactions")

# export
parsed_args = parser.parse_args()
