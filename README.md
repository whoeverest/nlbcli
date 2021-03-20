# The NLB CLI: NLBKlik in your terminal

Disclaimer: this is an _UNOFFICAL_ tool, it's not developed by НЛБ Банка АД Скопје. It's maintained by Andrej T.

This CLI tool allows you to do a subset of the things you can do on the nlbklik.com.mk web app.
Things like checking your balance, listing transations etc.

## Getting started

To install just run:
```bash
pip install git+https://github.com/whoeverest/nlbcli.git
```

If the install fails because of write permissions, try using `sudo`.

Now `nlbcli` should be available as an executable in your shell. If using pip w/ `--user` flag, make sure `~/.local/bin` is in `$PATH`

* Log in: `nlbcli login`
    * credentials get stored in `~/.nlbcli/credentials`
    * sessions expire quite fast, but the tool will automatically log you back in when it detects an expired session.
* List your account IDs: `nlbcli accounts`
* Get account details: `nlbcli accounts --id $ACCOUNT_ID`

## Install in development mode

1. Clone the GitHub repository
2. Run `pip install --editable .` to create a editable/dev install
3. Perform code changes in `nlbcli/`
4. Changes will picked up when running `nlbcli` or `python nlbcli/__init__.py` without re-doing `pip install`
