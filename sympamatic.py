import re
import sys
import time
import json
import base64
from email.utils import parsedate
from argparse import ArgumentParser

from gmail.imap import GIMAP
from gmail.smtp import GSMTP


SYMPA_ADDR = 'sympa@lists.carleton.edu'


class Subscriber(object):

    def __init__(self, username, password):
        self.imap = GIMAP(username, password)
        self.smtp = GSMTP(username, password)


    def request_lists(self):
        self.smtp.send(SYMPA_ADDR, 'LISTS')


    def get_lists(self, cutoff=0):
        uids = self.imap.search('from: "{}" "Here is the list of lists"'.format(SYMPA_ADDR))
        for uid in reversed(uids):
            m = self.imap.fetch(uid)
            t = time.mktime(parsedate(m['Date']))
            if t > cutoff:
                b = base64.b64decode(m.get_payload()).decode('utf-8')
                return re.compile('^(.*?@lists.carleton.edu) :', re.M).findall(b)
            break
        return None


    def new_lists(self):
        t = time.time()
        self.request_lists()
        sys.stderr.write('Waiting for list of lists to arrive... ')
        sys.stderr.flush()
        while True:
            time.sleep(5)
            l = self.get_lists(cutoff=t)
            if l is not None:
                sys.stderr.write('DONE\n')
                sys.stderr.flush()
                return l


    def subscribe(self, lists):
        body = '\n'.join(map('SUBSCRIBE {}'.format, lists))
        print(body)
        # self.sender.send(body)


def main():

    parser = ArgumentParser(description='Sign up for all Carleton email lists. You must have a list of lists email in your inbox, unless run with the --with-new-lists option.')
    parser.add_argument('-r', '--request-lists', action='store_true', help='Just request the list of lists email and do nothing else.')
    parser.add_argument('-n', '--with-new-lists', action='store_true', help='Request the list of lists email, and then wait for a response and subscribe to all.')
    parser.add_argument('-u', '--username', nargs=1, metavar='USERNAME', help='Gmail address (e.g. example@gmail.com)')
    parser.add_argument('-p', '--password', nargs=1, metavar='PASSWORD', help='Gmail password')
    parser.add_argument('-c', '--creds-file', nargs=1, metavar='CREDS_FILE', help='JSON document with keys "username" and "password"')
    args = parser.parse_args()

    if args.creds_file is not None:
        with open(args.creds_file[0], 'r') as f:
            creds = json.load(f)
        username = creds['username']
        password = creds['password']
    elif args.username and args.password:
        username = args.username[0]
        password = args.password[0]
    else:
        sys.exit('You must specify a --creds-file or a --username and --password')

    subscriber = Subscriber(username, password)
    if args.request_lists and args.with_new_lists:
        sys.die('Choose at most one of --request-lists and --with-new-lists')
    if args.request_lists:
        subscriber.request_lists()
    elif args.with_new_lists:
        lists = subscriber.new_lists()
        subscriber.subscribe(lists)
    else:
        lists = subscriber.get_lists()
        if lists is None:
            sys.die('Run with --request-lists first')
        subscriber.subscribe(lists)


if __name__ == '__main__':
    main()
