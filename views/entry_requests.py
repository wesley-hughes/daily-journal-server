import sqlite3
import json
from models import Entry, Mood

def get_all_entries():
    """
    Retrieve all entries from the database and returns a list of dictionary representation of the animals.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute("""
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.moodId,
            e.date,
            m.label
        FROM Entries e
        JOIN Moods m
            ON m.id = e.moodId
        """)
        entries = []
        dataset = db_cursor.fetchall()
        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'], row['moodId'],
                    row['date'])
            mood = Mood(row['moodId'], row['label'])
            entry.mood = mood.__dict__
            entries.append(entry.__dict__)
        return entries

def get_single_entry(id):
    '''retrieve single journal entry by id'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute('''
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.moodId,
            e.date
        FROM Entries e
        WHERE e.id = ?
        ''', (id, ))
        data = db_cursor.fetchone()
        entry = Entry(data['id'], data['concept'], data['entry'], data['moodId'],
                    data['date'])
        return entry.__dict__

def update_entry(id, new_entry):
    '''uses id to locate entry, then creates new entry'''
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()
        db_cursor.execute('''
        UPDATE Entries
            SET
               concept = ?,
               entry = ?,
               moodId = ?,
               date = ?
            WHERE id = ? 
        ''', (new_entry['concept'], new_entry['entry'], new_entry['moodId'], new_entry['date'], id, ))
        rows_affected = db_cursor.rowcount
    if rows_affected == 0:
        return False
    else:
        return True

def delete_entry(id):
    """
    Delete the entry with the given ID from the database.
    """

    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM Entries
        WHERE id = ?
        """, (id, ))

def get_entries_by_term(term):
    """
    Retrieve all entries with the specified term and returns the list of dictionary representation of the entries.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        db_cursor.execute('''
        SELECT
            e.id,
            e.concept,
            e.entry,
            e.moodId,
            e.date
        FROM Entries e
        WHERE e.entry LIKE ?
        ''', (f"%{term}%", ))

        entries = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            entry = Entry(row['id'], row['concept'], row['entry'],
                            row['moodId'], row['date'])

            entries.append(entry.__dict__)
    return entries

def create_entry(new_entry):
    """
    Create a new entry in the database with the given data and returns the dictionary representation of the new entry.
    """
    with sqlite3.connect("./dailyjournal.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Entries
            ( concept, entry, moodId, date )
        VALUES
            ( ?, ?, ?, ?);
        """, (new_entry['concept'], new_entry['entry'],
                new_entry['moodId'], new_entry['date']))

        # The `lastrowid` property on the cursor will return
        # the primary key of the last thing that got added to
        # the database.
        id = db_cursor.lastrowid

        # Add the `id` property to the entry dictionary that
        # was sent by the client so that the client sees the
        # primary key in the response.
        new_entry['id'] = id


    return new_entry
