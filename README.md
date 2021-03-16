# The NLB CLI: NLBKlik in your terminal

Disclaimer: this is an *UNOFFICAL* tool, it's not developed by НЛБ Банка АД Скопје. It's maintained by Andrej T.

This CLI tool allows you to do a subset of the things you can do on the nlbklik.com.mk web app.
Things like checking your balance, listing transations etc.

Tested only on Linux.


## Getting started

Clone this repository. `cd` into it.

Run `pip install requests`

Create a symlink: `sudo ln -s /home/path/to/nlbcli/nlbcli /usr/local/bin`.

Make sure it works by typing `nlbcli --version` in the terminal.

Log in: `nlbcli login`

This will prompt you for your username and password, and store them in `~/.nlbcli/credentials`.

Sessions expire quite fast, but the tool will automatically log you back in when it detects an expired session. It'll happen in the background.

Check your balance by typing `nlbcli balance`
