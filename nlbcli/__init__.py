#!/usr/bin/env python3

# built-in
import argparse
import sys
import getpass
import os
import pickle
import re
import pkg_resources

# Unfortunately, NLB's certificate is invalid, as it's not including an intermediate
# certificate from the chain. For this PoC we're skipping the validation altogether.

VERIFY_SSL = pkg_resources.resource_filename('nlbcli', 'nlbklik-chain.pem')


# external pkgs
import requests as r
import bs4 as bs


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

NLBCLI_USER_FOLDER_PATH = os.path.expanduser('~/.nlbcli')
CREDENTIALS_FILE_PATH = os.path.join(NLBCLI_USER_FOLDER_PATH, 'credentials')
SESSION_FILE_PATH = os.path.join(NLBCLI_USER_FOLDER_PATH, 'session')


if not os.path.exists(NLBCLI_USER_FOLDER_PATH):
    os.makedirs(NLBCLI_USER_FOLDER_PATH)
    print("Info: ~/.nlbcli folder didn't exist, created it now.")


sess_global = None


def save_session_to_file():
    with open(SESSION_FILE_PATH, 'wb') as session_file:
        pickle.dump(sess_global, session_file)


def load_session_from_file():
    global sess_global
    with open(SESSION_FILE_PATH, 'rb') as session_file:
        sess_global = pickle.load(session_file)


if os.path.exists(SESSION_FILE_PATH):
    load_session_from_file()


def login_redirect_detected(response):
    """ Redirects toward the login page will have a history (302 redirection)
    which will contain the URL of the login page."""
    return response.history and '/Account/Login' in response.history[0].text


def load_credentials_from_file():
    if not os.path.exists(CREDENTIALS_FILE_PATH):
        print('Error: credentails file not found. Try running `nlbcli login` first.')
        exit(1)
    with open(CREDENTIALS_FILE_PATH, 'r') as credentials_file:
        return credentials_file.read().split('\n')


def save_credentials_to_file(username, password):
    with open(CREDENTIALS_FILE_PATH, 'w') as credentials_file:
        credentials_file.write(username + '\n' + password)


def login_with_saved_credentials():
    global sess_global
    username, password = load_credentials_from_file()
    sess = r.Session()
    data = {"UserName": username, "Password": password,
            "X-Requested-With": "XMLHttpRequest"}
    sess.post(
        'https://www.nlbklik.com.mk/Account/LoginUserNamePassword', data=data, verify=VERIFY_SSL)
    sess_global = sess
    save_session_to_file()


def fetch_retry_on_logout(request_func):
    if not sess_global:
        print('Info: no session detected, attempting to log in first')
        login_with_saved_credentials()
    response = request_func()
    if login_redirect_detected(response):
        print('Info: logout detected, attempting to log in with saved credentials')
        login_with_saved_credentials()
        return request_func()  # retry after login
    else:
        return response  # return original response


def main():
    args = parser.parse_args()
    global sess_global

    if args.subparser_name == 'login':
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        save_credentials_to_file(username, password)
        sess_global = r.Session()
        data = {"UserName": username, "Password": password,
                "X-Requested-With": "XMLHttpRequest"}
        login_res = sess_global.post(
            'https://www.nlbklik.com.mk/Account/LoginUserNamePassword', data=data, verify=VERIFY_SSL)

        # TODO: handle failed login
        save_session_to_file()

        print('Info: logged in successfully; saved credentials and session data.')

    elif args.subparser_name == 'accounts':
        if args.id:
            def retail_account_req():
                data = {"ignoreSettingContextAccount": "False",
                        "SaveFilter": "False",
                        "RemoveFilter": "False",
                        "PageNumber": "",
                        "PageSize": "",
                        "DetailsView": "0",
                        "SelectedItem": "",
                        "PageId": "",
                        "IsWidget": "False",
                        "AccountID": args.id,
                        "Report": "",
                        "X-Requested-With": "XMLHttpRequest"}
                return sess_global.post('https://www.nlbklik.com.mk/Retail/Account', data=data, verify=VERIFY_SSL)
            response = fetch_retry_on_logout(retail_account_req)
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            table_cells = soup.select('.dps-content')
            print('Account owner:', table_cells[0].text)
            print('Status:', table_cells[1].text)
            print('Current balance:', table_cells[3].text)
            print('Available balance:', table_cells[5].text)
            print('Allowed overdraft:', table_cells[7].text)
            print('Reserved funds:', table_cells[9].text)
            print('Last change:', table_cells[13].text)
            print('Last interest:', table_cells[15].text)

        else:
            def home_balances_req():
                return sess_global.get('https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank', verify=VERIFY_SSL)
            response = fetch_retry_on_logout(home_balances_req)
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            account_id_regex = r'[0-9]{3}-[0-9]{10}-[0-9]{2}[A-Z]{2,3}'
            for line in re.findall(account_id_regex, soup.text):
                print(line)

    elif args.subparser_name == 'cards':
        if args.id:
            def cms_account_req():
                data = {"ignoreSettingContextAccount": "False",
                        "SaveFilter": "False",
                        "RemoveFilter": "False",
                        "PageNumber": "",
                        "PageSize": "",
                        "DetailsView": "0",
                        "SelectedItem": "",
                        "PageId": "",
                        "IsWidget": "False",
                        "AccountID": args.id,
                        "Report": "",
                        "X-Requested-With": "XMLHttpRequest"}
                return sess_global.post('https://www.nlbklik.com.mk/Cms/Account', data=data, verify=VERIFY_SSL)
            # response = fetch_retry_on_logout(cms_account_req)
            # soup = bs.BeautifulSoup(response.text, 'html.parser')
            print('Not implemented yet.')
        else:
            def home_balances_req():
                return sess_global.get('https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank', verify=VERIFY_SSL)
            response = fetch_retry_on_logout(home_balances_req)
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            card_id_regex = r'[0-9]{8,15}/[0-9]{4}'
            for line in re.findall(card_id_regex, soup.text):
                print(line)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__': main()