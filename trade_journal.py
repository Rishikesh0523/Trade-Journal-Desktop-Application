import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, simpledialog
import sqlite3
from datetime import datetime
from ttkbootstrap import Style

class TradeJournalApp:
    def __init__(self, master):
        self.master = master
        master.title("Trade Journal")
        master.state('zoomed')  # Start maximized
        
        self.style = Style(theme='darkly')
        
        self.create_tables()
        self.create_menu()

        self.main_frame = ttk.Frame(master)
        self.main_frame.pack(expand=True, fill="both")

        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(expand=True, fill="both", padx=20, pady=20)

        self.add_entry_frame = ttk.Frame(self.notebook)
        self.view_entries_frame = ttk.Frame(self.notebook)
        self.trash_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.add_entry_frame, text="Add Entry")
        self.notebook.add(self.view_entries_frame, text="View Entries")
        self.notebook.add(self.trash_frame, text="Trash")

        self.setup_add_entry_tab()
        self.setup_view_entries_tab()
        self.setup_trash_tab()

        self.master.bind("<Configure>", self.on_resize)

    def create_menu(self):
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Exit", command=self.master.quit)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Minimize", command=self.minimize)
        view_menu.add_command(label="Maximize", command=self.maximize)
        view_menu.add_command(label="Full Screen", command=self.toggle_fullscreen)

    def minimize(self):
        self.master.iconify()

    def maximize(self):
        self.master.state('zoomed')

    def toggle_fullscreen(self):
        self.master.attributes('-fullscreen', not self.master.attributes('-fullscreen'))

    def on_resize(self, event):
        # Resize the text widgets when the window is resized
        width = event.width - 40  # Subtract padding
        height = event.height - 100  # Subtract space for buttons and padding

        if hasattr(self, 'title_entry'):
            self.title_entry.config(width=width // 10)  # Approximate character width

        if hasattr(self, 'description_entry'):
            self.description_entry.config(width=width // 10, height=height // 25)

    def create_tables(self):
        conn = sqlite3.connect('trade_journal.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS trades
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      title TEXT,
                      description TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS trash
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      date TEXT NOT NULL,
                      title TEXT,
                      description TEXT NOT NULL)''')
        conn.commit()
        conn.close()

    def setup_add_entry_tab(self):
        self.add_entry_frame.columnconfigure(1, weight=1)
        self.add_entry_frame.rowconfigure(1, weight=1)

        ttk.Label(self.add_entry_frame, text="Title (optional):").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        self.title_entry = ttk.Entry(self.add_entry_frame, font=('Arial', 12))
        self.title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(self.add_entry_frame, text="Description:").grid(row=1, column=0, sticky="nw", pady=5, padx=5)
        self.description_entry = scrolledtext.ScrolledText(self.add_entry_frame, font=('Arial', 12))
        self.description_entry.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        ttk.Button(self.add_entry_frame, text="Add Entry", command=self.add_entry).grid(row=2, column=1, pady=20, padx=5)

    def setup_view_entries_tab(self):
        self.view_entries_frame.columnconfigure(1, weight=1)
        self.view_entries_frame.rowconfigure(0, weight=1)

        # Create a sidebar for entry selection
        self.sidebar = ttk.Frame(self.view_entries_frame, style='Secondary.TFrame')
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=(5, 0), pady=5)

        # Create a listbox for entry titles
        self.entry_listbox = tk.Listbox(self.sidebar, font=('Arial', 12), bg='#f0f0f0', selectbackground='#a6a6a6')
        self.entry_listbox.pack(expand=True, fill="both", padx=5, pady=5)
        self.entry_listbox.bind('<<ListboxSelect>>', self.on_entry_select)

        # Create a frame for the entry display
        self.entry_frame = ttk.Frame(self.view_entries_frame, style='Primary.TFrame')
        self.entry_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # Create widgets for entry display
        self.entry_title = ttk.Label(self.entry_frame, font=('Arial', 16, 'bold'), wraplength=600)
        self.entry_title.pack(pady=(20, 10), padx=20, anchor='w')

        self.entry_date = ttk.Label(self.entry_frame, font=('Arial', 10), foreground='gray')
        self.entry_date.pack(pady=(0, 10), padx=20, anchor='w')

        self.entry_description = scrolledtext.ScrolledText(self.entry_frame, font=('Arial', 12), wrap=tk.WORD, bg='#ffffff')
        self.entry_description.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        # Create a frame for buttons
        button_frame = ttk.Frame(self.view_entries_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="Refresh Entries", command=self.view_entries).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Entry", command=self.update_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Entry", command=self.delete_entry).pack(side=tk.LEFT, padx=5)

        self.view_entries()  # Load entries when the tab is created

    def setup_trash_tab(self):
        self.trash_frame.columnconfigure(0, weight=1)
        self.trash_frame.rowconfigure(0, weight=1)

        self.trash_text = scrolledtext.ScrolledText(self.trash_frame, font=('Arial', 12))
        self.trash_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        button_frame = ttk.Frame(self.trash_frame)
        button_frame.grid(row=1, column=0, pady=10)
        
        ttk.Button(button_frame, text="Refresh Trash", command=self.view_trash).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Restore Entry", command=self.restore_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Delete Permanently", command=self.delete_permanently).pack(side=tk.LEFT, padx=5)

    def add_entry(self):
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        title = self.title_entry.get()
        description = self.description_entry.get("1.0", tk.END).strip()

        if not description:
            messagebox.showerror("Error", "Description cannot be empty")
            return

        conn = sqlite3.connect('trade_journal.db')
        c = conn.cursor()
        c.execute("INSERT INTO trades (date, title, description) VALUES (?, ?, ?)",
                  (date, title if title else None, description))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Trade entry added successfully!")
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete("1.0", tk.END)
        self.view_entries()  # Refresh the entries list

    def view_entries(self):
        conn = sqlite3.connect('trade_journal.db')
        c = conn.cursor()
        c.execute("SELECT id, date, title, description FROM trades ORDER BY date DESC")
        entries = c.fetchall()
        conn.close()

        self.entry_listbox.delete(0, tk.END)
        self.entries = entries  # Store entries for later use

        for entry in entries:
            display_title = entry[2] if entry[2] else f"Untitled - {entry[1][:10]}"
            self.entry_listbox.insert(tk.END, display_title)

    def on_entry_select(self, event):
        selection = self.entry_listbox.curselection()
        if selection:
            index = selection[0]
            entry = self.entries[index]
            
            self.entry_title.config(text=entry[2] if entry[2] else "Untitled")
            self.entry_date.config(text=entry[1])
            
            self.entry_description.delete("1.0", tk.END)
            self.entry_description.insert(tk.END, entry[3])

    def view_trash(self):
        conn = sqlite3.connect('trade_journal.db')
        c = conn.cursor()
        c.execute("SELECT * FROM trash ORDER BY date DESC")
        entries = c.fetchall()
        conn.close()

        self.trash_text.delete("1.0", tk.END)
        if not entries:
            self.trash_text.insert(tk.END, "No trashed entries found.")
        else:
            for entry in entries:
                self.trash_text.insert(tk.END, f"\nID: {entry[0]}\n", "id")
                self.trash_text.insert(tk.END, f"Date: {entry[1]}\n", "date")
                if entry[2]:
                    self.trash_text.insert(tk.END, f"Title: {entry[2]}\n", "title")
                self.trash_text.insert(tk.END, f"Description: {entry[3]}\n", "description")
                self.trash_text.insert(tk.END, "-" * 50 + "\n", "separator")
        
        self.trash_text.tag_configure("id", font=('Arial', 12, 'bold'), foreground="blue")
        self.trash_text.tag_configure("date", font=('Arial', 12, 'bold'))
        self.trash_text.tag_configure("title", font=('Arial', 12, 'italic'))
        self.trash_text.tag_configure("description", font=('Arial', 12))
        self.trash_text.tag_configure("separator", foreground="gray")

    def update_entry(self):
        selection = self.entry_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an entry to update")
            return

        index = selection[0]
        entry = self.entries[index]

        update_window = tk.Toplevel(self.master)
        update_window.title("Update Entry")
        update_window.geometry("500x400")
        
        update_window.columnconfigure(1, weight=1)
        update_window.rowconfigure(1, weight=1)

        ttk.Label(update_window, text="Title:").grid(row=0, column=0, sticky="w", pady=5, padx=5)
        title_entry = ttk.Entry(update_window, font=('Arial', 12))
        title_entry.insert(0, entry[2] if entry[2] else "")
        title_entry.grid(row=0, column=1, sticky="ew", pady=5, padx=5)

        ttk.Label(update_window, text="Description:").grid(row=1, column=0, sticky="nw", pady=5, padx=5)
        description_entry = scrolledtext.ScrolledText(update_window, font=('Arial', 12))
        description_entry.insert(tk.END, entry[3])
        description_entry.grid(row=1, column=1, sticky="nsew", pady=5, padx=5)

        def save_update():
            new_title = title_entry.get()
            new_description = description_entry.get("1.0", tk.END).strip()
            
            conn = sqlite3.connect('trade_journal.db')
            c = conn.cursor()
            c.execute("UPDATE trades SET title=?, description=? WHERE id=?",
                      (new_title if new_title else None, new_description, entry[0]))
            conn.commit()
            conn.close()
            
            messagebox.showinfo("Success", "Entry updated successfully!")
            update_window.destroy()
            self.view_entries()

        ttk.Button(update_window, text="Save", command=save_update).grid(row=2, column=1, pady=10, padx=5)

    def delete_entry(self):
        selection = self.entry_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select an entry to delete")
            return

        index = selection[0]
        entry = self.entries[index]

        if messagebox.askyesno("Confirm", "Are you sure you want to move this entry to trash?"):
            conn = sqlite3.connect('trade_journal.db')
            c = conn.cursor()
            c.execute("INSERT INTO trash (date, title, description) VALUES (?, ?, ?)",
                      (entry[1], entry[2], entry[3]))
            c.execute("DELETE FROM trades WHERE id=?", (entry[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Entry moved to trash")
            self.view_entries()

    def restore_entry(self):
        id = simpledialog.askstring("Restore Entry", "Enter the ID of the entry to restore:")
        if id:
            conn = sqlite3.connect('trade_journal.db')
            c = conn.cursor()
            c.execute("SELECT * FROM trash WHERE id=?", (id,))
            entry = c.fetchone()
            if entry:
                c.execute("INSERT INTO trades (date, title, description) VALUES (?, ?, ?)",
                          (entry[1], entry[2], entry[3]))
                c.execute("DELETE FROM trash WHERE id=?", (id,))
                conn.commit()
                messagebox.showinfo("Success", "Entry restored")
            else:
                messagebox.showerror("Error", "Entry not found")
            conn.close()
            self.view_trash()
            self.view_entries()  # Refresh the main entries list

    def delete_permanently(self):
        id = simpledialog.askstring("Delete Permanently", "Enter the ID of the entry to delete permanently:")
        if id:
            if messagebox.askyesno("Confirm", "Are you sure you want to permanently delete this entry?"):
                conn = sqlite3.connect('trade_journal.db')
                c = conn.cursor()
                c.execute("DELETE FROM trash WHERE id=?", (id,))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Entry permanently deleted")
                self.view_trash()

if __name__ == "__main__":
    root = tk.Tk()
    app = TradeJournalApp(root)
    root.mainloop()