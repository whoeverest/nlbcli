import os
import pickle
import requests as r
import bs4 as bs
import getpass

from . import constants


class ResponseErrorException(Exception):
    pass


def _save_session_to_file(sess):
    with open(constants.SESSION_FILE_PATH, 'wb') as session_file:
        pickle.dump(sess, session_file)


def _load_session_from_file():
    with open(constants.SESSION_FILE_PATH, 'rb') as session_file:
        return pickle.load(session_file)


def _login_redirect_detected(response):
    return response.status_code == 302


def _load_credentials_from_file():
    if not os.path.exists(constants.CREDENTIALS_FILE_PATH):
        print('Error: credentails file not found. Try running `nlbcli login` first.')
        exit(1)
    with open(constants.CREDENTIALS_FILE_PATH, 'r') as credentials_file:
        return credentials_file.read().split('\n')


def _save_credentials_to_file(username, password):
    with open(constants.CREDENTIALS_FILE_PATH, 'w') as credentials_file:
        credentials_file.write(username + '\n' + password)


def _credentials_file_exists():
    return os.path.exists(constants.CREDENTIALS_FILE_PATH)


def _login(username, password):
    """ Performs a log in and returns a Requests session, or throws on unsuccessful login. """
    new_session = r.Session()
    data = {"UserName": username, "Password": password,
            "X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.nlbklik.com.mk/Account/LoginUserNamePassword'
    login_res = new_session.post(url, data=data, allow_redirects=False)
    login_json_body = login_res.json()

    # Response always contains 'ErrorMessage' key and has status code 200, unfortunately.
    if login_json_body['ErrorMessage'] != None:
        response_msg = login_res.json()['ErrorMessage']
        raise ResponseErrorException(
            'Server returned an error: ' + response_msg)
    else:
        return new_session


def _login_with_saved_credentials():
    """ Returns a fresh session object after logging in. """
    username, password = _load_credentials_from_file()
    new_session = _login(username, password)
    return new_session


def _fetch_with_autorenewal(req_fn):
    """
    Tries to fulfil the requests with the old session. If that fails, tries to log in and retries the requests.
    Saves the resulting session in a file.
    Returns a response.
    """
    old_session = _load_session_from_file()
    response = req_fn(old_session)
    if _login_redirect_detected(response):
        print('Info: logout detected, attempting to log in')
        if _credentials_file_exists():
            print('Info: using saved credentials.')
            new_session = _login_with_saved_credentials()
        else:
            username, password = prompt_for_credentials()
            new_session = _login(username, password)
        response = req_fn(new_session)  # retry after login
        _save_session_to_file(new_session)
    else:
        _save_session_to_file(old_session)
    return response


def prompt_for_credentials():
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    return (username, password)


def login_and_remember_credentials(username, password, remember_credentials=False):
    """ Performs a log in, and optionally saves the credentials in a file,
    where they can be read and used again in case of an expired session."""
    try:
        new_session = _login(username, password)
    except ResponseErrorException as e:
        print('Error: login failed.', e)
        exit(1)

    if remember_credentials:
        print('Info: saved credentials at: ' + constants.CREDENTIALS_FILE_PATH)
        _save_credentials_to_file(username, password)
    _save_session_to_file(new_session)
    print('Info: logged in successfully, saved session data at: ' +
          constants.SESSION_FILE_PATH)


def nlb_post(url, data):
    """
    Performs a POST requests; auto-renews expired sessions.
    Returns a tuple: the response and the parsed html body."""
    def req_fn(sess):
        return sess.post(url, data=data, allow_redirects=False)
    response = _fetch_with_autorenewal(req_fn)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    return (response, soup)


def nlb_get(url):
    """
    Performs a GET requests; auto-renews expired sessions.
    Returns a tuple: the response and the parsed html body.
    """
    def req_fn(sess):
        return sess.get(url, allow_redirects=False)
    response = _fetch_with_autorenewal(req_fn)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    return (response, soup)
