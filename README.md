# The NLB CLI: NLBKlik in your terminal

Disclaimer: this is an *UNOFFICAL* tool, it's not developed by НЛБ Банка АД Скопје. It's maintained by Andrej T.

This CLI tool allows you to do a subset of the things you can do on the nlbklik.com.mk web app.
Things like checking your balance, listing transations etc.

Tested only on Linux.


## Getting started

Clone this repository. `cd` into it.

Create a symlink: `sudo ln -s /home/path/to/nlbcli/nlbcli /usr/local/bin`.

Make sure it works by typing `nlbcli --version` in the terminal.

Create a `~/.nlbcli` directory, if it doesn't already exist.

Create a new file called `~/.nlbcli/credentials`. It should contain TWO lines; first the username, then the password:

```
john.doe
SuperSecurePass123
```

Check your balance by typing `nlbcli balance`
