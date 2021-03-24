#!/usr/bin/env python3

# built-in
import sys
import os
import re
from datetime import date, timedelta

# local files
from . import constants
from .args_parser import parsed_args, parser
from .session import prompt_for_credentials, login_and_remember_credentials, nlb_post, nlb_get

# create state folder if it doesn't exist
if not os.path.exists(constants.NLBCLI_USER_FOLDER_PATH):
    os.makedirs(constants.NLBCLI_USER_FOLDER_PATH)
    print("Info: ~/.nlbcli folder didn't exist, created it now.")


def main():
    if parsed_args.subparser_name == 'login':
        username, password = prompt_for_credentials()
        login_and_remember_credentials(
            username, password, remember_credentials=parsed_args.remember_credentials)

    elif parsed_args.subparser_name == 'accounts':
        if parsed_args.accounts_subparser_name == 'balance':
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

        elif parsed_args.accounts_subparser_name == 'transactions':
            # direction explanation:
            # 0 means 'both debit and credit'; 1 means 'credit'; -1 means 'debit'
            direction = "0"
            if parsed_args.type:
                direction = "1" if parsed_args.type == 'in' else "-1"

            # counterparty name
            # todo: this isn't working for some inexplicable reason
            other_party_name = ""
            if parsed_args.name:
                other_party_name = parsed_args.name

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
                "DateFrom": parsed_args.start,  # todo: validation
                "DateTo": parsed_args.end,  # todo: validation
                "Direction": direction,
                "AmountCondition": "",
                "AmountFrom": "",
                "Amount": "",
                "AmountTo": "",
                "OtherPartyName": other_party_name,
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

        elif parsed_args.accounts_subparser_name == 'reservations':
            url = 'https://www.nlbklik.com.mk/Retail/ReservationList'
            data = {"ignoreSettingContextAccount": "False",
                    "SaveFilter": "False",
                    "RemoveFilter": "False",
                    "PageNumber": "",
                    "PageSize": "20",
                    "DetailsView": "0",
                    "SelectedItem": "",
                    "PageId": "",
                    "IsWidget": "False",
                    "AccountID": parsed_args.account_id,
                    "SortColumn": "Date",
                    "SortDirection": "DESC",
                    "Report": "",
                    "X-Requested-With": "XMLHttpRequest"}
            _, soup = nlb_post(url, data)
            for tr in soup.select('tbody > tr'):
                tds = tr.select('td')
                print('\t'.join(td.text.strip() for td in tds))

        else:
            # list accounts
            url = 'https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank'
            _, soup = nlb_get(url)
            account_id_regex = r'[0-9]{3}-[0-9]{10}-[0-9]{2}[A-Z]{2,3}'
            for line in re.findall(account_id_regex, soup.text):
                print(line)

    elif parsed_args.subparser_name == 'cards':
        if parsed_args.cards_subparser_name == 'balance':
            print('Error: card balance not implemented yet.')

        elif parsed_args.cards_subparser_name == 'transactions':
            today = date.today()
            month_ago = today - timedelta(days=30)
            url = 'https://www.nlbklik.com.mk/Cms/Transactions'
            data = {"ignoreSettingContextAccount": "False",
                    "SaveFilter": "False",
                    "RemoveFilter": "False",
                    "PageNumber": "",
                    "PageSize": "20",
                    "DetailsView": "0",
                    "SelectedItem": "",
                    "PageId": "",
                    "IsWidget": "False",
                    "AccountID": parsed_args.card_id,
                    "DateFrom": month_ago.strftime(constants.DATES_FORMAT),
                    "DateTo": today.strftime(constants.DATES_FORMAT),
                    "CardNumber": "",
                    "AmountCondition": "",
                    "AmountFrom": "",
                    "Amount": "",
                    "AmountTo": "",
                    "TrnDescription": "",
                    "SortColumn": "Date",
                    "SortDirection": "DESC",
                    "Report": "",
                    "X-Requested-With": "XMLHttpRequest"}
            _, soup = nlb_post(url, data)
            for tr in soup.select('tbody > tr'):
                tds = tr.select('td')
                print('\t'.join(td.text.strip() for td in tds))

        else:
            url = 'https://www.nlbklik.com.mk/Home/Balances?bankid=tutunska.banka@ibank'
            _, soup = nlb_get(url)
            card_id_regex = r'[0-9]{8,15}/[0-9]{4}'
            for line in re.findall(card_id_regex, soup.text):
                print(line)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == '__main__':
    main()
