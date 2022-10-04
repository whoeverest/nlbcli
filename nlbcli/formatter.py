import re
import csv
import json
import sys


def OutputResult(parsed_args, table_cells, input_type):
    output_format = parsed_args.format
    if output_format == 'tab':
        if input_type == "accounts":
            print('Account Id:', parsed_args.account_id)
            print('Account owner:', table_cells[0].text)
            print('Status:', table_cells[1].text)
            print('Current balance:', table_cells[3].text)
            print('Available balance:', table_cells[5].text)
            print('Allowed overdraft:', table_cells[7].text)
            print('Reserved funds:', table_cells[9].text)
            print('Last change:', table_cells[13].text)
            print('Last interest:', table_cells[15].text)
        elif input_type == "transactions":
            for tr in table_cells:
                tds = tr.select('td')[1:]
                print('\t'.join(td.text.strip() for td in tds))
    elif output_format == 'json':
        if input_type == "accounts":
            json_output = json.dumps(
                {
                    'account-id': parsed_args.account_id,
                    'account-owner': table_cells[0].text,
                    'account-status': table_cells[1].text,
                    'current-balance': table_cells[3].text,
                    'available-balance': table_cells[5].text,
                    'allowed-overdraft': table_cells[7].text,
                    'reserved-funds': table_cells[9].text,
                    'last-change': table_cells[13].text,
                    'last-interest': table_cells[15].text
                },indent=4
            )
        elif input_type == "transactions":
            txns = []
            for tr in table_cells:
                tds = tr.select('td')[1:]
                dict_txn = {}
                dict_txn['date'] = tds[0].text.strip()
                dict_txn['recipient_name'] = tds[1].text.strip()
                dict_txn['txn_description'] = tds[2].text.strip()
                dict_txn['status'] = tds[3].text.strip()
                dict_txn['amount'] = tds[4].text.strip()
                dict_txn['txn_fee'] = tds[5].text.strip()
                dict_txn['balance'] = tds[6].text.strip()
                txns.append(dict_txn)
            json_output = json.dumps(txns,indent=4)
        print(json_output)
    elif output_format == 'csv':
        if input_type == "accounts":
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
                'account-id': parsed_args.account_id,
                'account-owner': table_cells[0].text,
                'account-status': table_cells[1].text,
                'current-balance': table_cells[3].text,
                'available-balance': table_cells[5].text,
                'allowed-overdraft': table_cells[7].text,
                'reserved-funds': table_cells[9].text,
                'last-change': table_cells[13].text,
                'last-interest': table_cells[15].text
            })
