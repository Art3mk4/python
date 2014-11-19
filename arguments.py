import argparse

class UserAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print 'user'
        if len(namespace.passwords) < len(namespace.users):
            parser.error('Missing password')
        else:
            namespace.users.append(values)

class PasswordAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        print 'password'
        if len(namespace.users) <= len(namespace.passwords):
            parser.error('Missing user')
        else:
            namespace.passwords.append(values)

parser = argparse.ArgumentParser()
parser.add_argument('--password', dest='passwords', default=[], action=PasswordAction, required=True)
parser.add_argument('--user', dest='users', default=[], action=UserAction, required=True)

print(parser.parse_args())