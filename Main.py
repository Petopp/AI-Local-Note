import streamlit as st
import sqlite3
import time


if 'current_category_index' not in st.session_state:
    st.session_state['current_category_index'] = 0

if 'current_note_id' not in st.session_state:
    st.session_state['current_note_id'] = ""
            
            
# Kategorie abrufen aus der DB
def get_categories():
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        note.execute("SELECT DISTINCT kategorie FROM notizen")
        categories = [row[0] for row in note.fetchall()]
    return categories
    

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


# Webseite Konfiguration
st.set_page_config(page_title="AI-Local-Note", page_icon="icons\Icon_Note.png", layout="wide", initial_sidebar_state="auto", menu_items=None)

# DEV hide
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .reportview-container .main .block-container{padding-top: 0px;}
    header {visibility: hidden;}
    
    .vertical-align {
        display: flex;
        align-items: center;
    }
    
    .custom-button {
        width: 70%;
        height: 40px; /* Höhe entsprechend anpassen */
        padding: 8px;
        margin: 30px;
        color: white;
        background-color: olive;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-button:hover {
        background-color: darkkhaki;
    }
    
    .custom-button2 {
        width: 70%;
        height: 40px; /* Höhe entsprechend anpassen */
        padding: 8px;
        margin: 30px;
        color: white;
        background-color: darkred;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-button2:hover {
        background-color: red;
    }

    .custom-button3 {
        width: 70%;
        height: 40px; /* Höhe entsprechend anpassen */
        padding: 8px;
        margin: 30px;
        color: white;
        background-color: darkgreen;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
    .custom-button3:hover {
        background-color: green;
    }
    
    </style>
    """, unsafe_allow_html=True)

# Header, Bild und Text Nebeneinander
Header=st.subheader('AI-Local-Note')
st.write("___")

# Sidebar Navigation mit Suche
st.sidebar.title("Navigation")
search = st.sidebar.text_input("Search", "")
st.sidebar.write("___")

# Kategorie Auswahl
category = st.sidebar.selectbox("Select a category", get_categories(), index=0)
st.sidebar.write("___")



# Definieren Sie die Höhe des Platzhalters
placeholder_height = 10

col1, col2, col3,col4 = st.columns([3, 1,1, 1])

with col1:
    Kateogrie_Box = st.empty()
    Kateogrie_Box.selectbox("Category", ["Option 1", "Option 2"], index=0)

with col2:
    # Benutzerdefinierter Button mit HTML
    new_button_html = '<button class="custom-button3" onclick="alert(\'New!\')">New</button>'
    new_button=st.markdown(new_button_html, unsafe_allow_html=True)

with col3:
    # Benutzerdefinierter Button mit HTML
    save_button_html = '<button class="custom-button" onclick="alert(\'Saved!\')">Save</button>'
    save_button=st.markdown(save_button_html, unsafe_allow_html=True)

with col4:
    # Benutzerdefinierter Button mit HTML
    delete_button_html = '<button class="custom-button2" onclick="alert(\'Deleted!\')">Delete</button>'
    delete_button=st.markdown(delete_button_html, unsafe_allow_html=True)
    


# Editor
Text=st.empty()
Text.text_area("Text", "", height=600)


# Erstellen Sie einen Platzhalter
ID_Code = st.empty()
# Schreiben Sie einen initialen Wert in den Platzhalter
ID_Code.write("-")


# Reagrien auf Kategorie Auswahl
if category:
    # Bestehende Notiz abrufen und mit Radio anzeigen
    with sqlite3.connect('notes.db') as conn:
        note = conn.cursor()
        note.execute("SELECT id, ueberschrift FROM notizen WHERE kategorie = ?", (category,))
        rows = note.fetchall()

        # Falls Ergebnisse vorhanden sind
        if rows:
            # Erstelle eine Liste der Überschriften
            ueberschriften = [row[1] for row in rows]
            # Erstelle Radiobuttons für jede Überschrift
            selected_ueberschrift = st.sidebar.radio("Select a note", ueberschriften)

# Reagiere auf die Auswahl
if selected_ueberschrift:
    
    selected_id = next(row[0] for row in rows if row[1] == selected_ueberschrift)

    # Führe eine weitere Abfrage aus, um die Details der ausgewählten Notiz zu erhalten
    note.execute("SELECT * FROM notizen WHERE id = ?", (selected_id,))
    selected_note = note.fetchone()
    
    # Zeige Details der ausgewählten Notiz
    if selected_note:
        ID_Code.write("ID: "+str(selected_note[0]))
        Text.text_area("Text", selected_note[2], height=600)
        
        st.session_state['current_note_id'] = str(selected_note[0])

        current_categories = get_categories()                   
        current_category = selected_note[4]    
        st.session_state['current_category_index'] = current_categories.index(current_category)
        
        
        # Kateogrie Text wie Auch auswahl nebeneinander
        Kateogrie_Box.selectbox("Category", current_categories, index=st.session_state['current_category_index'])


## Neu
if new_button_html:
    
    
    
    pass


## Speichern
if save_button_html:
    
    
    # Änderung speichern
    conn.commit()
    pass    


## Löschen der Notiz
if delete_button_html:
    
    
    # Änderung speichern
    conn.commit()
    pass