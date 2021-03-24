import os
import pkg_resources

NLBCLI_USER_FOLDER_PATH = os.path.expanduser('~/.nlbcli')
CREDENTIALS_FILE_PATH = os.path.join(NLBCLI_USER_FOLDER_PATH, 'credentials')
SESSION_FILE_PATH = os.path.join(NLBCLI_USER_FOLDER_PATH, 'session')

# Unfortunately, NLB's certificate is invalid, as it's not including an intermediate
# certificate from the chain. For this PoC we're skipping the validation altogether.
VERIFY_SSL = pkg_resources.resource_filename('nlbcli', 'nlbklik-chain.pem')

DATES_FORMAT = '%d.%m.%Y'
