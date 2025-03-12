import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# Creazione del database
conn = sqlite3.connect("chiamate.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS chiamate (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data TEXT,
    chi_chiamato TEXT,
    info_fermo TEXT,
    orario_inizio TEXT,
    orario_fine TEXT
)
""")
conn.commit()

# Funzioni per il database
def aggiungi_chiamata():
    data = entry_data.get()
    chi_chiamato = entry_chiamato.get()
    info_fermo = entry_fermo.get()
    orario_inizio = entry_inizio.get()
    orario_fine = entry_fine.get()

    if data and chi_chiamato and info_fermo and orario_inizio and orario_fine:
        cursor.execute("INSERT INTO chiamate (data, chi_chiamato, info_fermo, orario_inizio, orario_fine) VALUES (?, ?, ?, ?, ?)", 
                       (data, chi_chiamato, info_fermo, orario_inizio, orario_fine))
        conn.commit()
        aggiorna_tabella()
        messagebox.showinfo("Successo", "Chiamata aggiunta con successo!")
    else:
        messagebox.showwarning("Errore", "Compila tutti i campi!")

def aggiorna_tabella():
    for row in tabella.get_children():
        tabella.delete(row)

    cursor.execute("SELECT * FROM chiamate")
    for chiamata in cursor.fetchall():
        tabella.insert("", "end", values=chiamata)

def cerca_chiamata():
    chiave = entry_ricerca.get()
    for row in tabella.get_children():
        tabella.delete(row)

    cursor.execute("SELECT * FROM chiamate WHERE data LIKE ? OR chi_chiamato LIKE ?", ('%'+chiave+'%', '%'+chiave+'%'))
    for chiamata in cursor.fetchall():
        tabella.insert("", "end", values=chiamata)

def elimina_chiamata():
    item = tabella.selection()
    if not item:
        messagebox.showwarning("Errore", "Seleziona una chiamata da eliminare!")
        return

    id_chiamata = tabella.item(item, "values")[0]
    cursor.execute("DELETE FROM chiamate WHERE id=?", (id_chiamata,))
    conn.commit()
    aggiorna_tabella()
    messagebox.showinfo("Successo", "Chiamata eliminata con successo!")

def modifica_chiamata():
    item = tabella.selection()
    if not item:
        messagebox.showwarning("Errore", "Seleziona una chiamata da modificare!")
        return
    finestra_modifica = tk.Toplevel(root)
    finestra_modifica.title("Modifica Chiamata")

#     

# Creazione della finestra principale
root = tk.Tk()
root.title("Gestione Chiamate")
root.geometry("1600x900")

# Campi di input



frame_input = tk.Frame(root)
frame_input.pack(pady=20)

tk.Label(frame_input, text="Data (DD-MM-YYYY):").grid(row=0, column=0, padx=(10, 70))
entry_data = tk.Entry(frame_input)
entry_data.grid(row=0, column=1)


tk.Label(frame_input, text="Chi Chiamato:").grid(row=1, column=0, padx=(10, 70))
entry_chiamato = tk.Entry(frame_input)
entry_chiamato.grid(row=1, column=1)

tk.Label(frame_input, text="Info Fermo:").grid(row=2, column=0, padx=(10, 70))
entry_fermo = tk.Entry(frame_input)
entry_fermo.grid(row=2, column=1)

tk.Label(frame_input, text="Orario Inizio (HH:MM):").grid(row=3, column=0, padx=(10, 70))
entry_inizio = tk.Entry(frame_input)
entry_inizio.grid(row=3, column=1)

tk.Label(frame_input, text="Orario Fine (HH:MM):").grid(row=4, column=0, padx=(10, 70))
entry_fine = tk.Entry(frame_input)
entry_fine.grid(row=4, column=1)



# Pulsanti di azione
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=20, padx=30)

tk.Button(frame_buttons, text="Aggiungi", command=aggiungi_chiamata, bg="green", fg="white").grid(row=0, column=0, padx=15, ipadx=30)
tk.Button(frame_buttons, text="Modifica", command=modifica_chiamata, bg="blue", fg="white").grid(row=0, column=1, padx=15, ipadx=30)
tk.Button(frame_buttons, text="Elimina", command=elimina_chiamata, bg="red", fg="white").grid(row=0, column=2, padx=15, ipadx=30)

# Tabella per visualizzare i dati
frame_table = tk.Frame(root)
frame_table.pack()

colonne = ("ID", "Data", "Chi Chiamato", "Info Fermo", "Inizio", "Fine")
tabella = ttk.Treeview(frame_table, columns=colonne, show="headings",)
for col in colonne:
    tabella.heading(col, text=col)
    tabella.column(col, width=260)
    tabella.column(col,anchor="center")
    from tkinter import ttk

# Creazione dello stile per modificare il font
style = ttk.Style()
style.configure("Treeview", font=("Arial", 14))  # Modifica il font e la dimensione del testo
style.configure("Treeview.Heading", font=("Arial", 16, "bold"))  # Modifica il font delle intestazioni
tabella.pack()

tabella.pack(expand=True, fill="both")  # Espande la tabella per riempire lo spazio

# Ricerca
frame_search = tk.Frame(root)
frame_search.pack(pady=20)
tk.Label(frame_search, text="Cerca (Data/Nome):").grid(row=0, column=0, padx=(10, 70))
entry_ricerca = tk.Entry(frame_search)
entry_ricerca.grid(row=0, column=1, padx=(10, 20))
tk.Button(frame_search, text="Cerca", command=cerca_chiamata).grid(row=0, column=2, padx=10)
style = ttk.Style()


# Frame per la tabella con scrollbar
frame_table = tk.Frame(root)
frame_table.pack(expand=True, fill="both")

# Scrollbar verticale
scrollbar_y = tk.Scrollbar(frame_table, orient="vertical", command=tabella.yview)
tabella.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.pack(side="right", fill="y")

# Scrollbar orizzontale
scrollbar_x = tk.Scrollbar(frame_table, orient="horizontal", command=tabella.xview)
tabella.configure(xscrollcommand=scrollbar_x.set)
scrollbar_x.pack(side="bottom", fill="x")

# Carica i dati iniziali
aggiorna_tabella()
root.mainloop()




