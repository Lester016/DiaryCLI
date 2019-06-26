import datetime
import sys
from collections import OrderedDict
from peewee import *


db = SqliteDatabase('diary.db')


class Entry(Model):
    # content
    # timestamp
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def add_entry():
    """Add entry."""
    print("Press ctrl+D when finished")
    entry = sys.stdin.read().strip()

    if entry:
        if input("Save entry? Yn").lower != 'n':
            Entry.create(content=entry)
            print("Saved successfully!")


def view_entries():
    """View Entries"""
    print("tae tae")

def delete_entry(entry):
    """Delete entry."""


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries)
])


def menu_loop():
    """Show the menu."""
    choice = None

    while choice != 'q':
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()


if __name__ == '__main__':
    initialize()
    menu_loop()
