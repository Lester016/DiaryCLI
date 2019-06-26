import datetime
import sys
import os
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
        if input("Save entry? Yn: ").lower != 'n':
            Entry.create(content=entry)
            print("Saved successfully!")


def view_entries(search_query=None):
    """View Entries"""
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime("%A %B %d, %Y %I:%M:%p")
        clear_screen()
        print(timestamp)
        print("="*len(timestamp)+"\n")
        print(entry.content)
        print("\n"+"="*len(timestamp))
        print("n) to next entry.")
        print('d) to delete entry.')
        print("q) to return to main menu.")

        next_action = input("Action: ").lower().strip()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)


def search_entries():
    """Search entry in your diary."""
    view_entries(input('Search query: '))


def delete_entry(entry):
    """Delete entry."""
    if input("Are you sure you want to delete this? [Yn]: ").lower() == 'y':
        entry.delete_instance()
        print("Entry deleted successfully!")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def initialize():
    """Create the database and the table if they don't exist."""
    db.connect()
    db.create_tables([Entry], safe=True)


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries)
])


def menu_loop():
    """Show the menu."""
    choice = None
    while choice != 'q':
        clear_screen()
        print("Enter 'q' to quit.")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action: ").lower().strip()

        if choice in menu:
            menu[choice]()


if __name__ == '__main__':
    initialize()
    menu_loop()
