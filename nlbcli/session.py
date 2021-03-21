import os
import pickle
import requests as r
import bs4 as bs

from . import constants


def _save_session_to_file(sess):
    if not os.path.exists(constants.SESSION_FILE_PATH):
        print('Error: session file not found; try running `nlbcli login` first.')
        exit(1)
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


def _login(username, password):
    """ Performs a log in and returns a Requests session, or throws on unsuccessful login. """
    new_session = r.Session()
    data = {"UserName": username, "Password": password,
            "X-Requested-With": "XMLHttpRequest"}
    url = 'https://www.nlbklik.com.mk/Account/LoginUserNamePassword'
    login_res = new_session.post(
        url, data=data, verify=constants.VERIFY_SSL, allow_redirects=False)
    login_json_body = login_res.json()

    # Response always contains 'ErrorMessage' key and has status code 200, unfortunately.
    if login_json_body['ErrorMessage'] != None:
        response_msg = login_res.json()['ErrorMessage']
        raise Exception(response_msg)
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
        print('Info: logout detected, attempting to log in with saved credentials')
        new_session = _login_with_saved_credentials()
        response = req_fn(new_session)  # retry after login
        _save_session_to_file(new_session)
    else:
        _save_session_to_file(old_session)
    return response


def login_and_save_credentials(username, password):
    """ Performs a log in, and saves the credentials in a file, where they'll be
    read and used again in case of an expired session."""
    new_session = _login(username, password)
    _save_credentials_to_file(username, password)
    _save_session_to_file(new_session)
    print('Info: logged in successfully; saved credentials and session data.')


def nlb_post(url, data):
    """
    Performs a POST requests; auto-renews expired sessions.
    Returns a tuple: the response and the parsed html body."""
    def req_fn(sess):
        return sess.post(
            url, data=data, verify=constants.VERIFY_SSL, allow_redirects=False)
    response = _fetch_with_autorenewal(req_fn)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    return (response, soup)


def nlb_get(url):
    """
    Performs a GET requests; auto-renews expired sessions.
    Returns a tuple: the response and the parsed html body.
    """
    def req_fn(sess):
        return sess.get(url, verify=constants.VERIFY_SSL,
                        allow_redirects=False)
    response = _fetch_with_autorenewal(req_fn)
    soup = bs.BeautifulSoup(response.text, 'html.parser')
    return (response, soup)
