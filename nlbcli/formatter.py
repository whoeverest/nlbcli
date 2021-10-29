import re
import csv
import json
import sys


def OutputResult(parsed_args, table_cells):
    output_format = parsed_args.format
    anon = parsed_args.anon
    if output_format == 'tab':
        print('Account Id:', parsed_args.account_id)
        print('Account owner:', table_cells[0].text)
        print('Status:', table_cells[1].text)
        print('Current balance:', table_cells[3].text)
        print('Available balance:', table_cells[5].text)
        print('Allowed overdraft:', table_cells[7].text)
        print('Reserved funds:', table_cells[9].text)
        print('Last change:', table_cells[13].text)
        print('Last interest:', table_cells[15].text)
    elif output_format == 'json':
        json_output = json.dumps(
            {
                'account-id': parsed_args.account_id if anon == False else "REDACTED",
                'account-owner': table_cells[0].text if anon == False else "REDACTED",
                'account-status': table_cells[1].text if anon == False else "REDACTED",
                'current-balance': table_cells[3].text if anon == False else "REDACTED",
                'available-balance': table_cells[5].text if anon == False else "REDACTED",
                'allowed-overdraft': table_cells[7].text if anon == False else "REDACTED",
                'reserved-funds': table_cells[9].text if anon == False else "REDACTED",
                'last-change': table_cells[13].text if anon == False else "REDACTED",
                'last-interest': table_cells[15].text if anon == False else "REDACTED"
            }
        )
        print(json_output)
    elif output_format == 'csv':
        field_names = ['account-id',
                       'account-owner',
                       'account-status',
                       'current-balance',
                       'available-balance',
                       'allowed-overdraft',
                       'reserved-funds',
                       'last-change',
                       'last-interest']
        csv_writer = csv.DictWriter(sys.stdout, field_names)
        csv_writer.writeheader()
        csv_writer.writerow({
            'account-id': parsed_args.account_id if anon == False else "REDACTED",
            'account-owner': table_cells[0].text if anon == False else "REDACTED",
            'account-status': table_cells[1].text,
            'current-balance': table_cells[3].text if anon == False else "REDACTED",
            'available-balance': table_cells[5].text if anon == False else "REDACTED",
            'allowed-overdraft': table_cells[7].text if anon == False else "REDACTED",
            'reserved-funds': table_cells[9].text if anon == False else "REDACTED",
            'last-change': table_cells[13].text if anon == False else "REDACTED",
            'last-interest': table_cells[15].text if anon == False else "REDACTED"
        })
