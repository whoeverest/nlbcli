import argparse
from datetime import date, timedelta

from .constants import DATES_FORMAT

today = date.today()
month_ago = today - timedelta(days=30)

parser = argparse.ArgumentParser()
# FIXME: this would need to be enabled so that every command has the --format argument, instead of just nlbcli accounts <id> balance
#parser.add_argument('--format', nargs="?", choices=['tab','csv','json'], required=False, default='tab')
main_subparsers = parser.add_subparsers(dest='subparser_name')
login_parser = main_subparsers.add_parser(
    'login', help='Log in and save your credentials.')
login_parser.add_argument(
    '--remember', dest="remember_credentials",  action="store_true", help="Save credentials; enables automatically re-authenticating on expired session.")

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
    '--start', required=False, default=month_ago.strftime(DATES_FORMAT))
transactions_parser.add_argument(
    '--end', required=False, default=today.strftime(DATES_FORMAT))
transactions_parser.add_argument(
    '--type', choices=['in', 'out'], required=False)
transactions_parser.add_argument('--name', required=False)

# ACCOUNTS [id] balance
balance_parser = accounts_subparsers.add_parser(
    'balance', help="Show the balance on the specified account")
balance_parser.add_argument('--format', nargs="?", choices=['tab','csv','json'], required=False, default='tab')

# ACCOUNtS [id] reservations
reservations_parser = accounts_subparsers.add_parser(
    'reservations', help="List reserved funds")

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
