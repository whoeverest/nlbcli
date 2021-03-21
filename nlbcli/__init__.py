#!/usr/bin/env python3

# external pkgs
import bs4 as bs

# built-in
import sys
import getpass
import os
import pickle
import re
import pkg_resources

# local files
from . import constants
from .args_parser import parsed_args, parser
from .session import login_and_save_credentials, nlb_post, nlb_get

# create state folder if it doesn't exist
if not os.path.exists(constants.NLBCLI_USER_FOLDER_PATH):
    os.makedirs(constants.NLBCLI_USER_FOLDER_PATH)
    print("Info: ~/.nlbcli folder didn't exist, created it now.")


def main():
    if parsed_args.subparser_name == 'login':
        username = input('Username: ')
        password = getpass.getpass('Password: ')
        login_and_save_credentials(username, password)

    elif parsed_args.subparser_name == 'accounts':
        if parsed_args.id:
            data = {"ignoreSettingContextAccount": "False",
                    "SaveFilter": "False",
                    "RemoveFilter": "False",
                    "PageNumber": "",
                    "PageSize": "",
                    "DetailsView": "0",
                    "SelectedItem": "",
                    "PageId": "",
                    "IsWidget": "False",
                    "AccountID": parsed_args.id,
                    "Report": "",
                    "X-Requested-With": "XMLHttpRequest"}

            url = 'https://www.nlbklik.com.mk/Retail/Account'
            response = nlb_post(url, data)
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
            url = 'https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank'
            response = nlb_get(url)
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            account_id_regex = r'[0-9]{3}-[0-9]{10}-[0-9]{2}[A-Z]{2,3}'
            for line in re.findall(account_id_regex, soup.text):
                print(line)

    elif parsed_args.subparser_name == 'cards':
        if parsed_args.id:
            data = {"ignoreSettingContextAccount": "False",
                    "SaveFilter": "False",
                    "RemoveFilter": "False",
                    "PageNumber": "",
                    "PageSize": "",
                    "DetailsView": "0",
                    "SelectedItem": "",
                    "PageId": "",
                    "IsWidget": "False",
                    "AccountID": parsed_args.id,
                    "Report": "",
                    "X-Requested-With": "XMLHttpRequest"}
            # response = nlb_post('https://www.nlbklik.com.mk/Cms/Account', data=data)
            # soup = bs.BeautifulSoup(response.text, 'html.parser')
            print('Error: not implemented yet.')
        else:
            url = 'https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank'
            response = nlb_get(url)
            soup = bs.BeautifulSoup(response.text, 'html.parser')
            card_id_regex = r'[0-9]{8,15}/[0-9]{4}'
            for line in re.findall(card_id_regex, soup.text):
                print(line)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
