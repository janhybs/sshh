# -*- coding: utf-8 -*-

import yaml
import os
import argparse
import itertools

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'



class Connection(object):
    """
    Represent Connection config entry
    :type tags:     list[str]
    :type server:   str
    :type password: str
    :type keyfile:  str
    :type user:     str
    :type workdir:  str
    :type verbose:  bool
    :type port:     int
    """
    def __init__(self, user='jan-hybs', port=22, tags=list(), password=None, server=None, keyfile=None, verbose=None, workdir=None):
        self.user = user
        self.port = port
        self.tags = [str(x) for x in tags]
        self.password = password
        self.server = server
        self.keyfile = keyfile
        self.verbose = verbose
        self.workdir = workdir

    def describe(self):
        name = '%s@%s' % (self.user, self.server)

        if self.port != 22:
            name = '%s@%s:%d' % (self.user, self.server, self.port)

        if self.workdir:
            name += self.workdir
        return name

    def pretty(self, include_tags=True):
        parts = list()
        parts += [color.PURPLE, self.user, color.END]
        parts += [color.BOLD, '@', color.END]
        parts += [color.DARKCYAN, self.server, color.END]
        length = len(self.user) + len(self.server)
        if self.port != 22:
            length += 1 + len(str(self.port))
            parts += [color.BOLD, ':', color.RED, str(self.port), color.END]

        if self.workdir:
            length += len(self.workdir)
            parts += [color.BOLD, color.BLUE, self.workdir, color.END]

        if include_tags:
            if self.tags:
                c = max(0, 64 - length)
                tags = ['%s%s%s' % (color.BLUE, x, color.END) for x in self.tags]
                parts += [' ' * c, ' (', ', '.join(tags) ,')']
        return ''.join(parts)

    def get_hints(self):
        if self.tags:
            return self.tags + [self.server]
        return [self.server]

    def __repr__(self):
        host = self.describe()
        return host


__dir__ = os.path.abspath(os.path.dirname(__file__))
yaml_file = os.path.join(__dir__, '.sshh.yaml')
config = yaml.load(open(yaml_file, 'r').read())
connections = [Connection(**c) for c in config]


def find_connection(hint):
    """
    Find first suitable connection entry from yaml config
    :param hint: search value
    :return: Connection
    """
    if not hint:
        for con in connections:
            yield con
    else:
        for con in connections:
            for tag in con.get_hints():
                if tag.find(hint) != -1:
                    yield con
                    break


parser = argparse.ArgumentParser()
parser.add_argument('-l', '--list', action='store_true')
parser.add_argument('-f', '--find', type=str)
parser.add_argument('-c', '--connect', type=str)

args = parser.parse_args()

if args.list:
    hints = list(itertools.chain.from_iterable([m.get_hints() for m in connections]))
    print(' '.join(hints), end='\n')
    exit(0)

if args.find is not None:
    matches = list(find_connection(args.find)) or list(find_connection(''))
    hints = list(itertools.chain.from_iterable([m.get_hints() for m in matches]))
    print(' '.join(hints), end='\n')
    exit(0)

if args.connect is not None:
    matches = list(find_connection(args.connect))
    hints = list(itertools.chain.from_iterable([m.get_hints() for m in connections]))
    if len(matches) == 0:
        print("No results matches your query, here are the servers:")
        for c in connections:
            idx, fmt = connections.index(c)+1, c.pretty()
            print(' - %d) %s' % (idx, fmt))
    elif len(matches) > 0:
        #print("Multiple results matches your query:")
        #for c in matches:
        #    idx, fmt = connections.index(c) + 1, c.pretty()
        #    print(' - %d) %s' % (idx, fmt))
        connection = matches[0]

        #print('Connection to the first server (%s)' % connection.pretty(False))
        command = list()
        command += ['ssh']
        if connection.workdir:
            command += ['-t']
        if connection.port != 22:
            command += ['-p', str(connection.port)]

        command += ['%s@%s' % (connection.user, connection.server)]
        if connection.workdir:
            command += ['"cd %s ; bash"' % connection.workdir]

        if connection.password:
            command = ['sshpass', '-f', os.path.join(__dir__, connection.password)] + command

        command_str = ' '.join(command)
        print(command_str, end='')
        exit(0)


print("Available servers:")
for c in connections:
    idx, fmt = connections.index(c) + 1, c.pretty()
    print(' %d) %s' % (idx, fmt))

