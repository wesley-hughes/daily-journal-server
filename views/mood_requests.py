import sqlite3
import json
from models import Entry, Mood

def get_all_moods():
    """
    Retrieve all moods from the database and returns a list of dictionary representation of the animals.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            m.id,
            m.label
        FROM Moods m
        """)
        moods = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            mood = Mood(row['id'], row['label'])
            moods.append(mood.__dict__)
        return moods

def get_single_mood(id):
    '''retrieve single journal mood by id'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute('''
        SELECT
            m.id,
            m.label
        FROM Moods m
        WHERE m.id = ?
        ''', (id, ))
        data = db_cursor.fetchone()
        mood = mood(data['id'], data['label'])
        return mood.__dict__





