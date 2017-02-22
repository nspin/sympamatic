# sympamatic

Sign up for all Carleton Sympa email lists.

## Usage

```
$ python3 sympamatic.py --help
usage: sympamatic.py [-h] [-r] [-n] [-u USERNAME] [-p PASSWORD]
                     [-c CREDS_FILE]

Sign up for all Carleton email lists. You must have a list of lists email in
your inbox, unless run with the --with-new-lists option.

optional arguments:
  -h, --help            show this help message and exit
  -r, --request-lists   Just request the list of lists email and do nothing
                        else.
  -n, --with-new-lists  Request the list of lists email, and then wait for a
                        response and subscribe to all.
  -u USERNAME, --username USERNAME
                        Gmail address (e.g. example@gmail.com)
  -p PASSWORD, --password PASSWORD
                        Gmail password
  -c CREDS_FILE, --creds-file CREDS_FILE
                        JSON document with keys "username" and "password"
```

## Note

This script is for educational purposes only.
The Sympa list system is more manual than you may think.
You will cause inconvenience, or even suspicion, especially if you use a non-Carleton email address.

I've put this here because it contains useful snippets for automating Sympa-related tasks.
