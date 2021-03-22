# The NLB CLI: NLBKlik in your terminal

Disclaimer: this is an **UNOFFICAL** tool, it's not developed by НЛБ Банка АД Скопје. It's maintained by Andrej T.

This CLI tool allows you to do a subset of the things you can do on the nlbklik.com.mk web app.
Things like checking your balance, listing transations etc.

## Getting started

To install just run:

```bash
pip install git+https://github.com/whoeverest/nlbcli.git
```

Now `nlbcli` should be available as an executable in your shell. If using pip w/ `--user` flag, make sure `~/.local/bin` is in `$PATH`

- Log in: `nlbcli login`
- List your account IDs: `nlbcli accounts`
- See the balance on one account: `nlbcli accounts $ACCOUNT_ID balance`
- List recent transactions: `nlbcli accounts $ACCOUNT_ID transactions`
- Filter transactions: `nlbcli accounts $ACCOUNT_ID transactions --start="01.01.2019" --end="30.01.2019" --name="EVN" --type="out"`
- List cards: `nlbcli cards`
- Reserved funds (recent transactions): `nlbcli accounts $ACCOUNT_ID reservations`

Running `nlbcli -h` will show you all the available commands.

Each command has it's own help section: `nlbcli accounts -h` or `nlbcli accounts $ACCOUNT_ID transactions -h`

## Install in development mode

1. Clone the GitHub repository
2. Run `pip install --editable .` to create a editable/dev install
3. Perform code changes in `nlbcli/`
4. Changes will picked up when running `nlbcli` without re-doing `pip install`

# How it works

At it's core, `nlbcli` is a script written in Python 3 which acts like a simplified browser.
It sends HTTPS requests, parses the HTML responses and prints the data in a way that's
suitable for the terminal. Intead of using GUI and your mouse, you can access your NLBKlik
data using the terminal and keyboard.

When you run `nlbcli login` your credentails (username and password) are stored in _plaintext_
in a file located at `~/.nlbcli/credentials`. You can inspect this file using any text editor. The
credentials are remembered so that you run `nlbcli` in automated setups, where a human can't re-enter
them all the time. **Keep the ~/.nlbcli directory safe!**

Your session, with all the cookies is stored in `~/.nlbcli/session`. This is a binary file, which
is produced by serializing (pickling) the `requests.Session()` object. The session expires relatively
often, but `nlbcli` automatically logs you back in, when it detects a 302 Redirect response towards
the NLBKlik login page.

NLBCLI relies on just two extremely popular Python libraries: [Requests](https://2.python-requests.org/en/master/) for doing performing HTTP requests and handling sessions, and [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for parsing the HTML contents. The rest of the external modules
come from Python's standard library.

The whole of the code is available on GitHub for inspection. In the documentation, you're advised to
install the package directly from the repository, via: `pip install git+https://github.com/whoeverest/nlbcli.git`. Before installing, feel free to make sure that there isn't anything weird going on,
especially in the part of the code that's dealing with sensitive data.

**NLBCLI comes with no warranty!** It's a piece of software owned by a single person and maintained by a
small community. Use it at your own risk!

If you have any questions, feel free to open an issue, or drop me a line at andrejtrajchevski at googleprovider's email.
