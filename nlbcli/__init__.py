#!/usr/bin/env python3

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
        if parsed_args.account_id:
            data = {"ignoreSettingContextAccount": "False",
                    "SaveFilter": "False",
                    "RemoveFilter": "False",
                    "PageNumber": "",
                    "PageSize": "",
                    "DetailsView": "0",
                    "SelectedItem": "",
                    "PageId": "",
                    "IsWidget": "False",
                    "AccountID": parsed_args.account_id,
                    "Report": "",
                    "X-Requested-With": "XMLHttpRequest"}

            url = 'https://www.nlbklik.com.mk/Retail/Account'
            _, soup = nlb_post(url, data)
            table_cells = soup.select('.dps-content')
            print('Account Id:', parsed_args.account_id)
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
            _, soup = nlb_get(url)
            account_id_regex = r'[0-9]{3}-[0-9]{10}-[0-9]{2}[A-Z]{2,3}'
            for line in re.findall(account_id_regex, soup.text):
                print(line)

    elif parsed_args.subparser_name == 'cards':
        url = 'https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank'
        _, soup = nlb_get(url)
        card_id_regex = r'[0-9]{8,15}/[0-9]{4}'
        for line in re.findall(card_id_regex, soup.text):
            print(line)

    elif parsed_args.subparser_name == 'transactions':
        url = 'https://www.nlbklik.com.mk/Retail/Transactions'
        data = {
            "ignoreSettingContextAccount": "False",
            "SaveFilter": "False",
            "RemoveFilter": "False",
            "PageNumber": "",
            "PageSize": "",
            "DetailsView": "0",
            "SelectedItem": "",
            "PageId": "",
            "IsWidget": "False",
            "AccountID": parsed_args.account_id,
            "DateFrom": "21.02.2021",  # todo: remove hardcoded value
            "DateTo": "21.03.2021",  # todo: remove hardcoded value
            "Direction": "0",
            "AmountCondition": "",
            "AmountFrom": "",
            "Amount": "",
            "AmountTo": "",
            "OtherPartyName": "",
            "OtherPartyAccount": "",
            "TransactionsForPrint": "",
            "SortColumn": "Date",
            "SortDirection": "DESC",
            "Report": "",
            "X-Requested-With": "XMLHttpRequest"
        }
        _, soup = nlb_post(url, data)

        # we print all cells except the "Details" link/button
        # todo: parse the 0th column to extract the unique transaction id
        for tr in soup.select('tbody > tr'):
            tds = tr.select('td')[1:]
            print('\t'.join(td.text.strip() for td in tds))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
