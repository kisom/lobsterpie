#!/usr/bin/env python
"""
Utility to manage lobsterpie's database.
"""

# still needs to be done:
#   - data validation

import os
import pickle
import sqlite3
import sys


DB_PATH = os.getenv('LB_DATABASE_PATH')


def create_db():
    """
    Create the database and set up the posted table.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute('CREATE TABLE posted (guid text, title text, link text)')
    conn.commit()
    did_create = False

    try:
        cur.execute('SELECT * FROM posted')
    except sqlite3.OperationalError as error:
        print '[!] %s' % (error, )
    else:
        did_create = True
    finally:
        cur.close()
        conn.close()
    return did_create


def dump_db(filename):
    """
    Dump the database to a serialised Python object, saving to a file.
    """
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    dump = {}
    posted = []

    cur.execute('SELECT * from posted')
    for (guid, title, link) in cur:
        story = {'guid': guid,
                 'title': title,
                 'link': link}
        posted.append(story)
    cur.close()
    conn.close()

    dump = pickle.dumps({'posted': posted})
    try:
        open(filename, 'w').write(dump)
    except IOError as err:
        print '[!] error dumping database: %s' % (err, )
        return False
    else:
        print '[+] successfully dumped database to %s' % (filename, )
        return True


def restore_db(filename):
    """
    Restore the database from a file containing a serialised Python
    object, loading into the database.
    """

    if not os.path.exists(DB_PATH):
        create_db()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    serialized = open(filename).read()
    posted = pickle.loads(serialized)

    for table in posted.keys():
        for story in posted[table]:
            cur.execute('insert into %s values (?, ?, ?)' % (table, ),
                        (story['guid'], story['title'], story['link']))
            conn.commit()
            if cur.rowcount > 0:
                print '[+] successfully loaded '
                print '%s into database' % (story['guid'], )
            else:
                print '[!] database error for %s' % (story['guid'], )


def usage():
    """
    Print a usage message and exit.
    """
    print "usage: %s [command] <filename>" % (sys.argv[0], )
    print "valid commands:"
    print "\tcreate\t\tcreates the database"
    print "\tdump\t\tdump the database to a file"
    print "\trestore\t\trestore a database dump"
    print "\nboth dump and restore expect filenames."
    print "if the database doesn't exist, restore will create it.\n"
    exit(1)


def main(command, filename):
    """
    Decide what to do with the given command and filename.
    """

    if 'create' == command:
        if create_db():
            print '[+] successfully created database.'
        else:
            print '[!] could not create database!'
    elif 'dump' == command:
        if not filename:
            usage()
        if dump_db(filename):
            exit(0)
        else:
            exit(1)
    elif 'restore' == command:
        if not filename:
            usage()
        if restore_db(filename):
            exit(0)
        else:
            exit(1)
    else:
        usage()

if '__main__' == __name__:
    if not DB_PATH:
        print '[!] invalid environment, cowardly refusing to proceed.'
        exit(1)

    ARGS = sys.argv[1:]

    if len(ARGS) == 0:
        usage()
    else:
        COMMAND = ARGS[0]
        if len(ARGS) > 1:
            FILENAME = ARGS[1]
        else:
            FILENAME = None

        main(COMMAND, FILENAME)
