from flask import Flask, request, jsonify, render_template
import sqlite3
import NLP 


app = Flask(__name__)

# Datenbankverbindung
conn = sqlite3.connect('notes.db')
note=conn.cursor()

note.execute('''
          CREATE TABLE IF NOT EXISTS notizen (
          id TEXT PRIMARY KEY,
          ueberschrift TEXT,
          text TEXT,
          text2 TEXT,
          kategorie TEXT)
          ''')

# Änderung speichern
conn.commit()


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# Bestehende Notiz abrufen
@app.route('/get_note', methods=['POST'])
def get_note():
    note_id = request.json['id']
    
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        note.execute("SELECT text, kategorie FROM notizen WHERE id = ?", (note_id,))
        row = note.fetchone()
        
        if row:
            content, kategorie = row  # Zerlege die Zeile in ihre Bestandteile
            print ("Abrufen",note_id+"#",kategorie)
            return jsonify({"content": content, "category": kategorie}), 200
        else:
            return jsonify({"message": "Note not found"}), 404



# Neue Notiz erstellen
@app.route("/new", methods=['POST'])
def new_note():
    print ("Neu")
    return jsonify({"message": "New contened"}), 200


# Title lesen
@app.route("/get_titles", methods=['GET'])
def get_titles():
    titles = []
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        note.execute("SELECT id, ueberschrift FROM notizen")
        rows = note.fetchall()
        for row in rows:
            titles.append({"id": row[0], "ueberschrift": NLP.Überschift_erzeugen(row[1])})
    return jsonify({"titles": titles}), 200


# Speichern der Daten in der Datenbank
@app.route("/save", methods=['POST'])
def save_note():
    data = request.json
    note_id = data['id']
    content = data['content']
    kategorie = data['category']
    print(note_id,kategorie)

    # Die erste Zeile als Titel nehmen
    
    
    titel = NLP.Überschift_erzeugen(content)
    

    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        
        # Überprüfen, ob die Notiz bereits existiert
        note.execute("SELECT * FROM notizen WHERE id = ?", (note_id,))
        existing_note = note.fetchone()
        
        if existing_note:
            # Notiz aktualisieren
            note.execute("UPDATE notizen SET ueberschrift = ?, text = ?, text2 = ?, kategorie = ? WHERE id = ?", 
                    (titel, content, NLP.Umwandeln(content), kategorie, note_id))
        else:
            # Neue Notiz einfügen
            note.execute("INSERT INTO notizen (id, ueberschrift, text, text2, kategorie) VALUES (?, ?, ?, ?, ?)", 
                    (note_id, titel, content, NLP.Umwandeln(content), kategorie))

        # Änderung speichern
        conn.commit()
        
    return jsonify({"message": "Note saved successfully"}), 200




# Löschen der Datenbank
@app.route("/delete", methods=['POST'])
def delete_note():
    
    data = request.json
    note_id = data['id']
    
    print("Löschen",note_id+"#")
    
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        
        # Überprüfen, ob die Notiz bereits existiert
        note.execute("SELECT * FROM notizen WHERE id = ?", (note_id,))
        existing_note = note.fetchone()
        
        if existing_note:
            # Notiz löschen
            note.execute("DELETE FROM notizen WHERE id = ?", (note_id,))
            conn.commit()
            
            print ("Gefunden")
            return jsonify({"message": "Note deleted successfully"}), 200
        else:
            print ("Nicht gefunden")
            return jsonify({"message": "Note not found"}), 404


# Suche 
@app.route("/search", methods=['POST'])
def search_note():
    search_term = request.json['search_term']
    print ("Suche", search_term+"#")
    
    # Überprüfen, ob der Suchbegriff leer ist
    if not search_term.strip():
        results = []
        with sqlite3.connect('notes.db') as conn:
            note = conn.cursor()
            note.execute("SELECT id, ueberschrift FROM notizen")
            rows = note.fetchall()
            for row in rows:
                results.append({"id": row[0], "ueberschrift": NLP.Überschift_erzeugen(row[1])})
        
    else:
        results = []
        
        with sqlite3.connect('notes.db') as conn:
            note = conn.cursor()
            
            # Suche in der Datenbank
            note.execute("""
                SELECT id, ueberschrift, text, text2 
                FROM notizen 
                WHERE ueberschrift LIKE ? OR text LIKE ? OR text2 LIKE ?
            """, ('%' + search_term + '%', '%' + search_term + '%', '%' + search_term + '%'))
            
            rows = note.fetchall()
            
            for row in rows:
                results.append({
                    "id": row[0], 
                    "ueberschrift": NLP.Überschift_erzeugen(row[1]),
                })
        
    return jsonify({"results": results}), 200


# Kategrorie abrufen aus der DB
@app.route("/get_categories", methods=['GET'])
def get_categories():
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        note.execute("SELECT DISTINCT kategorie FROM notizen")
        categories = [row[0] for row in note.fetchall()]
    print (categories)
    return jsonify({"categories": categories}), 200









if __name__ == "__main__":
    app.run(port=5000, threaded=True)


