import sqlite3
import json
from models import Entry, Mood, EntryTag

def get_all_entryTags():
    """
    Retrieve all entry tags from the database and returns a list of dictionary representation of the entry tags.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM EntryTags et
        """)
        entryTags = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entryTag = EntryTag(row['id'], row['entry_id'], row['tag_id'])
            entryTags.append(entryTag.__dict__)
        return entryTags

def get_single_entryTag(id):
    '''retrieve single entry tag by id'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute('''
        SELECT
            et.id,
            et.entry_id,
            et.tag_id
        FROM EntryTags et
        WHERE et.id = ?
        ''', (id, ))
        data = db_cursor.fetchone()
        entryTag = EntryTag(data['id'], data['entry_id'], data['tag_id'])
        return entryTag.__dict__


