#!/usr/bin/env python3
import sys
import argparse
import subprocess
import sqlite3
import json

from script_utils import get_vector_embedding

# Note put the full path so that you can access them from anywhere
note_dir = "/home/umar.dabhoiwala/scripts/notes/notes.db"
txt_file_dir = "/home/umar.dabhoiwala/scripts/notes/notes.txt"

def main():
    parser = argparse.ArgumentParser(description="Quick note taker")

    parser.add_argument('message', nargs='*', default=[], help='Note to save to file')
    parser.add_argument('--nostore', action='store_true', help='Do not embed the note string')
    parser.add_argument('--initdb', action='store_true', help='Initialize the storage database')
    parser.add_argument('--delete', help='Delete a specific ID or the last n items (format: id or lastn)')
    parser.add_argument('--edit',nargs=2, help= 'Edit a note with a specific ID. Format: --edit ID "New note text"' )
    parser.add_argument('--tag', type=str, default="None", help='Note Tag')

    # Subprocessor arguments to spawn the subprocesses that complete the action
    parser.add_argument('--subprocess-embed', action='store_true', help=argparse.SUPPRESS)
    parser.add_argument('--subprocess-delete', type=str, default='', help=argparse.SUPPRESS)
    parser.add_argument('--subprocess-edit', nargs=2, help=argparse.SUPPRESS)

    args = parser.parse_args()

    if args.initdb:
        initialize_db()

    if args.subprocess_edit:
        note_id, new_text = args.subprocess_edit
        edit_note(note_id, new_text)
        sys.exit(0)

    if args.subprocess_delete:
        delete_notes(args.subprocess_delete)
        sys.exit(0)
        return

    if args.subprocess_embed:
        message_string = ' '.join(args.message)
        process_and_store_embedding(message_string, args.tag)
        sys.exit(0)
        return

    # Spawning delete subprocess
    if args.delete:
        subprocess.Popen([sys.executable, __file__, '--subprocess-delete', args.delete])
        return

    # Spawning edit subprocess
    if args.edit:
        note_id, new_text = args.edit
        subprocess.Popen([sys.executable, __file__, '--subprocess-edit', note_id, new_text])
        return

    # Spawning store subprocess
    message_string = ' '.join(args.message)
    if message_string and not args.nostore:
        subprocess.Popen([sys.executable, __file__, '--subprocess-embed'] + args.message + ['--tag', args.tag])

    # Writing to basic txt
    if message_string:
        save_note_to_file(message_string)
    else:
        print("No message provided or action taken.")


def initialize_db():
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note_text TEXT,
            vector_embedding TEXT,
            tag TEXT DEFAULT 'None'
        );
    """)
    conn.commit()
    conn.close()


def edit_note(note_id, new_text):
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE notes SET note_text = ? WHERE id = ?", (new_text, note_id))
        conn.commit()
    except Exception as e:
        print(f"Error updating note: {e}")
    finally:
        conn.close()

def delete_notes(delete_arg):
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()
    try:
        if delete_arg.startswith('last'):
            n = int(delete_arg[4:])
            cursor.execute("DELETE FROM notes WHERE id IN (SELECT id FROM notes ORDER BY id DESC LIMIT ?)", (n,))
        else:
            note_id = int(delete_arg)
            cursor.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
    except Exception as e:
        print(f"Error deleting note: {e}")
    finally:
        conn.close()

def save_note_to_file(message_string):
    with open(txt_file_dir, 'a') as file:
        file.write(message_string + '\n')

def process_and_store_embedding(message_string, tag="None"):

    vec_embed = get_vector_embedding(message_string)
    vec_embed_str = json.dumps(vec_embed)
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO notes (note_text, vector_embedding, tag) VALUES (?, ?, ?)", (message_string, vec_embed_str, tag))
    conn.commit()
    conn.close()

if __name__ == "__main__":

    main()