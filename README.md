# The NLB CLI: NLBKlik in your terminal

Disclaimer: this is an _UNOFFICAL_ tool, it's not developed by НЛБ Банка АД Скопје. It's maintained by Andrej T.

This CLI tool allows you to do a subset of the things you can do on the nlbklik.com.mk web app.
Things like checking your balance, listing transations etc.

Tested only on Linux.

## Getting started

Clone this repository. `cd` into it.

Run `pip install requests bs4`

Log in: `./nlbcli login`

This will prompt you for your username and password, and store them in `~/.nlbcli/credentials`.

Sessions expire quite fast, but the tool will automatically log you back in when it detects an expired session. It'll happen in the background.

List your account IDs: `./nlbcli accounts`

Get account details: `./nlbcli accounts --id $ACCOUNT_ID`

Optionally, create a symlink: `sudo ln -s /home/path/to/nlbcli/nlbcli /usr/local/bin`.
