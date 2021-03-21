import argparse

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest='subparser_name')
login_parser = subparsers.add_parser(
    'login', help='Log in and save your credentials')

# accounts
accounts_parser = subparsers.add_parser(
    'accounts', help='Tools for working with your bank accounts')
accounts_parser.add_argument('--id')

# cards
cards_parser = subparsers.add_parser(
    'cards', help='Tools for working with your cards')
cards_parser.add_argument('--id')

parsed_args = parser.parse_args()
