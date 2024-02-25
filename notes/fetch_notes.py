#!/usr/bin/env python3
import sqlite3
import argparse
import script_utils
import numpy as np
import json
import heapq

note_dir = "/home/umar.dabhoiwala/scripts/notes/notes.db"

def main ():
    parser = argparse.ArgumentParser(description="Interface with ChatGPT")

    parser.add_argument('--similar', nargs='+', help='Fetch notes similar to the provided message')
    parser.add_argument('--num-notes', type=int, default=None, help='Number of notes to return (default: 5)')
    parser.add_argument('--fetch-by-tag', type=str, help='Fetch notes by tag')
    parser.add_argument('--fetch-tags', action='store_true', help='Fetch all unique tags')

    args = parser.parse_args()
    if args.fetch_tags:
        fetch_unique_tags()
    elif args.fetch_by_tag:
        fetch_notes_by_tag(args.fetch_by_tag)
    elif args.similar:
        message_string = ' '.join(args.similar)
        if args.num_notes:
            fetch_similar_notes(message_string,args.num_notes)
        else:
            fetch_similar_notes(message_string)
    else:
        fetch_and_print_notes(args.num_notes)

def fetch_unique_tags():
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()
    query = "SELECT DISTINCT tag FROM notes"
    cursor.execute(query)

    tags = cursor.fetchall()

    for tag in tags:
        print(tag)

    conn.close()

# Fetch the notes that match the tags
def fetch_notes_by_tag(tag, num_notes = None):
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()

    if num_notes is not None:
        query = "SELECT id, note_text FROM notes WHERE tag=? LIMIT ?"
        cursor.execute(query, (tag, num_notes,))
    else:
        cursor.execute("SELECT id, note_text FROM notes WHERE tag=?", (tag,))

    rows = cursor.fetchall()

    if rows:
        print(f"Fetched notes with tag '{tag}':")
        for row in rows:
            print(f"ID: {row[0]}, Note: {row[1]}")
    else:
        print(f"No notes found with tag '{tag}'.")

    conn.close()

def fetch_similar_notes(message_string, num_notes=5):

    # Get the vector embedding of the input message
    vec_embed = script_utils.get_vector_embedding(message_string)

    # Connect to the SQLite database
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()

    # Fetch the id, note text, and vector embeddings for all notes
    cursor.execute("SELECT id, note_text, vector_embedding FROM notes")
    rows = cursor.fetchall()


    heap = []

    for row in rows:
        note_id, note_text, note_embedding_json = row
        # Vector embedding stored with json dumps so loading it back
        note_embedding = json.loads(note_embedding_json)

        # Calculating cosine similarity
        similarity = cosine_similarity(np.array(vec_embed), np.array(note_embedding))

        # Restricting the size of the heap so we only get num_notes
        if len(heap) < num_notes:
            heapq.heappush(heap, (similarity, note_id, note_text))
        else:
            heapq.heappushpop(heap, (similarity, note_id, note_text))

    # Convert heap to a sorted list in descending order of similarity
    similar_notes = sorted(heap, key=lambda x: x[0], reverse=True)

    print(f"Top {num_notes} most similar notes:")
    for similarity, note_id, note_text in similar_notes:
        print(f"ID: {note_id}, Similarity: {similarity:.2f}, Note: {note_text}")

def cosine_similarity(vec1, vec2):
    """Compute the cosine similarity between two vectors."""
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

def fetch_and_print_notes(num_notes = None):
    # Connect to the DB
    conn = sqlite3.connect(note_dir)
    cursor = conn.cursor()

    if num_notes is not None:
        query = "SELECT id, note_text, tag FROM notes LIMIT ?"
        cursor.execute(query, (num_notes,))
    else:
        query = "SELECT id, note_text, tag FROM notes"
        cursor.execute(query)

    rows = cursor.fetchall()

    # Print Notes
    if rows:
        print("Fetched notes from database:")
        for row in rows:

            row_string = f"ID: {row[0]}, Note: {row[1]}"
            if row[2] != "None":
                row_string += f", Tag: {row[2]}"

            print(row_string)
    else:
        print("No notes found in the database.")

    conn.close()

if __name__ == "__main__":

    main()